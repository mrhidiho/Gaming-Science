"""ForgeQueue: local bounded jobs with transactional replay records.

Learning reference, NOT a public service or hostile-executable sandbox.
Only the shipped/trusted native worker may be configured as the executable.
"""
from concurrent.futures import ThreadPoolExecutor, Future, CancelledError
import json
from pathlib import Path
import sqlite3
import subprocess
import threading
from typing import Callable
from python.reference.lab_19_2 import parse_request, canonical_request

class BusyError(RuntimeError):
    pass

class WorkerError(RuntimeError):
    pass

class ResultStore:
    def __init__(self, path: Path, limit: int = 1024):
        self.path = Path(path)
        if type(limit) is not int or not 1 <= limit <= 1024:
            raise ValueError("history limit must be 1..1024")
        self.limit = limit
        with self._connection() as db:
            db.execute("PRAGMA journal_mode=DELETE")
            db.execute("CREATE TABLE IF NOT EXISTS job_results ("
                       "id TEXT PRIMARY KEY NOT NULL, payload TEXT NOT NULL, "
                       "result INTEGER NOT NULL CHECK(typeof(result)='integer' "
                       "AND result BETWEEN 0 AND 256000000))")

    def _connection(self):
        # Each call owns its connection; no cross-thread connection sharing.
        from contextlib import contextmanager
        @contextmanager
        def connection():
            db = sqlite3.connect(self.path, isolation_level=None, timeout=1.0)
            db.execute("PRAGMA synchronous=FULL")
            try:
                yield db
            finally:
                db.close()
        return connection()

    def commit(self, job: dict, result: int) -> dict:
        payload = canonical_request(job)
        if type(result) is not int or not 0 <= result <= 256000000:
            raise WorkerError("native result outside the declared range")
        with self._connection() as db:
            db.execute("BEGIN IMMEDIATE")
            try:
                row = db.execute("SELECT payload,result FROM job_results WHERE id=?",(job["id"],)).fetchone()
                if row:
                    if row[0] != payload:
                        raise ValueError("request ID conflicts with stored work")
                    result = row[1]
                else:
                    if db.execute("SELECT COUNT(*) FROM job_results").fetchone()[0] >= self.limit:
                        raise BusyError("result history full; existing replay records retained")
                    db.execute("INSERT INTO job_results VALUES (?,?,?)",(job["id"],payload,result))
                db.execute("COMMIT")
            except BaseException:
                if db.in_transaction:
                    db.execute("ROLLBACK")
                raise
        return {"version":1,"id":job["id"],"status":"done","result":result}

    def count(self) -> int:
        with self._connection() as db:
            return db.execute("SELECT COUNT(*) FROM job_results").fetchone()[0]


def native_compute(executable: Path, values: list[int]) -> int:
    # Values have passed parse_request. Executable path is owner configuration.
    try:
        run = subprocess.run([str(executable), *map(str, values)], shell=False,
                             capture_output=True, text=True, timeout=5.0)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise WorkerError("trusted native worker failed or timed out") from error
    if run.returncode != 0 or len(run.stdout) > 128:
        raise WorkerError("trusted native worker returned an error")
    output = run.stdout.strip()
    if not output.isascii() or not output.isdecimal():
        raise WorkerError("native worker returned an invalid integer")
    result = int(output)
    # Independent oracle is cheap for this educational workload. In a large
    # pipeline use a justified validation strategy instead of assuming this scales.
    expected = sum(x*x for x in values)
    if result != expected:
        raise WorkerError("native/reference result mismatch")
    return result

class Service:
    def __init__(self, path: Path, executable: Path | None = None, *,
                 workers: int = 2, capacity: int = 4, history_limit: int = 1024,
                 compute: Callable[[list[int]], int] | None = None):
        if type(workers) is not int or type(capacity) is not int or not 1 <= workers <= capacity <= 32:
            raise ValueError("require 1 <= workers <= capacity <= 32")
        if compute is None:
            if executable is None:
                raise ValueError("native executable required")
            selected = Path(executable).resolve(strict=True)
            compute = lambda values: native_compute(selected, values)
        self.store = ResultStore(Path(path),history_limit)
        self.compute = compute
        self.lock = threading.Lock()
        self.accepting = True
        self.cancel_requested = False
        self.tickets = threading.BoundedSemaphore(capacity)
        self.pool = ThreadPoolExecutor(max_workers=workers,thread_name_prefix="forge")

    def submit(self, payload: bytes) -> Future:
        job = parse_request(payload)
        with self.lock:
            if not self.accepting:
                raise BusyError("service is shutting down")
            if not self.tickets.acquire(blocking=False):
                raise BusyError("accepted-work capacity reached")
            try:
                future = self.pool.submit(self._work,job)
            except BaseException:
                self.tickets.release()
                raise
        # add_done_callback may execute immediately. It does not take self.lock.
        future.add_done_callback(lambda _: self.tickets.release())
        return future

    def _work(self, job: dict) -> dict:
        with self.lock:
            if self.cancel_requested:
                raise CancelledError("cancelled before computation")
        result = self.compute(job["values"])
        with self.lock:
            if self.cancel_requested:
                raise CancelledError("cancelled before persistence")
            # Commit and cancellation are serialized at this boundary. Cancellation
            # is not a rollback of a commit that already won this lock.
            return self.store.commit(job,result)

    def shutdown(self, cancel: bool = False) -> None:
        with self.lock:
            self.accepting = False
            self.cancel_requested |= cancel
        # Never join while holding the lock needed by workers.
        self.pool.shutdown(wait=True,cancel_futures=cancel)

    def __enter__(self):
        return self

    def __exit__(self, kind, value, traceback):
        self.shutdown(cancel=kind is not None)
