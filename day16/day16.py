import argparse
from collections import namedtuple
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

Step = namedtuple("Step", "valve minute openvalves")

class ValveSeq:
    def __init__(self, valvelist):
        self.vlist = valvelist
        self.vindex = {}
        for v in self.vlist:
            self.vindex[v.name] = v
        self.effectivevalves = len(list(filter(lambda x: x.flowrate > 0, self.vlist)))
            
    def get(self, name):
        return self.vindex[name]
    
    def state(self, step):
        return f"{step.valve} {str(step.openvalves)}"
    
    def totalpressure(self, openvalves):
        return sum(self.vindex[k].flowrate * (30 - v) for k, v in openvalves.items())
    
    def traverse(self, startvalve, debug=False):
        nsteps = 1
        startstep = Step(startvalve, 1, {})
        queue = []
        queue.append(startstep)
        visited = set()
        visited.add(self.state(startstep))
        
        maxstep = None
        maxpressure = 0
            
        while queue:
            s = queue.pop(0)
            if s.minute > 30:
                break
            nsteps += 1
            if nsteps % 1000 == 0:
                print(nsteps)
            pressure = self.totalpressure(s.openvalves)
            if debug:
                print(f"{pressure:5d} {s}")
            if pressure > maxpressure:
                maxpressure = pressure
                maxstep = s
            neighbors = []
            if s.valve not in s.openvalves and self.get(s.valve).flowrate > 0:
                # don't bother opening valves that don't release pressure
                neighbors.append(Step(s.valve, s.minute+1, {**s.openvalves, s.valve: s.minute}))
            if len(s.openvalves) < self.effectivevalves:
                # only keep going down tunnels if there are still valves to be opened
                for nvalve in self.get(s.valve).tunnels:
                    neighbors.append(Step(nvalve, s.minute+1, s.openvalves))
            for ns in neighbors:
                nstate = self.state(ns)
                if nstate not in visited:
                    visited.add(nstate)
                    queue.append(ns)
        print(nsteps)
        return maxpressure, maxstep
    
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
    for v in inp.vlist:
        print(v)
    print()
    print(inp.traverse("AA"), debug=args.d)
    
    