import sys

class ClockCpu:
    def __init__(self, instructions):
        self.instructions = instructions
    
    def reset(self):
        self.clock = 0
        self.x = 1
        self.strength = 0
        self.screen = []
        
    def clockinc(self):
        self.clock += 1
        pixel = (self.clock-1)%40
        if abs(pixel - self.x) <= 1:
            self.screen.append('#')
        else:
            self.screen.append('.')
        if self.clock in [20, 60, 100, 140, 180, 220]:
            self.strength += self.clock * self.x
    
    def evaluate(self):
        self.reset()
        for instr in self.instructions:
            #print(instr)
            if instr[0] == "noop":
                self.clockinc()
            elif instr[0] == "addx":
                self.clockinc()
                self.clockinc()
                self.x += int(instr[1])
        return self.strength
    
    def print_screen(self):
        for j in range(6):
            for i in range(40):
                print(self.screen[j*40+i], end="")
            print()
    
    @classmethod
    def fromfile(cls, filename):
        out = []
        with open(filename, "r") as fh:
            for l in fh:
                out.append(l.strip().split())
        return cls(out)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("missing filename argument")
    #print(sys.argv)
    cpu = ClockCpu.fromfile(sys.argv[1])
    print(cpu.evaluate())
    cpu.print_screen()
        