import random

class Obfuscator:
    def __init__(self):
        pass

    def rot(self, text: str, n: int) -> str:
        result = []

        for char in text:
            if "a" <= char <= "z":
                result.append(chr((ord(char) - ord("a") + n) % 26 + ord("a")))
            elif "A" <= char <= "Z":
                result.append(chr((ord(char) - ord("A") + n) % 26 + ord("A")))
            else:
                result.append(char)

        return "".join(result)

    def run(self, code: str):
        rot_len = 13
        rot = [ord(x) for x in self.rot(code, rot_len)]

        bytecode = [
            OP.LOAD_STR, 0, len(rot),
            OP.ROT, 0, 50, len(rot), rot_len
        ]

        bytecode[3:3] = rot

        return bytecode


class OP:
    MOV = 1
    PUSH = 2
    ADD = 3
    LOAD_STR = 4
    ROT = 5


class REG:
    A = 20
    B = 21
    C = 22
    D = 25
    E = 26
    F = 27


class Vm:
    def __init__(self, bytecode):
        self.bytecode = bytecode

        self.registers = {}
        self.memory = []
        self.pc = 0

        self.map = {
            OP.MOV: self.mov,
            OP.PUSH: self.push,
            OP.ADD: self.add,
            OP.LOAD_STR: self.load_str,
            OP.ROT: self.rot,
        }
    
    # rot, src, dst, len, n
    def rot(self):
        src = self.get_byte()
        dst = self.get_byte()

        strlen = self.get_byte()
        rotlen = self.get_byte()
        
        x = Obfuscator().rot([chr(x) for x in self.memory[src:strlen]], rotlen)
        exec(x)
    
    def load_str(self):
        dst = self.get_byte()
        strlen = self.get_byte()
        out = []

        for _ in range(strlen):
            out.append(self.get_byte())

        self.memory[dst:dst + strlen] = out

    def mov(self):
        reg = self.get_byte()
        value = self.get_byte()
        
        self.registers[reg] = value

    def push(self):
        value = self.get_byte()
        self.memory.append(value)

    def add(self):
        dst = self.get_byte()
        a = self.get_byte()
        b = self.get_byte()
        
        self.registers[dst] = self.registers[a] + self.registers[b]

    def get_byte(self):
        out = self.bytecode[self.pc]
        self.pc += 1

        return out

    def run(self):
        while self.pc < len(self.bytecode):
            op = self.get_byte()
            self.map[op]()

        print(self.registers, self.memory)

def conv_o(str):
    return [ord(x) for x in str]

if __name__ == "__main__":
    script = open("./src.py", encoding="utf8", errors="ignore").read()

    bytecode = Obfuscator().run(script)
    print(bytecode)
    Vm(
        bytecode
    ).run()
