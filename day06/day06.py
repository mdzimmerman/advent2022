def readstring(filename):
    s = ""
    with open(filename, 'r') as fh:
        for l in fh:
            s += l.strip()
    return s

def sliding(xs, size):
    for i in range(len(xs)-size+1):
        yield xs[i:i+size]

def find_marker(s, size):
    for i, w in enumerate(sliding(s, size)):
        #print(w)
        if len(set(w)) == size:
            return i+size

if __name__ == '__main__':
    test = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
    print(find_marker(test, 4))
    print(find_marker(test, 14))

    inp = readstring("input.txt")
    print(find_marker(inp, 4))
    print(find_marker(inp, 14))