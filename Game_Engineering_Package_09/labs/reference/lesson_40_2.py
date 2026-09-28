"""Lesson 40.2 computational slice.

Apply a signed fixed-point affine transform with explicit rounding and saturation. x and gain are signed encoded integers with bits (2..32) and frac (0..bits-1) fractional bits. Compute nearest-even(x*gain / 2**frac) + bias, then saturate to bits. bias is an encoded signed integer in the same format. Return raw integer outputs; Python arbitrary-precision intermediates avoid overflow.
"""
from __future__ import annotations

from labs.common import integer

def round_even_div(value: int, divisor: int) -> int:
    quotient,remainder=divmod(value,divisor)
    twice=2*remainder
    return quotient+int(twice>divisor or (twice==divisor and quotient%2!=0))

def solve(case: dict) -> dict:
    bits=integer(case['bits'],'bits',2,32); frac=integer(case['frac'],'frac',0,bits-1)
    lo=-(1<<(bits-1)); hi=(1<<(bits-1))-1
    gain=integer(case['gain'],'gain',lo,hi); bias=integer(case['bias'],'bias',lo,hi)
    result=[]; saturated=0
    for x in case['x']:
        integer(x,'x',lo,hi)
        raw=round_even_div(x*gain,1<<frac)+bias
        saturated+=int(raw<lo or raw>hi)
        result.append(max(lo,min(hi,raw)))
    return {'raw':result,'saturated':saturated}
