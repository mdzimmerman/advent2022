from collections import namedtuple
import sys

import numpy as np

def readgrid(filename):
    out = []
    with open(filename, "r") as fh:
        for l in fh:
            out.append([c for c in l.strip()])
    return np.array(out)

Point = namedtuple("Point", "x y")



if __name__ == '__main__':
    test = readgrid("test.txt")
    print(test)