"""Exception-injection save lab. NOT a proof of power-loss durability."""
import json
import os
import tempfile
from pathlib import Path

class InjectedFailure(RuntimeError):
    pass

def validate_save(value: object) -> dict:
    if type(value) is not dict or set(value) != {"version", "score"}:
        raise ValueError("save requires exactly version and score")
    if type(value["version"]) is not int or value["version"] != 1:
        raise ValueError("unsupported save version")
    if type(value["score"]) is not int or not 0 <= value["score"] <= 1000000:
        raise ValueError("score must be an integer in 0..1000000")
    return dict(value)

def write_save(path: str | Path, value: dict, fail_at: str | None = None) -> None:
    if fail_at not in {None, "before_write", "partial_write", "before_replace", "after_replace"}:
        raise ValueError("unknown failure point")
    payload = json.dumps(validate_save(value), sort_keys=True).encode("utf-8")
    path = Path(path)
    if path.is_symlink() or not path.parent.is_dir():
        raise ValueError("use an ordinary destination in your private scratch directory")
    # Trusted parent directory and one writer; racing path attacks are outside this lab.
    fd, temporary = tempfile.mkstemp(prefix=".course-save-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            if fail_at == "before_write":
                raise InjectedFailure(fail_at)
            if fail_at == "partial_write":
                f.write(payload[:len(payload)//2])
                raise InjectedFailure(fail_at)
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
        if fail_at == "before_replace":
            raise InjectedFailure(fail_at)
        os.replace(temporary, path)
        if fail_at == "after_replace":
            raise InjectedFailure(fail_at)
        # Parent-directory synchronization is deliberately NOT promised here.
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

def read_save(path: str | Path) -> dict:
    with Path(path).open("rb") as f:
        raw = f.read(1025)
    if len(raw) > 1024:
        raise ValueError("save too large")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError, RecursionError) as error:
        raise ValueError("invalid save encoding") from error
    return validate_save(value)


def write_save_async(executor, path, value):
    """Offload blocking I/O, owning a private snapshot until Future completion.

    Only one outstanding write per destination. This is a thread-based adapter,
    not a kernel-native asynchronous I/O implementation.
    """
    snapshot = validate_save(value)
    return executor.submit(write_save, path, snapshot)
