from collections import namedtuple
import copy
import re
import sys

if ".." not in sys.path:
    sys.path.append("..")

import aoc

Instr = namedtuple("Instr", "n src dst")

def window(xs, size):
    for i in range(0, len(xs), size):
        yield xs[i:i+size]

class InputData:
    def __init__(self, filename):
        self.filename = filename
        lines = aoc.readlines(filename)
        stacklines, instrlines = aoc.splitlist(lines, "")
        self.stack = self._parse_stack(stacklines)
        self.instr = self._parse_instr(instrlines)
    
    patt_stack = re.compile(r"\[(.)\]")
    patt_instr = re.compile(r"move (\d+) from (\d+) to (\d+)")
    
    def _parse_stack(self, xs):
        stack = dict()
        for s in window(xs[-1], 4):
            i = int(s.strip())
            stack[i] = list()
        for x in reversed(xs[:-1]):
            for j, s in enumerate(window(x, 4)):
                m = __class__.patt_stack.match(s)
                if m:
                    stack[j+1].append(m.group(1))
        return stack
        
    def _parse_instr(self, xs):
        instr = list()
        for x in xs:
            m = __class__.patt_instr.match(x)
            if m:
                instr.append(Instr(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        return instr
    
    def print_stack(self, s=None):
        if s is None:
            s = self.stack
        for k, v in s.items():
            print(f"{k}: {v}")
            
    def print_instr(self):
        for x in self.instr:
            print(x)

    def checksum(self, s=None):
        if s is None:
            s = self.stack
        return "".join(v[-1] for k,v in s.items())
 
    def rearrange(self, debug=0):
        stack = copy.deepcopy(self.stack)
        for ins in self.instr:
            if debug >= 2: 
                self.print_stack(stack)
                print()
            for _ in range(ins.n):
                stack[ins.dst].append(stack[ins.src].pop())
        if debug >= 1: self.print_stack(stack)
        return self.checksum(stack)
    
    def rearrange2(self, debug=0):
        stack = copy.deepcopy(self.stack)
        for ins in self.instr:
            if debug >= 2: 
                self.print_stack(stack)
                print()
            buff = stack[ins.src][-ins.n:]
            stack[ins.src][:] = stack[ins.src][:-ins.n]
            stack[ins.dst].extend(buff)
        if debug >= 1: self.print_stack(stack)
        return self.checksum(stack)
        
if __name__ == '__main__':
    print("-- test --")
    test = InputData('test.txt')
    test.print_stack()
    test.print_instr()
    print("-- test part #1 --")
    print(test.rearrange(debug=2))
    print("-- test part #2 --")
    print(test.rearrange2(debug=2))
    
    print("-- input --")
    inp = InputData('input.txt')
    inp.print_stack()
    print("-- input part #1 --")
    print(inp.rearrange(debug=1))
    print("-- input part #2 --")
    print(inp.rearrange2(debug=1))