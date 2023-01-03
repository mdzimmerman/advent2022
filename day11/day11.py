import argparse
from functools import reduce
import re
import sys

if ".." not in sys.path:
    sys.path.append("..")
import aoc

def read_pattern(pat, s):
    m = pat.match(s)
    if m:
        return m.group(1)
    else:
        return None

class Monkey:
    pmonkey = re.compile(r"Monkey (\d):")
    pstart  = re.compile(r"  Starting items: (.+)")
    pexpr   = re.compile(r"  Operation: new = (.+)")
    ptesti  = re.compile(r"  Test: divisible by (\d+)")
    ptrue   = re.compile(r"    If true: throw to monkey (\d)")
    pfalse  = re.compile(r"    If false: throw to monkey (\d)")
    
    def __init__(self, n, start, expr, testi, ntrue, nfalse):
        self.n = n
        self.start = start
        self.expr = expr
        self.testi = testi
        self.ntrue = ntrue
        self.nfalse = nfalse
        
    def __repr__(self):
        return f"Monkey(n={self.n} start={self.start} expr={self.expr} testi={self.testi} ntrue={self.ntrue} nfalse={self.nfalse})"

    def calcworry(self, x):
        return eval(self.expr, {}, {"old": x})
    
    def throwto(self, x):
        if x % self.testi == 0:
            return self.ntrue
        else:
            return self.nfalse
        
    @classmethod
    def fromtext(cls, xs):
        n      = int(read_pattern(cls.pmonkey, xs[0]))
        start  = [int(x) for x in read_pattern(cls.pstart, xs[1]).split(", ")]
        expr   = read_pattern(cls.pexpr, xs[2])
        testi  = int(read_pattern(cls.ptesti, xs[3]))
        ntrue  = int(read_pattern(cls.ptrue, xs[4]))
        nfalse = int(read_pattern(cls.pfalse, xs[5]))
        return Monkey(n, start, expr, testi, ntrue, nfalse)

def print_inventory(inventory):
    for i in range(len(inventory)):
        inv = ", ".join(str(x) for x in inventory[i])
        print(f"{i}: {inv}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    
    args = parser.parse_args()
    monkeys = []
    for xs in aoc.splitlist(aoc.readlines(args.filename), ""):
        monkeys.append(Monkey.fromtext(xs))
    #print(monkeys[0])
    
    inventory = []
    inspectcount = []
    for i, m in enumerate(monkeys):
        inventory.append(m.start[:])
        inspectcount.append(0)
    print_inventory(inventory)
    
    supermod = reduce(lambda x, y: x * y, [m.testi for m in monkeys])
    print(supermod)
    rounds = 10000
    for _ in range(rounds):
        for i, m in enumerate(monkeys):
            for item in inventory[i]:
                inspectcount[i] += 1
                newitem = m.calcworry(item) % supermod
                dest = m.throwto(newitem)
                inventory[dest].append(newitem)
            inventory[i][:] = []
    
    print_inventory(inventory)
    print(inspectcount)
    countmax = sorted(inspectcount)[-2:]
    print(countmax[0] * countmax[1])