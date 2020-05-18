"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
    
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
        halted = False

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010

        while not halted:
            ir = self.ram[self.pc]
            # self.trace()

            if ir == LDI:
                reg_num = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)
                self.reg[reg_num] = value
                self.pc += 3
            
            elif ir == PRN:
                reg_num = self.ram_read(self.pc + 1)
                print(self.reg[reg_num])
                self.pc += 2

            elif ir == MUL:
                reg_num_a = self.ram_read(self.pc + 1)
                reg_num_b = self.ram_read(self.pc + 2)
                self.reg[reg_num_a] *= self.reg[reg_num_b]
                self.pc += 3

            elif ir == HLT:
                halted = True
            
            else:
                print(f'Unknown instruction {ir} at address {self.pc}')
                break