from collections import defaultdict, deque, namedtuple
import re

import aoc

ResourcesBase = namedtuple("ResourcesBase", "ore clay obsidian geode")

class Resources(ResourcesBase):
    fields = ResourcesBase._fields

    def __add__(self, other):
        return Resources(*(s+r for s, r in zip(self, other)))

    def __sub__(self, other):
        return Resources(*(s-r for s, r in zip(self, other)))

    @classmethod
    def new(cls, **kwargs):
        d = dict()
        for k in Resources.fields:
            d[k] = 0
        for k, v in kwargs.items():
            d[k] = v
        return cls(**d)


class Blueprint:
    def __init__(self, n, costs):
        self.n = n
        self.costs = costs

    def __repr__(self):
        return f"Blueprint({self.n}, {self.costs})"

    patt_bp = re.compile(r"Blueprint (\d+)")
    patt_cost = re.compile(r".*Each (.+) robot costs (.+)$")

    @classmethod
    def parse(cls, s):
        bp_str, costs_str = s.split(":")
        n = None
        m = cls.patt_bp.match(bp_str)
        if m:
            n = int(m.group(1))
        #print(n)

        costs = dict()
        for cost_str in costs_str.split("."):
            m = cls.patt_cost.match(cost_str)
            if m:
                robot = m.group(1)
                d = dict()
                for c in m.group(2).split(' and '):
                    v, k = c.split()
                    d[k] = int(v)
                costs[robot] = Resources.new(**d)
        return Blueprint(n, costs)

    @classmethod
    def fromfile(cls, filename):
        return [cls.parse(l) for l in aoc.readlines(filename)]

State = namedtuple("State", "t minerals robots")

def canbuild(minerals, cost):
    return min(minerals - cost) >= 0

def runblueprint(bp, totalmin=24):
    queue = deque()
    s1 = State(t=1,
               minerals=Resources.new(),
               robots=Resources.new(ore=1))
    queue.append(s1)

    while queue:
        s = queue.popleft()
        if True:
            print(s)
        if s.t < totalmin:
            nminerals = s.minerals + s.robots

            # don't build anything!
            snext = State(s.t+1, nminerals, s.robots)
            queue.append(snext)

            # or build any kind of robot we can
            for k in Resources.fields:
                cost = bp.costs[k]
                if canbuild(nminerals, cost):
                    sk = State(s.t+1,
                               nminerals - cost,
                               s.robots + Resources.new(**{k: 1}))
                    queue.append(sk)


if __name__ == '__main__':
    test = Blueprint.fromfile("day19/test.txt")
    inp  = Blueprint.fromfile("day19/input.txt")

    for b in test:
        print(b)

    runblueprint(test[0])