"""Deterministic nonpreemptive FCFS model; times are invented model units."""
def schedule_fcfs(jobs: list[tuple[int, int, int]]) -> list[dict]:
    if type(jobs) is not list or len(jobs) > 128:
        raise ValueError("at most 128 jobs")
    for row in jobs:
        if not isinstance(row, (list, tuple)) or len(row) != 3:
            raise ValueError("each job is (release, duration, absolute deadline)")
        if any(type(v) is not int or not 0 <= v <= 100000 for v in row):
            raise ValueError("times must be nonnegative bounded integers")
        if row[1] == 0 or row[2] < row[0]:
            raise ValueError("positive duration; deadline no earlier than release")
    now = 0
    result = []
    # Stable tie break: original position, not a nondeterministic task identity.
    for index in sorted(range(len(jobs)), key=lambda i: (jobs[i][0], i)):
        release, duration, deadline = jobs[index]
        start = max(now, release)
        now = start + duration
        result.append({"job": index, "start": start, "finish": now,
                       "lateness": max(0, now - deadline)})
    return result
