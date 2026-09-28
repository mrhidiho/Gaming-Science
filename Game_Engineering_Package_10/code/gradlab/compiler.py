"""Small compiler laboratory: CFG execution, fixed points and a pure u32 DSL.
The interpreter is restricted but is NOT an OS sandbox for hostile processes.
No eval/exec, machine-code JIT or arbitrary file/network effect is used.
"""
from __future__ import annotations
import hashlib
import json

MASK = (1 << 32)-1


def live_variables(blocks: dict) -> dict:
    """Backward may-liveness for use/def/succ sets; phi uses belong on edges.
    This small schema is non-SSA: use it to derive liveness before adding phi edges.
    """
    ins = {k: set() for k in blocks}; outs = {k: set() for k in blocks}
    for b in blocks.values():
        if any(s not in blocks for s in b['succ']): raise ValueError("missing successor")
    iterations = 0
    while True:
        changed = False; iterations += 1
        for name in reversed(list(blocks)):
            b = blocks[name]
            out = set().union(*(ins[s] for s in b['succ']))
            new = set(b['use']) | (out-set(b['defs']))
            if new != ins[name] or out != outs[name]: changed = True
            ins[name], outs[name] = new, out
        if not changed: break
    return dict(live_in={k: sorted(v) for k, v in ins.items()},
                live_out={k: sorted(v) for k, v in outs.items()}, iterations=iterations)


def run_cfg(blocks: dict, inputs: dict, fuel=1000):
    """SSA-shaped toy CFG. phi values chosen simultaneously on block entry.
    Runtime checks don't replace a dominance/type verifier (a learner extension).
    code entries: [dest, op, operands]; terminator: ret/br/jmp.
    Operands are integer literals or variable names. Integer semantics: u32 wrap.
    """
    env = {k: int(v)&MASK for k, v in inputs.items()}; here, prev = 'entry', None
    def get(v): return env[v] if isinstance(v, str) else int(v)&MASK
    while fuel > 0:
        fuel -= 1
        if here not in blocks: raise ValueError("unknown block")
        b = blocks[here]
        values = {name: get(incoming[prev]) for name, incoming in b.get('phi', {}).items()}
        env.update(values)
        for dest, op, args in b.get('code', []):
            vals = [get(v) for v in args]
            if op == 'add': result = vals[0]+vals[1]
            elif op == 'mul': result = vals[0]*vals[1]
            elif op == 'lt': result = int(vals[0] < vals[1])
            elif op == 'copy': result = vals[0]
            else: raise ValueError("unsupported IR operation")
            env[dest] = result&MASK
        term = b['term']
        if term[0] == 'ret': return get(term[1])
        nxt = term[1] if term[0] == 'jmp' else term[2] if get(term[1]) else term[3]
        prev, here = here, nxt
    raise RuntimeError("CFG fuel exhausted")


def validate_expr(tree, variables: set[str], max_nodes=128, max_depth=32):
    """Tuple/list DSL: ('const',u32), ('var',name), ('add'|'mul',a,b)."""
    count = 0
    def visit(t, depth):
        nonlocal count
        count += 1
        if count > max_nodes or depth > max_depth: raise ValueError("expression exceeds budget")
        if not isinstance(t, (list, tuple)) or not t: raise ValueError("invalid node")
        op = t[0]
        if op == 'const' and len(t) == 2:
            if type(t[1]) is not int or not 0 <= t[1] <= MASK: raise ValueError("u32 constant required")
        elif op == 'var' and len(t) == 2:
            if not isinstance(t[1], str) or t[1] not in variables: raise ValueError("unknown variable")
        elif op in ('add', 'mul') and len(t) == 3:
            visit(t[1], depth+1); visit(t[2], depth+1)
        else: raise ValueError("unsupported node/effect")
    visit(tree, 0)
    return count


def interpret(tree, env):
    validate_expr(tree, set(env))
    if any(type(v) is not int or not 0 <= v <= MASK for v in env.values()):
        raise ValueError("u32 inputs required")
    def ev(t):
        if t[0] == 'const': return t[1]
        if t[0] == 'var': return env[t[1]]
        a, b = ev(t[1]), ev(t[2])
        return (a+b if t[0] == 'add' else a*b)&MASK
    return ev(tree)


def fold(tree, variables: set[str]):
    validate_expr(tree, variables)
    def go(t):
        op = t[0]
        if op in ('var', 'const'): return tuple(t)
        a, b = go(t[1]), go(t[2])
        if a[0] == b[0] == 'const': return ('const', interpret((op, a, b), {}))
        if op == 'add' and b == ('const', 0): return a
        if op == 'add' and a == ('const', 0): return b
        if op == 'mul' and b == ('const', 1): return a
        if op == 'mul' and a == ('const', 1): return b
        return (op, a, b)
    return go(tree)


def cache_key(tree, *, target, compiler_version, flags, abi="u32-v1"):
    # Call validate_expr before cache insertion in an actual host application.
    record = dict(tree=tree, target=target, compiler=compiler_version, flags=flags,
                  abi=abi, schema=1)
    return hashlib.sha256(json.dumps(record, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def ranges_overlap(a_start: int, a_size: int, b_start: int, b_size: int) -> bool:
    """Half-open integer byte ranges; real native pointer provenance is separate."""
    if min(a_start, a_size, b_start, b_size) < 0: raise ValueError("negative address/size")
    return a_size > 0 and b_size > 0 and a_start < b_start+b_size and b_start < a_start+a_size


def generate_cpp(tree, variables: set[str]) -> str:
    """Emit a pure uint32_t expression for inspection, NOT compile or run it."""
    validate_expr(tree, variables)
    if any(not name.isidentifier() or not name.isascii() for name in variables):
        raise ValueError("invalid identifier")
    # Prefix all external names, so keywords cannot become source code.
    names = {v: f'arg_{i}' for i, v in enumerate(sorted(variables))}
    def go(t):
        if t[0] == 'const': return f"std::uint32_t{{{t[1]}u}}"
        if t[0] == 'var': return names[t[1]]
        operator = '+' if t[0] == 'add' else '*'
        return f'({go(t[1])} {operator} {go(t[2])})'
    args = ', '.join(f'std::uint32_t {names[v]}' for v in sorted(variables))
    return '#include <cstdint>\nstd::uint32_t kernel('+args+') { return '+go(tree)+'; }\n'
