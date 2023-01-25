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


def ymax(cs):
    if cs:
        return max(c.y for c in cs)
    else:
        return -1


def move(s, dx, dy):
    return {Cell(c.x + dx, c.y + dy) for c in s}


def printset(s, r=None):
    if r is None:
        r = calcranges(s)
    #print(r)
    for y in range(r.ymax, r.ymin - 1, -1):
        for x in range(r.xmin, r.xmax + 1):
            if Cell(x, y) in s:
                print("#", end="")
            else:
                print(".", end="")
        print()


def part1(wind, npieces=1, debug=0):
    stopped = set()
    i = 0
    for j in range(npieces):
        shape0 = SHAPES[j % len(SHAPES)]
        shape = move(shape0, 2, ymax(stopped)+4)
        if debug >= 2:
            print()
            printset(stopped | shape, Ranges(0, 6, 0, ymax(shape)))

        inmotion = True
        while inmotion:
            # left or right
            dir = wind[i % len(wind)]
            canmove = True
            if dir == "<":
                for s in shape:
                    sn = Cell(s.x-1, s.y)
                    if sn.x < 0 or sn in stopped:
                        canmove = False
                if canmove:
                    shape = move(shape, -1, 0)
            elif dir == '>':
                for s in shape:
                    sn = Cell(s.x+1, s.y)
                    if sn.x > 6 or sn in stopped:
                        canmove = False
                if canmove:
                    shape = move(shape, 1, 0)
            if debug >= 2:
                print(dir)
                printset(stopped | shape, Ranges(0, 6, 0, ymax(shape)))
            i += 1

            # down
            for s in shape:
                sn = Cell(s.x, s.y-1)
                if sn.y < 0 or sn in stopped:
                    inmotion = False
            if inmotion:
                shape = move(shape, 0, -1)
            if debug >= 2:
                print("v")
                printset(stopped | shape, Ranges(0, 6, 0, ymax(shape)))

        stopped.update(shape)

    if debug >= 1:
        print()
        printset(stopped, Ranges(0, 6, 0, ymax(stopped)))

    return ymax(stopped)+1

def main():
    print("-- shapes --")

    for s in SHAPES:
        print()
        print(s)
        printset(s)

    print()
    print("-- part 1 --")
    print("test")
    test = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    #part1(test, 2)
    print(part1(test, npieces=5, debug=1))

    print()
    print(part1(test, npieces=2022, debug=0))

if __name__ == '__main__':
    main()
