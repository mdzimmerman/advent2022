import re
from typing import List
from dataclasses import dataclass, field

class File:
    def __init__(self, name, fsize=0):
        self.name = name
        self.fsize = fsize
        
    def __repr__(self):
        return f"File({self.name} {self.fsize})"
    
    def print_tree(self, indent):
        print("  "*indent+str(self))
        
    def totalsize(self):
        return self.fsize
        
class Dir(File):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.files = dict()

    def __repr__(self):
        return f"Dir({self.name})"
        
    def add_file(self, file):
        self.files[file.name] = file
        if isinstance(file, Dir):
            file.parent = self
            
    def print_tree(self, indent=0):
        #super().print_tree(indent)
        print("  "*indent+str(self)+" "+str(self.totalsize()))
        for name, file in self.files.items():
            file.print_tree(indent+1)
            
    def totalsize(self):
        return sum(file.totalsize() for name, file in self.files.items())
    
    def find_dir_totalsize(self, f):
        dirs=[]
        if f(self.totalsize()):
            dirs.append(self)
        for name, file in self.files.items():
            #print(file.name)
            if isinstance(file, Dir):
                dirs.extend(file.find_dir_totalsize(f))
        return dirs
        
def parse_output(filename):
    root = None
    with open(filename, "r") as fh:
        curr = None
        inls = False
        for l in fh:
            c = l.strip().split()
            if c[0] == "$":
                if c[1] == "cd":
                    dirname = c[2]
                    if dirname == "/":
                        curr = Dir("/")
                        root = curr
                    elif dirname == "..":
                        curr = curr.parent
                    else:
                        curr = curr.files[dirname]
                elif c[1] == "ls":
                    pass
            else:
                if c[0] == "dir":
                    curr.add_file(Dir(c[1]))
                else:
                    curr.add_file(File(c[1], int(c[0])))
    return root

if __name__ == '__main__':
    test = parse_output("test.txt")
    test.print_tree()
    le100k = lambda x: x <= 100000
    print(sum([x.totalsize() for x in test.find_dir_totalsize(le100k)]))
    
    inp = parse_output("input.txt")
    print(sum([x.totalsize() for x in inp.find_dir_totalsize(le100k)]))
    
    currsize = inp.totalsize()
    print(currsize)
    totalsize = 70000000
    free = totalsize - currsize
    print(free)
    needed = 30000000 - free
    print(needed)
    
    sizes = sorted([x.totalsize() for x
                    in inp.find_dir_totalsize(lambda x: x >= needed)])
    print(sizes[:3])