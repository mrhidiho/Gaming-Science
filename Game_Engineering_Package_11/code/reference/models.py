"""Analytical arithmetic models; all physical quantities require stated units."""
import math
from .checks import finite, integer


def pareto_front(points):
    """Return indices of strictly non-dominated points; all objectives minimize.
    Duplicate points remain non-dominated. Empty input returns an empty list.
    """
    rows = [tuple(finite(x,'objective') for x in row) for row in points]
    if not rows:
        return []
    if not rows[0] or any(len(r) != len(rows[0]) for r in rows):
        raise ValueError('objective vectors must have equal positive dimension')
    return [i for i,p in enumerate(rows) if not any(
        j != i and all(a <= b for a,b in zip(q,p)) and any(a < b for a,b in zip(q,p))
        for j,q in enumerate(rows))]


def setup_slack(period, skew, qmax, dmax, setup, uncertainty):
    p=finite(period,'period',0); k=finite(skew,'skew')
    q=finite(qmax,'qmax',0); d=finite(dmax,'dmax',0)
    s=finite(setup,'setup',0); u=finite(uncertainty,'uncertainty',0)
    return p+k-u-s-q-d


def hold_slack(skew, qmin, dmin, hold, uncertainty):
    k=finite(skew,'skew'); q=finite(qmin,'qmin',0); d=finite(dmin,'dmin',0)
    h=finite(hold,'hold',0); u=finite(uncertainty,'uncertainty',0)
    return q+d-k-h-u


def inverter_chain(load_ratio, stages, parasitic=1.0):
    h=finite(load_ratio,'load_ratio',0)
    if h == 0:
        raise ValueError('load ratio must be positive')
    integer(stages,'stages',1); p=finite(parasitic,'parasitic',0)
    effort=h**(1/stages)
    return dict(effort=effort, delay=stages*(effort+p),
                sizes=[effort**i for i in range(stages)],
                inverting=bool(stages%2), units='normalized')


def dynamic_power(activity, capacitance_f, voltage_v, frequency_hz):
    a=finite(activity,'activity',0); c=finite(capacitance_f,'capacitance_f',0)
    v=finite(voltage_v,'voltage_v',0); f=finite(frequency_hz,'frequency_hz',0)
    # Activity counts charging events/cycle and may exceed one with glitches.
    return a*c*v*v*f


def energy_per_item(power_w, items_per_second):
    p=finite(power_w,'power_w',0); rate=finite(items_per_second,'items_per_second',0)
    if rate == 0:
        raise ValueError('throughput must be positive')
    return p/rate
