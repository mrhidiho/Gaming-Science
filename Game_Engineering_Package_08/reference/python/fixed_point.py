"""Explicit signed widths, wrap/saturation, and integer nearest-even rescaling."""
def bounds(width:int)->tuple[int,int]:
    if not isinstance(width,int) or width<1:raise ValueError('positive integer width required')
    return -(1<<(width-1)),(1<<(width-1))-1

def wrap_signed(value:int,width:int)->int:
    bounds(width)
    raw=value&((1<<width)-1)
    return raw-(1<<width) if raw&(1<<(width-1)) else raw

def saturate(value:int,width:int)->int:
    lo,hi=bounds(width);return max(lo,min(hi,value))

def sat_add(a:int,b:int,width:int=16)->int:
    lo,hi=bounds(width)
    if not lo<=a<=hi or not lo<=b<=hi:raise ValueError('operands outside signed width')
    return saturate(a+b,width)

def round_shift_even(value:int,shift:int)->int:
    if not isinstance(shift,int) or shift<0:raise ValueError('nonnegative shift required')
    if shift==0:return value
    denominator=1<<shift
    q,r=divmod(value,denominator) # floor quotient: handles negative values consistently
    if 2*r>denominator or (2*r==denominator and q%2):q+=1
    return q

def fixed_multiply(a:int,b:int,width:int=16,fractional:int=8,policy:str='saturate')->int:
    lo,hi=bounds(width)
    if not 0<=fractional<width or not lo<=a<=hi or not lo<=b<=hi:raise ValueError('invalid fixed-point format/operand')
    value=round_shift_even(a*b,fractional)
    if policy=='saturate':return saturate(value,width)
    if policy=='wrap':return wrap_signed(value,width)
    raise ValueError('policy must be saturate or wrap')
