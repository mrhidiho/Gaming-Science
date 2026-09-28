# ForgeQueue worked reference

This is a small learning prototype realizing Gate D. It is not a production service and is not an independent student submission. Read `source/CAPSTONE_SPEC.md` for the complete contract and failure model.

Build the native targets first. From the package root run `python3 capstone/reference/run_demo.py --native build/native_worker`, using the actual platform-specific executable location. The demo creates a temporary private database, binds an ephemeral port on 127.0.0.1, performs a split-frame request and replay, checks one retained row, then shuts down and removes its temporary directory. It leaves no persistent public listener.

## Responsibilities

`gateway.py` owns transport. Its single acceptor processes one active peer at a time, uses a bounded absolute receive deadline, and returns UNKNOWN_OUTCOME when its result wait expires. The in-process service can accept concurrent work even though this deliberately small network gateway is serial.

`service.py` owns admission, workers and commitment. Capacity tickets cover queued/running work. A trusted native worker receives only validated integers in an argument list, without a shell. Its result is independently checked. The service lock orders cancellation against committing; it is not held during computation or while joining the pool.

`ResultStore` creates a separate SQLite connection for each operation. An explicit transaction compares a retained identity/payload or inserts one result. It does not promise exactly-once computation. Full history rejects new identities instead of evicting replay protection.

## Two worked decisions

**ADR-1: Native worker plus Python supervisor.** This makes native execution, process boundaries, errors and validated serialization observable with standard tools. Alternatives include one all-C++ process or an in-process pure Python calculation. Costs are subprocess startup, copying and a trusted-executable assumption. This small workload is educational, not evidence that process isolation is the fastest arithmetic design.

**ADR-2: SQLite plus retained request records.** A local transaction keeps the identity, canonical request and result consistent without a server installation. An in-memory dictionary would lose replay history at restart; a database server adds deployment and concurrency considerations unnecessary for this local prototype. Costs include serialized writes, disk growth within the record quota, and a bounded replay scope. PostgreSQL study remains part of the source curriculum and is not claimed to have been exercised by these SQLite tests.

## Evidence map

Native contract tests exercise arithmetic, bounds, cache modeling, coherent inventory access, queue shutdown and publication. Graph tests exercise worker counts, failure propagation and cycles. Python lab tests cover parsing, framing, temporary saves, SQL constraints and atomic transfers. Capstone tests cover capacity, cancellation before/after commitment, graceful drain, worker failure, replay, conflicting identities and real native loopback execution when NATIVE_WORKER is set. The full verifier sets it; running tests manually without it explicitly skips three integration checks.

The reference still requires human design review. No test establishes every scheduling interleaving, every filesystem failure, complete accessibility, resistance to malicious local processes, or safe execution of arbitrary code. The student must supply a changed operation or similarly bounded extension, at least twenty learner-authored acceptance tests and the requested evidence dossier.
