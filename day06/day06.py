def readstring(filename):
    s = ""
    with open(filename, 'r') as fh:
        for l in fh:
            s += l.strip()
    return s
    
if __name__ == '__main__':
    print(readstring())