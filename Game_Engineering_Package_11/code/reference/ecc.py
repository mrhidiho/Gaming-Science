"""Extended Hamming(8,4), even parity; position 1 is integer bit 0.

Corrects all single-bit codeword faults; detects all doubles. Higher-weight
faults may escape or be miscorrected. Decoder statuses assume this fault model.
"""
from itertools import combinations
from .checks import integer
DATA_POSITIONS = (3,5,6,7)


def parity(value):
    integer(value,'value')
    return value.bit_count() & 1


def encode(payload):
    integer(payload,'payload')
    if payload > 15:
        raise ValueError('payload must fit four bits')
    word = sum(((payload>>i)&1)<<(pos-1) for i,pos in enumerate(DATA_POSITIONS))
    for p in (1,2,4):
        check=0
        for pos in range(1,8):
            if pos & p:
                check ^= (word>>(pos-1))&1
        word |= check<<(p-1)
    return word | (parity(word)<<7)


def decode(word):
    integer(word,'word')
    if word > 255:
        raise ValueError('word must fit eight bits')
    syndrome=0
    for pos in range(1,8):
        if (word>>(pos-1))&1:
            syndrome ^= pos
    odd=parity(word)
    corrected=word
    if syndrome and not odd:
        return dict(status='detected_double', payload=None, corrected_word=None,
                    syndrome=syndrome)
    if odd:
        position=syndrome if syndrome else 8
        corrected ^= 1<<(position-1)
        status='corrected_overall_parity' if position==8 else 'corrected_single'
    else:
        status='no_error_detected'
    payload=sum(((corrected>>(pos-1))&1)<<i for i,pos in enumerate(DATA_POSITIONS))
    return dict(status=status,payload=payload,corrected_word=corrected,syndrome=syndrome)


def fault_campaign():
    counts=dict(clean=0,single=0,double=0)
    for payload in range(16):
        word=encode(payload)
        assert decode(word)['payload']==payload
        counts['clean']+=1
        for bit in range(8):
            assert decode(word^(1<<bit))['payload']==payload
            counts['single']+=1
        for a,b in combinations(range(8),2):
            result=decode(word^(1<<a)^(1<<b))
            assert result['status']=='detected_double' and result['payload'] is None
            counts['double']+=1
    triple=decode(encode(0)^0b111)
    return dict(cases=counts, triple_counterexample=dict(original_payload=0,
        flipped_positions=[1,2,3],result=triple), evidence='exhaustive finite codeword fault model')
