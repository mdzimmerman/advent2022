import argparse
from collections import deque
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

def readfile(filename):
    out = []
    with open(filename, "r") as fh:
        for l in fh:
            out.append(Point(*(int(x) for x in l.strip().split(","))))
    return out

def inrange(p, ranges):
    if p.x < ranges['xmin'] or p.x > ranges['xmax']:
        return False
    elif p.y < ranges['ymin'] or p.y > ranges['ymax']:
        return False
    elif p.z < ranges['zmin'] or p.z > ranges['zmax']:
        return False
    else:
        return True

def main(filename):
    dirs = [
        Point( 1,  0,  0),
        Point(-1,  0,  0),
        Point( 0,  1,  0),
        Point( 0, -1,  0),
        Point( 0,  0,  1),
        Point( 0,  0, -1)]
    points = set(readfile(filename))

    print("-- part 1 ---")
    area = 0
    for p in points:
        for d in dirs:
            np = p + d
            if np not in points:
                area += 1
    print(area)

    ranges = {
        'xmin': min(p.x for p in points)-1,
        'xmax': max(p.x for p in points)+1,
        'ymin': min(p.y for p in points)-1,
        'ymax': max(p.y for p in points)+1,
        'zmin': min(p.z for p in points)-1,
        'zmax': max(p.z for p in points)+1}
    print(ranges)

    p0 = Point(ranges['xmin'], ranges['ymin'], ranges['zmin'])
    queue = deque()
    queue.append(p0)
    visited = set()
    visited.add(p0)

    while queue:
        p = queue.popleft()
        for d in dirs:
            np = p + d
            if inrange(np, ranges) and np not in visited and np not in points:
                queue.append(np)
                visited.add(np)

    area2 = 0
    for p in points:
        for d in dirs:
            np = p + d
            if np in visited:
                area2 += 1
    print(area2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-d', action='store_true')
    args = parser.parse_args()

    main(args.filename)
