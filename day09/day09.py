from collections import namedtuple
import math

Point = namedtuple("Point", "x y")

def printset(d, xmin, xmax, ymin, ymax):
    for j in range(ymin, ymax+1):
        for i in range(xmin, xmax+1):
            p = Point(i, j)
            if p in d:
                print("#", end="")
            else:
                print(".", end="")
        print()

def movetail(h, t):
    if abs(h.x-t.x) <= 1 and abs(h.y-t.y) <= 1:
        return t
    tx = t.x
    if h.x < t.x:
        tx = t.x - 1
    elif h.x > t.x:
        tx = t.x + 1
    ty = t.y 
    if h.y < t.y:
        ty = t.y - 1
    elif h.y > t.y:
        ty = t.y + 1
    return Point(tx, ty)    
        
def moverope(filename, ropelength=2):
    rope = [Point(0, 0)] * ropelength
    print(rope)
    tailall = set()
    tailall.add(rope[-1])
    with open(filename, "r") as fh:
        for l in fh:
            direct, n = l.split()
            #print(direct, n)
            for _ in range(int(n)):
                if direct == 'U':
                    rope[0] = Point(rope[0].x, rope[0].y-1)
                elif direct == 'R':
                    rope[0] = Point(rope[0].x+1, rope[0].y)
                elif direct == 'D':
                    rope[0] = Point(rope[0].x, rope[0].y+1)
                elif direct == 'L':
                    rope[0] = Point(rope[0].x-1, rope[0].y)
                for i in range(1, ropelength):
                    rope[i] = movetail(rope[i-1], rope[i])
                tailall.add(rope[-1])
    return tailall
            
if __name__ == "__main__":
    testall = moverope("test.txt")
    printset(testall, 0, 5, -5, 0)
    print(len(testall))
    
    inpall = moverope("input.txt")
    print(len(inpall))
    
    inpall2 = moverope("input.txt", ropelength=10)
    print(len(inpall2))