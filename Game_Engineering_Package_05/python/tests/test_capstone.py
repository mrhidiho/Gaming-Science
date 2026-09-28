from concurrent.futures import CancelledError
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import threading
import time
import unittest
from capstone.reference.service import Service,ResultStore,BusyError,WorkerError,native_compute
from capstone.reference.gateway import Gateway,exchange
from python.reference.lab_19_1 import recv_frame

NATIVE=os.environ.get("NATIVE_WORKER")
def raw(identifier="one", values=None):
    return json.dumps({"version":1,"id":identifier,"operation":"sum_squares","values":[2,3] if values is None else values}).encode()
def compute(values):return sum(x*x for x in values)

class TestCapstone(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.db=Path(self.tmp.name)/"results.sqlite"
    def service(self,**kwargs):return Service(self.db,compute=compute,**kwargs)
    def test_simple(self):
        with self.service() as s:self.assertEqual(s.submit(raw()).result(2)["result"],13)
    def test_invalid_before_admission(self):
        with self.service() as s:
            with self.assertRaises(ValueError):s.submit(b"bad")
            self.assertEqual(s.store.count(),0)
    def test_duplicate_concurrent(self):
        with self.service(workers=4,capacity=32) as s:
            futures=[s.submit(raw()) for _ in range(16)]
            results=[f.result(3) for f in futures]
            self.assertTrue(all(r==results[0] for r in results));self.assertEqual(s.store.count(),1)
    def test_id_conflict(self):
        with self.service() as s:
            s.submit(raw()).result(2)
            with self.assertRaises(ValueError):s.submit(raw(values=[1])).result(2)
            self.assertEqual(s.store.count(),1)
    def test_restart(self):
        with self.service() as s:first=s.submit(raw()).result(2)
        with self.service() as s:self.assertEqual(s.submit(raw()).result(2),first);self.assertEqual(s.store.count(),1)
    def test_history_quota_keeps_replays(self):
        with self.service(history_limit=1) as s:
            first=s.submit(raw()).result(2)
            with self.assertRaises(BusyError):s.submit(raw("two")).result(2)
            self.assertEqual(s.submit(raw()).result(2),first);self.assertEqual(s.store.count(),1)
    def test_backpressure_and_release(self):
        started=threading.Event();release=threading.Event()
        def slow(v):started.set();release.wait(3);return compute(v)
        with Service(self.db,workers=1,capacity=1,compute=slow) as s:
            f=s.submit(raw());self.assertTrue(started.wait(2))
            try:
                with self.assertRaises(BusyError):s.submit(raw("two"))
            finally:release.set()
            f.result(2);self.assertEqual(s.submit(raw("two")).result(2)["result"],13)
    def test_worker_failure_no_commit(self):
        def bad(_):raise WorkerError("injected")
        with Service(self.db,compute=bad) as s:
            with self.assertRaises(WorkerError):s.submit(raw()).result(2)
            self.assertEqual(s.store.count(),0)
    def test_cancel_pending_and_running_before_commit(self):
        started=threading.Event();release=threading.Event()
        def slow(v):started.set();release.wait(5);return compute(v)
        s=Service(self.db,workers=1,capacity=2,compute=slow)
        a=s.submit(raw());self.assertTrue(started.wait(2));b=s.submit(raw("two"))
        closer=threading.Thread(target=lambda:s.shutdown(cancel=True));closer.start()
        until=time.monotonic()+2
        try:
            while time.monotonic()<until:
                with s.lock:cancelled=s.cancel_requested
                if cancelled:break
                time.sleep(0.001)
            self.assertTrue(cancelled)
        finally:release.set();closer.join(3)
        self.assertFalse(closer.is_alive())
        with self.assertRaises(CancelledError):a.result(1)
        with self.assertRaises(CancelledError):b.result(1)
        self.assertEqual(s.store.count(),0)
    def test_cancel_after_commit_does_not_undo(self):
        s=self.service();s.submit(raw()).result(2);s.shutdown(cancel=True);self.assertEqual(s.store.count(),1)
    def test_graceful_drain(self):
        s=self.service(capacity=16);futures=[s.submit(raw(str(i))) for i in range(12)];s.shutdown()
        self.assertTrue(all(f.result(1)["result"]==13 for f in futures));self.assertEqual(s.store.count(),12)
        with self.assertRaises(BusyError):s.submit(raw("late"))
    def test_limits(self):
        for kw in [{"workers":0},{"capacity":0},{"workers":4,"capacity":2},{"history_limit":0}]:
            with self.assertRaises(ValueError):self.service(**kw)
    def test_direct_store_invalid_result(self):
        store=ResultStore(self.db)
        with self.assertRaises(WorkerError):store.commit(json.loads(raw()),True)
        self.assertEqual(store.count(),0)
    def test_loopback_split_and_replay(self):
        with self.service() as s:
            with Gateway(s) as g:
                first=exchange(g.address,raw(),split=True);second=exchange(g.address,raw())
                self.assertEqual(first,second);self.assertEqual(first["result"],13);self.assertFalse(g.errors)
    def test_loopback_bad_schema(self):
        with self.service() as s:
            with Gateway(s) as g:self.assertEqual(exchange(g.address,b"{}")['code'],"INVALID_REQUEST")
    def test_loopback_bad_length(self):
        with self.service() as s:
            with Gateway(s) as g:
                with socket.create_connection(g.address,timeout=2) as peer:
                    peer.sendall(b"\xff\xff\xff\xff")
                    r=json.loads(recv_frame(peer,time.monotonic()+2))
                    self.assertEqual(r["code"],"INVALID_REQUEST")
    @unittest.skipUnless(NATIVE,"set NATIVE_WORKER to test the built native executable")
    def test_real_native(self):self.assertEqual(native_compute(Path(NATIVE),[2,3,4]),29)
    @unittest.skipUnless(NATIVE,"set NATIVE_WORKER to test the built native executable")
    def test_real_native_bad_argument(self):
        result=subprocess.run([NATIVE,"1001"],capture_output=True,text=True,timeout=2)
        self.assertEqual(result.returncode,2);self.assertFalse(result.stdout)
    @unittest.skipUnless(NATIVE,"set NATIVE_WORKER to test the built native executable")
    def test_native_loopback_integration(self):
        with Service(self.db,Path(NATIVE)) as s:
            with Gateway(s) as g:
                r=exchange(g.address,raw(values=[0,1000,4]));self.assertEqual(r["result"],1000016)

if __name__=="__main__":unittest.main()
