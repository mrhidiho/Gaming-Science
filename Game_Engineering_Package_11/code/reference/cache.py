"""Cold, read-only, set-associative LRU cache. No overlap or hardware timing."""
from dataclasses import dataclass
from .checks import integer, power_of_two, finite


@dataclass(frozen=True)
class CacheConfig:
    sets: int
    ways: int
    line_bytes: int = 64

    def __post_init__(self):
        power_of_two(self.sets, 'sets')
        integer(self.ways, 'ways', 1)
        power_of_two(self.line_bytes, 'line_bytes')


class Cache:
    def __init__(self, config: CacheConfig):
        self.config = config
        self.tags = [[] for _ in range(config.sets)]  # LRU at index zero.

    def access(self, address: int) -> bool:
        integer(address, 'address')
        block = address // self.config.line_bytes
        index, tag = block % self.config.sets, block // self.config.sets
        row = self.tags[index]
        hit = tag in row
        if hit:
            row.remove(tag)
        elif len(row) == self.config.ways:
            row.pop(0)
        row.append(tag)
        return hit


def cache_hits(addresses, sets, ways, line_bytes=64):
    cache = Cache(CacheConfig(sets, ways, line_bytes))
    return [cache.access(a) for a in addresses]


def serial_cycles(requests, misses, hit_cost, additional_miss_penalty):
    integer(requests, 'requests'); integer(misses, 'misses')
    if misses > requests:
        raise ValueError('misses cannot exceed requests')
    h = finite(hit_cost, 'hit_cost', 0)
    p = finite(additional_miss_penalty, 'additional_miss_penalty', 0)
    return requests * h + misses * p


def workloads():
    """Synthetic byte-address traces; not measured game-engine traces."""
    return {
        'stream': [i * 64 for i in range(64)],
        'localized': [i * 64 for _ in range(16) for i in range(4)],
        'conflict': [i * 4 * 64 for _ in range(16) for i in range(4)],
    }
