"""Atomic two-core, one-line MSI model. No transient messages or weak memory."""
from dataclasses import dataclass, field
from .checks import integer


@dataclass
class MSI:
    memory: int = 0
    state: list = field(default_factory=lambda: ['I', 'I'])
    value: list = field(default_factory=lambda: [None, None])
    latest: int = 0

    def check(self):
        assert all(x in {'I','S','M'} for x in self.state)
        owners = [i for i,s in enumerate(self.state) if s == 'M']
        assert len(owners) <= 1, 'multiple owners'
        if owners:
            i = owners[0]
            assert self.state[1-i] == 'I', 'owner coexists with reader'
            assert self.value[i] == self.latest, 'owner has stale value'
        else:
            assert self.memory == self.latest, 'memory stale without owner'
        for i,s in enumerate(self.state):
            if s == 'S':
                assert self.value[i] == self.memory == self.latest

    def request(self, core, op, data=0):
        integer(core, 'core')
        if core not in (0,1) or op not in ('R','W'):
            raise ValueError('core must be 0/1 and op R/W')
        if isinstance(data,bool) or not isinstance(data,int):
            raise ValueError('data must be an integer')
        other = 1-core
        if op == 'R':
            if self.state[core] == 'I':
                if self.state[other] == 'M':
                    self.memory = self.value[other]
                    self.state[other] = 'S'
                self.state[core] = 'S'
                self.value[core] = self.memory
            result = self.value[core]
        else:
            self.state[other], self.value[other] = 'I', None
            self.state[core], self.value[core] = 'M', data
            self.latest = data
            result = None
        self.check()
        return result
