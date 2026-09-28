"""Show that a focused test rejects a known wrong implementation."""
from pathlib import Path
import importlib.util
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('damage_reference',ROOT/'labs/reference/lab_04_1.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def double_damage(health,damage):
    return max(0,health-2*damage)

def violates_contract(function):
    try:
        assert function(10,3)==7, 'One event must subtract damage exactly once.'
    except AssertionError:
        return True
    return False

assert not violates_contract(module.apply_damage)
assert violates_contract(double_damage)
print('PASS: reference satisfies the example; seeded double-damage mutant is rejected.')
print('This checks one known mutation. It does not prove all defects are detected.')
