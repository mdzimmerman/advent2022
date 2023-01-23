import argparse
from collections import deque, namedtuple
from dataclasses import dataclass
import re

@dataclass
class Valve:
    name: str
    flowrate: int
    tunnels: list
    
    pat = re.compile(r"Valve (.+) has flow rate=(\d+); tunnels? leads? to valves? (.+)")
    
    @classmethod
    def parse(cls, s):
        m = cls.pat.match(s)
        if m:
            valve = m.group(1)
            flowrate = int(m.group(2))
            tunnels = m.group(3).split(", ")
            return cls(valve, flowrate, tunnels)

Step = namedtuple("Step", "valve minute openvalves totalpressure")

class ValveSeq:
    def __init__(self, valvelist):
        self.vlist = valvelist
        self.vindex = {}
        self.bitm = {}
        self.dists = self._calc_dists()
        for i, v in enumerate(self.vlist):
            self.vindex[v.name] = v
            self.bitm[v.name] = 1 << i
        self.goodvalves = list(v.name for v in filter(lambda x: x.flowrate > 0, self.vlist))
        self.ngoodvalves = len(self.goodvalves)
    
    def _calc_dists(self):
        dist = {}
        vnames = [v.name for v in self.vlist]
        for v in self.vlist:
            a = v.name
            for b in vnames:
                if a == b:
                    dist[(a,b)] = 0
                elif b in v.tunnels:
                    dist[(a,b)] = 1
                else:
                    dist[(a,b)] = 1000  # "Inf"
        for k in vnames:
            for i in vnames:
                for j in vnames:
                    if dist[(i,j)] > dist[(i,k)] + dist[(k,j)]:
                        dist[(i,j)] = dist[(i,k)] + dist[(k,j)]
        return dist
   
    def dist(self, a, b):
        return self.dists[(a, b)]

    def get(self, name):
        return self.vindex[name]
    
    def state(self, step):
        return f"{step.valve} {str(step.openvalves)}"
    
    def totalpressure(self, openvalves):
        return sum(self.vindex[k].flowrate * (30 - v) for k, v in openvalves.items())
    
    def traverse(self, startvalve, totalminutes, debug=False):
        nsteps = 1
        startstep = Step(startvalve, 1, {}, 0)
        queue = deque()
        queue.append(startstep)
        visited = set()
        visited.add(self.state(startstep))
        
        maxstep = None
        maxpressure = 0
        solutions = dict()

        while queue:
            s = queue.popleft()
            nsteps += 1
            if nsteps % 10000 == 0:
                dig = (nsteps // 10000) % 10
                print(dig, end="")
            pressure = s.totalpressure
            if debug:
                print(f"{pressure:5d} {s}")
            bitmask = sum(self.bitm[n] for n in s.openvalves.keys())
            if bitmask not in solutions or solutions[bitmask].totalpressure < s.totalpressure:
                solutions[bitmask] = s
            neighbors = []
            if s.valve not in s.openvalves:
                # don't bother opening valves that don't release pressure
                pressure = (totalminutes - s.minute) * self.get(s.valve).flowrate
                neighbors.append(Step(s.valve, s.minute+1, {**s.openvalves, s.valve: s.minute}, s.totalpressure + pressure))
            if len(s.openvalves) < self.ngoodvalves:
                # only keep going down tunnels if there are still valves to be opened
                for gv in self.goodvalves:
                    d = self.dist(s.valve, gv)
                    if gv != s.valve and gv not in s.openvalves and s.minute+d <= totalminutes:
                        neighbors.append(Step(gv, s.minute+d, s.openvalves, s.totalpressure))
            for ns in neighbors:
                nstate = self.state(ns)
                if nstate not in visited:
                    visited.add(nstate)
                    queue.append(ns)

        print(f"total steps={nsteps}")
        print(len(solutions))
        return solutions
    
    @classmethod
    def readfile(cls, filename):
        out = []
        with open(filename, "r") as fh:
            for s in fh:
                out.append(Valve.parse(s.strip()))
        return cls(out)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', action='store_true')
    args = parser.parse_args()
    
    inp = ValveSeq.readfile(args.filename)
    print("-- input data --")
    for v in inp.vlist:
        print(v)
    indices = {v.name: 1 << i for i, v in enumerate(inp.vlist)}
    print(indices)
    print()

    print("-- part 1 --")
    sol1 = inp.traverse("AA", 30, debug=args.d)
    #for k, v in sol1.items():
    #    print(k, v)
    print(max(v.totalpressure for k, v in sol1.items()))

    print("-- part 2 --")
    sol2 = inp.traverse("AA", 26)
    print(max(sol2[k1].totalpressure + sol2[k2].totalpressure
              for k1 in sol2.keys()
              for k2 in sol2.keys()
              if not k1 & k2))
