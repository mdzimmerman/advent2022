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


def canmove(dir, shape, stopped):
    if dir == '<':
        for s in shape:
            sn = Cell(s.x-1, s.y)
            if sn.x < 0 or sn in stopped:
                return False, shape
        return True, move(shape, -1, 0)
    elif dir == '>':
        for s in shape:
            sn = Cell(s.x+1, s.y)
            if sn.x > 6 or sn in stopped:
                return False, shape
        return True, move(shape, 1, 0)
    elif dir == 'v':
        for s in shape:
            sn = Cell(s.x, s.y-1)
            if sn.y < 0 or sn in stopped:
                return False, shape
        return True, move(shape, 0, -1)


def prune(stopped, buffer=50):
    y1 = ymax(stopped)
    y0 = y1 - buffer
    return set(filter(lambda c: c.y >= y0, stopped))


def simulate(wind, npieces=1, debug=0):
    stopped = set()
    i = 0
    for j in range(npieces):
        #if j % 1000 == 0:
        #    print(f"j={j}")
        shape0 = SHAPES[j % len(SHAPES)]
        shape = move(shape0, 2, ymax(stopped)+4)
        if debug >= 2:
            print()
            printset(stopped | shape, Ranges(0, 6, 0, ymax(shape)))

        inmotion = True
        while inmotion:
            # left or right
            dir = wind[i % len(wind)]
            _, shape = canmove(dir, shape, stopped)
            if debug >= 2:
                print(dir)
                printset(stopped | shape, Ranges(0, 6, 0, ymax(shape)))
            i += 1

            # down
            inmotion, shape = canmove('v', shape, stopped)
            if debug >= 2:
                print("v")
                printset(stopped | shape, Ranges(0, 6, 0, ymax(shape)))

        stopped = prune(stopped | shape, buffer=30)

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
    print("- test - ")
    test = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    #part1(test, 2)
    print("test with 5 blocks")
    print(simulate(test, npieces=5, debug=1))

    print()
    print(simulate(test, npieces=2022, debug=0))

    print("- input -")
    inp = ""
    with open("day17/input.txt", "r") as fh:
        for l in fh:
            inp += l.strip()
    #print(inp)
    print(simulate(inp, npieces=2022))

    print("-- part 2 --")
    print("- test -")
    # blergh too much to simulate
    #print(simulate(test, npieces=1000000000000))
    print(f"test length={len(test)}")
    print(f"inp length={len(inp)}")


if __name__ == '__main__':
    main()
