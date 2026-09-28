"""Strict version-1 request parser. Payloads are data, never executable code."""
import json
import re

_ID = re.compile(r"[A-Za-z0-9_-]{1,32}\Z", re.ASCII)

def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result

def _constant(_):
    raise ValueError("non-finite JSON constant")

def parse_request(payload: bytes) -> dict:
    if type(payload) is not bytes or not 1 <= len(payload) <= 4096:
        raise ValueError("request must be 1..4096 bytes")
    try:
        job = json.loads(payload.decode("utf-8"), object_pairs_hook=_pairs,
                         parse_constant=_constant)
    except (UnicodeError, ValueError, RecursionError) as error:
        raise ValueError("invalid request encoding") from error
    if type(job) is not dict or set(job) != {"version", "id", "operation", "values"}:
        raise ValueError("request has missing or unknown fields")
    if type(job["version"]) is not int or job["version"] != 1:
        raise ValueError("unsupported request version")
    if type(job["id"]) is not str or not _ID.fullmatch(job["id"]):
        raise ValueError("invalid request ID")
    if job["operation"] != "sum_squares":
        raise ValueError("unsupported operation")
    values = job["values"]
    if type(values) is not list or not 1 <= len(values) <= 256:
        raise ValueError("expected 1..256 values")
    if any(type(x) is not int or not 0 <= x <= 1000 for x in values):
        raise ValueError("values must be integers in 0..1000")
    return job

def canonical_request(job: dict) -> str:
    raw = json.dumps(job, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    checked = parse_request(raw)
    return json.dumps(checked, sort_keys=True, separators=(",", ":"))
