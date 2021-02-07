"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000


class CPU:
    """Main CPU class."""
    LDI = 0b10000010
    PRN = 0b01000111
    HLT = 0b00000001
    MUL = 0b10100010
    CALL = 0b01010000
    RET = 0b00010001
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.sp = len(self.reg) - 1

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""
        address = 0
        if len(sys.argv) != 2:
            print("usage: comp.py + filename")
            sys.exit(1)
        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    try:
                        # print("Line", line)
                        line = line.split("#", 1)[0]
                        line = int(line, 2)
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass
        except FileNotFoundError:
            print(f"Could not find file: {sys.argv[1]}")
            sys.exit(1)
        for instruction in self.reg:
            self.ram[address] = instruction
            address += 1


            
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            #instruction register
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            if ir == HLT: 
                self.running = False
            elif ir == PRN:
                print(self.reg[operand_a])
            elif ir == LDI:
                self.reg[operand_a] = operand_b
            elif ir == MUL:
                self.alu('MUL', operand_a, operand_b)
            elif ir == PUSH:
                self.sp -= 1
                self.reg[self.sp] = self.reg[self.ram[self.pc + 1]] 
            elif ir == POP:
                self.reg[self.ram[self.pc + 1]] = self.reg[self.sp]
                self.sp += 1
            elif ir == RET:
                self.pc = self.ram[self.reg[6]]
                self.reg[6] += 1
            elif ir == CALL:
                return_address = self.pc + 2

                self.reg[6] -= 1

                self.ram[self.reg[6]] = return_address

                self.pc = self.reg[self.ram_read(self.pc + 1)]
            elif ir == ADD:
                num_1 = self.reg[self.ram_read(self.pc + 1)]
                num_2 = self.reg[self.ram_read(self.pc + 2)]

                self.reg[self.ram_read(self.pc + 1)] = (num_1 + num_2)



            if ir != CALL and ir != RET:
                offset = ir >> 6
                self.pc += offset + 1



