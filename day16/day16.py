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
            
    def get(self, name):
        return self.vindex[name]
    
    def state(self, step):
        return f"{step.valve} {str(step.openvalves)}"
    
    def totalpressure(self, openvalves):
        return sum(self.vindex[k].flowrate * (30 - v) for k, v in openvalves.items())
    
    def traverse(self, startvalve, debug=False):
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
                return maxpressure, maxstep
            pressure = self.totalpressure(s.openvalves)
            if debug:
                if "DD" in s.openvalves and s.openvalves["DD"] == 2 and "BB" in s.openvalves and s.openvalves["BB"] == 5:
                    print(f"{pressure:5d} {s} {self.state(s)}")
            if pressure > maxpressure:
                maxpressure = pressure
                maxstep = s
            neighbors = []
            if s.valve not in s.openvalves and self.get(s.valve).flowrate > 0:
                # don't bother opening valves that don't release pressure
                neighbors.append(Step(s.valve, s.minute+1, {**s.openvalves, s.valve: s.minute}))
            for nvalve in self.get(s.valve).tunnels:
                neighbors.append(Step(nvalve, s.minute+1, s.openvalves))
            for ns in neighbors:
                nstate = self.state(ns)
                if nstate not in visited:
                    visited.add(nstate)
                    queue.append(ns)
    
        return maxpressure, maxstep
    
    @classmethod
    def readfile(cls, filename):
        out = []
        with open(filename, "r") as fh:
            for s in fh:
                out.append(Valve.parse(s.strip()))
        return cls(out)
    
def main(filename, debug=False):
    test = ValveSeq.readfile("test.txt")
    for v in test.vlist:
        print(v)
    print()
    return test.traverse("AA", debug=debug)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', action='store_true')
    parser.parse_args()
    main()
    
    