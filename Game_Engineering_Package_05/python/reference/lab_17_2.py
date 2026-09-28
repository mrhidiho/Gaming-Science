"""Compare content, not claimed speed, of two file-access paths."""
import hashlib
import mmap
from pathlib import Path

MAX_FILE_BYTES = 1024 * 1024

def file_digests(path: str | Path) -> tuple[str, str]:
    path = Path(path)
    # Lab assumption: a regular file in an exclusively owned scratch folder;
    # no concurrent writer or hostile path replacement during this operation.
    if not path.is_file() or path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError("expected a regular file no larger than 1 MiB")
    h = hashlib.sha256()
    with path.open("rb") as f:
        total = 0
        while chunk := f.read(4096):
            total += len(chunk)
            if total > MAX_FILE_BYTES:
                raise ValueError("file grew beyond the lab size limit")
            h.update(chunk)
    with path.open("rb") as f:
        if path.stat().st_size == 0:
            mapped = hashlib.sha256(b"").hexdigest()
        else:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mapping:
                mapped = hashlib.sha256(mapping).hexdigest()
    return h.hexdigest(), mapped
