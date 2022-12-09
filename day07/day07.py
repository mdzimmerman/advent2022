import re
from typing import List
from dataclasses import dataclass, field

class Node:
    def size(self):
        return None

@dataclass
class File(Node):
    name: str
    fsize: int
    
    pattern = re.compile(r"(\d+) (.+)")
    
    @classmethod
    def parse(cls, s):
        m = cls.pattern.match(s)
        if m:
            return cls(m.group(2), int(m.group(1)))
        else:
            return None

@dataclass
class Dir(Node):
    name: str
    parent: Node = None
    contents: List[Node] = field(default_factory=list)
    
    def add_node(self, s):
        
    
    pattern = re.compile(r"dir (.+)")
    
    @classmethod
    def parse(cls, s):
        m = cls.pattern.match(s)
        if m:
            return cls(m.group(1))
        else:
            return None
        
if __name__ == '__main__':
    root = Dir(name="/")
    print(root)
    print(File.parse("12321321 foo.txt"))
    print(Dir.parse("12321321 foo.txt"))
    print(File.parse("dir foo"))
    print(Dir.parse("dir foo"))