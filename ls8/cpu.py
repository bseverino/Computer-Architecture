"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.halted = True

        self.branchtable = {}
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[ADD] = self.handle_add
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
        self.branchtable[CALL] = self.handle_call
        self.branchtable[RET] = self.handle_ret
    
    def ram_read(self, address):
        if 0 <= address <= 255:
            return self.ram[address]
        else:
            print(f'{address} is an invalid address')

    def ram_write(self, address, value):
        if 0 <= address <= 255:
            self.ram[address] = value
        else:
            print(f'{address} is an invalid address')

    def load(self, filepath):
        """Load a program into memory."""
        print(filepath)

        address = 0

        # For now, we've just hardcoded a program:

        program = []

        with open(f'examples/{filepath}', "r") as a_file:
            # line = a_file.readline()
            for line in a_file:
                if line.startswith('#') or not line.strip():
                    pass
                else:
                    if '#' in line:
                        line = line.split('#')[0].strip()
                    program.append(int(line, 2))

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

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
    
    def handle_hlt(self, arg_a, arg_b):
        self.halted = True
    
    def handle_ldi(self, arg_a, arg_b):
        self.reg[arg_a] = arg_b
        self.pc += 3

    def handle_prn(self, arg_a, arg_b):
        print(self.reg[arg_a])
        self.pc += 2
    
    def handle_add(self, arg_a, arg_b):
        self.alu("ADD", arg_a, arg_b)
        self.pc += 3
    
    def handle_mul(self, arg_a, arg_b):
        self.alu("MUL", arg_a, arg_b)
        self.pc += 3

    def handle_push(self, arg_a, arg_b):   
        self.reg[7] -= 1
        self.ram_write(self.reg[7], self.reg[arg_a])
        self.pc += 2

    def handle_pop(self, arg_a, arg_b):
        if self.reg[7] >= 244:
            print('Cannot pop, stack empty')
            self.halted = True
        else:
            self.reg[arg_a] = self.ram_read(self.reg[7])
            self.reg[7] += 1
            self.pc += 2
    
    def handle_call(self, arg_a, arg_b):
        self.reg[7] -= 1
        self.ram_write(self.reg[7], self.pc + 2)
        self.pc = self.reg[arg_a]

    def handle_ret(self, arg_a, arg_b):
        self.pc = self.ram_read(self.reg[7])
        self.reg[7] += 1

    def run(self):
        """Run the CPU."""
        self.halted = False
        self.reg[7] = 244

        while not self.halted:
            ir = self.ram[self.pc]
            arg_a = self.ram_read(self.pc + 1)
            arg_b = self.ram_read(self.pc + 2)
            try:
                self.branchtable[ir](arg_a, arg_b)
                self.trace()
            except:
                print(f'Error with instruction {ir} at address {self.pc}')
                self.halted = True