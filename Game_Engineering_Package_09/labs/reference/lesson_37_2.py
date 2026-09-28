"""Lesson 37.2 computational slice.

Count unique byte-addressed sectors touched by one modeled memory instruction, including cross-sector words and repeated addresses. Fields: addresses, word_bytes (1..128), sector_bytes (1..4096). useful_unique_bytes is not the logical byte count for broadcast reads. Cache reuse, merging across instructions and actual DRAM traffic are not simulated.
"""
from __future__ import annotations

from labs.common import integer

def solve(case: dict) -> dict:
    word=integer(case['word_bytes'],'word_bytes',1,128)
    sector=integer(case['sector_bytes'],'sector_bytes',1,4096)
    addresses=case['addresses']
    touched=set(); useful=set()
    for addr in addresses:
        integer(addr,'address')
        for byte in range(addr,addr+word): useful.add(byte); touched.add(byte//sector)
    transfer=len(touched)*sector
    return {'sectors':len(touched),'transferred_bytes':transfer,'useful_unique_bytes':len(useful),
            'utilization':len(useful)/transfer if transfer else 0.0}

def bank_conflict(words: list[int], banks: int=32) -> int:
    integer(banks,'banks',1)
    groups={}
    for word in words:
        integer(word,'word')
        groups.setdefault(word % banks,set()).add(word)
    return max((len(x) for x in groups.values()),default=0)
