from collections import namedtuple

Cell = namedtuple("Cell", "x y")

SHAPES = [
    {Cell(0, 0), Cell(1, 0), Cell(2, 0), Cell(3, 0)},
    {Cell(1, 0), Cell(0, 1), Cell(1, 1), Cell(2, 1), Cell(1, 2)},
    {Cell(0, 0), Cell(1, 0), Cell(2, 0), Cell(2, 1), Cell(2, 2)},
    {Cell(0, 0), Cell(0, 1), Cell(0, 2), Cell(0, 3)},
    {Cell(0, 0), Cell(1, 0), Cell(0, 1), Cell(1, 1)}
]

Ranges = namedtuple("Ranges", "xmin xmax ymin ymax")


def calcranges(cs):
    return Ranges(
        min(c.x for c in cs),
        max(c.x for c in cs),
        min(c.y for c in cs),
        max(c.y for c in cs))


def move(s, dx, dy):
    return {Cell(c.x + dx, c.y + dy) for c in s}


def printset(s, r=None):
    if r is None:
        r = calcranges(s)
    print(r)
    for y in range(r.ymax, r.ymin - 1, -1):
        for x in range(r.xmin, r.xmax + 1):
            if Cell(x, y) in s:
                print("#", end="")
            else:
                print(".", end="")
        print()


def main():
    print("-- part 1 --")

    for s in SHAPES:
        print()
        sm = move(s, 2, 3)
        print(sm)
        r = calcranges(sm)
        printset(sm, Ranges(0, 6, 0, r.ymax))


if __name__ == '__main__':
    main()
