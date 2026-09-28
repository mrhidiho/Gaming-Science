"""Educational contract exercise. Python 3.11+; standard library only."""
import copy
import hashlib
import json
import math

def integer(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value

def finite(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return float(value)

def apply_edit(state, undo, redo, entity_id, new_position):
    """Single-owner position command; invalid inputs never change world or history."""
    if not isinstance(state,dict) or not isinstance(undo,list) or not isinstance(redo,list): raise ValueError('invalid command containers')
    if entity_id not in state: raise ValueError('unknown entity')
    if not isinstance(new_position,(list,tuple)) or len(new_position)!=3: raise ValueError('position requires three values')
    after=[finite(x,'position') for x in new_position]
    if any(abs(x)>1e6 for x in after): raise ValueError('position out of bounds')
    before=copy.deepcopy(state[entity_id])
    if before==after: return False
    command={'id':entity_id,'before':before,'after':after[:]}
    state[entity_id]=after; undo.append(command); redo.clear()
    return True
