"""Paired teaching analysis; synthetic demos are not experimental measurements."""
import math, random
from .checks import finite, integer


def quantile(values, p):
    rows=sorted(finite(v,'sample') for v in values)
    if not rows:
        raise ValueError('empty sample')
    p=finite(p,'p',0)
    if p>1:
        raise ValueError('p must be in [0,1]')
    index=(len(rows)-1)*p
    lo=int(math.floor(index));hi=int(math.ceil(index))
    return rows[lo]+(rows[hi]-rows[lo])*(index-lo)


def paired_gmean(baseline, candidate):
    if not baseline or len(baseline)!=len(candidate):
        raise ValueError('nonempty equally sized pairs required')
    logs=[]
    for b,c in zip(baseline,candidate):
        b=finite(b,'baseline',0);c=finite(c,'candidate',0)
        if b==0 or c==0:
            raise ValueError('times must be positive')
        logs.append(math.log(b)-math.log(c))
    return math.exp(math.fsum(logs)/len(logs))


def paired_bootstrap(baseline,candidate,replications=2000,seed=20260928,confidence=0.95):
    point=paired_gmean(baseline,candidate)
    integer(replications,'replications',1)
    confidence=finite(confidence,'confidence',0)
    if not 0<confidence<1:
        raise ValueError('confidence must be strictly between zero and one')
    rng=random.Random(seed);n=len(baseline);sampled=[]
    for _ in range(replications):
        ix=[rng.randrange(n) for _ in range(n)]
        sampled.append(paired_gmean([baseline[i] for i in ix],[candidate[i] for i in ix]))
    tail=(1-confidence)/2
    return dict(speedup=point,lower=quantile(sampled,tail),upper=quantile(sampled,1-tail),
                confidence=confidence,replications=replications,seed=seed,
                unit='matched independent pair',quantile='linear interpolation at (n-1)*p',
                warning='Teaching bootstrap; validity depends on sampling design and independence.')
