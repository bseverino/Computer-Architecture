"""CPU functionality."""

import sys
from time import time

ADD = 0b10100000
ADDI = 0b10001111
AND = 0b10101000
CALL = 0b01010000
CMP = 0b10100111
DEC = 0b01100110
DIV = 0b10100011
HLT = 0b00000001
INC = 0b01100101
INT = 0b01010010
IRET = 0b00010011
JEQ = 0b01010101
JGE = 0b01011010
JGT = 0b01010111
JLE = 0b01011001
JMP = 0b01010100
JNE = 0b01010110
LD = 0b10000011
LDI = 0b10000010
MOD = 0b10100100
MUL = 0b10100010
NOP = 0b00000000
NOT = 0b01101001
OR = 0b10101010
POP = 0b01000110
PRA = 0b01001000
PRN = 0b01000111
PUSH = 0b01000101
RET = 0b00010001
SHL = 0b10101100
SHR = 0b10101101
ST = 0b10000100
SUB = 0b10100001
XOR = 0b10101011

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.fl = 0b00000000
        self.halted = True

        self.branchtable = {}
        self.branchtable[ADD] = self.handle_add
        self.branchtable[ADDI] = self.handle_addi
        self.branchtable[AND] = self.handle_and
        self.branchtable[CALL] = self.handle_call
        self.branchtable[CMP] = self.handle_cmp
        self.branchtable[DEC] = self.handle_dec
        self.branchtable[DIV] = self.handle_div
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[INC] = self.handle_inc
        self.branchtable[INT] = self.handle_int
        self.branchtable[IRET] = self.handle_iret
        self.branchtable[JEQ] = self.handle_jeq
        self.branchtable[JGE] = self.handle_jge
        self.branchtable[JGT] = self.handle_jgt
        self.branchtable[JLE] = self.handle_jle
        self.branchtable[JMP] = self.handle_jmp
        self.branchtable[JNE] = self.handle_jne
        self.branchtable[LD] = self.handle_ld
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[MOD] = self.handle_mod
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[NOP] = self.handle_mul
        self.branchtable[NOT] = self.handle_mul
        self.branchtable[OR] = self.handle_mul
        self.branchtable[POP] = self.handle_pop
        self.branchtable[PRA] = self.handle_pra
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[RET] = self.handle_ret
        self.branchtable[SHL] = self.handle_shl
        self.branchtable[SHR] = self.handle_shr
        self.branchtable[ST] = self.handle_st
        self.branchtable[SUB] = self.handle_sub        
        self.branchtable[XOR] = self.handle_xor
    
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

        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]

        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]

        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]

        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
        
        elif op == "SHL":
            self.reg[reg_a] <<= self.reg[reg_b]
        
        elif op == "SHR":
            self.reg[reg_a] >>= self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")
        
        self.reg[reg_a] &= 255

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
    
    def handle_add(self):
        num_a = self.ram_read(self.pc + 1)
        num_b = self.ram_read(self.pc + 2)
        self.alu("ADD", num_a, num_b)
        self.pc += 3
    
    def handle_addi(self):
        reg_num = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[reg_num] += value
        self.pc += 3
    
    def handle_and(self):
        num_a = self.ram_read(self.pc + 1)
        num_b = self.ram_read(self.pc + 2)
        self.alu("AND", num_a, num_b)
        self.pc += 3
    
    def handle_call(self):
        reg_num = self.ram_read(self.pc + 1)
        self.reg[7] -= 1
        self.ram_write(self.reg[7], self.pc + 2)
        self.pc = self.reg[reg_num]

    def handle_cmp(self):
        reg_a = self.reg[self.ram_read(self.pc + 1)]
        reg_b = self.reg[self.ram_read(self.pc + 2)]
        if reg_a == reg_b:
            self.fl = 0b00000001
        elif reg_a < reg_b:
            self.fl = 0b00000100
        else:
            self.fl = 0b00000010
        self.pc += 3

    def handle_dec(self):
        reg_num = self.ram_read(self.pc + 1)
        self.reg[reg_num] -= 1
        self.pc += 2
    
    def handle_div(self):
        num_a = self.ram_read(self.pc + 1)
        num_b = self.ram_read(self.pc + 2)
        if self.reg[num_b] == 0:
            print('Cannot divide by 0')
            self.halted = True
        else:
            self.alu("DIV", num_a, num_b)
            self.pc += 3
    
    def handle_hlt(self):
        self.halted = True

    def handle_inc(self):
        reg_num = self.ram_read(self.pc + 1)
        self.reg[reg_num] += 1
        self.pc += 2
    
    def handle_int(self):
        reg_num = self.ram_read(self.pc + 1)
        self.pc += 2
    
    def handle_iret(self):
        self.pc += 1

    def handle_jeq(self):
        if self.fl & 0b00000001 == 0b00000001:
            self.handle_jmp()
        else:
            self.pc += 2

    def handle_jge(self):
        self.pc += 2

    def handle_jgt(self):
        self.pc += 2

    def handle_jle(self):
        self.pc += 2
    
    def handle_jmp(self):
        reg_num = self.ram_read(self.pc + 1)
        self.pc = self.reg[reg_num]

    def handle_jne(self):
        if self.fl & 0b00000001 == 0b00000000:
            self.handle_jmp()
        else:
            self.pc += 2
    
    def handle_ld(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.reg[reg_a] = self.ram_read(self.reg[reg_b])
        self.pc += 3
    
    def handle_ldi(self):
        reg_num = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[reg_num] = value
        self.pc += 3

    def handle_mod(self):        
        num_a = self.ram_read(self.pc + 1)
        num_b = self.ram_read(self.pc + 2)
        self.alu("MOD", num_a, num_b)
        self.pc += 3
    
    def handle_mul(self):
        num_a = self.ram_read(self.pc + 1)
        num_b = self.ram_read(self.pc + 2)
        self.alu("MUL", num_a, num_b)
        self.pc += 3

    def handle_nop(self):
        self.pc += 1

    def handle_not(self):        
        num_a = self.ram_read(self.pc + 1)
        self.alu("NOT", num_a, None)
        self.pc += 2

    def handle_or(self):        
        num_a = self.ram_read(self.pc + 1)
        num_b = self.ram_read(self.pc + 2)
        self.alu("OR", num_a, num_b)
        self.pc += 3

    def handle_pop(self):
        if self.reg[7] >= 244:
            print('Cannot pop, stack empty')
            self.halted = True
        else:
            reg_num = self.ram_read(self.pc + 1)
            self.reg[reg_num] = self.ram_read(self.reg[7])
            self.reg[7] += 1
            self.pc += 2

    def handle_pra(self):
        reg_num = self.ram_read(self.pc + 1)
        print(self.reg[reg_num])
        self.pc += 2

    def handle_prn(self):
        reg_num = self.ram_read(self.pc + 1)
        print(self.reg[reg_num])
        self.pc += 2

    def handle_push(self):
        reg_num = self.ram_read(self.pc + 1)
        self.reg[7] -= 1
        self.ram_write(self.reg[7], self.reg[reg_num])
        self.pc += 2

    def handle_ret(self):
        self.pc = self.ram_read(self.reg[7])
        self.reg[7] += 1

    def handle_st(self):
        reg_num_a = self.ram_read(self.pc + 1)
        reg_num_b = self.ram_read(self.pc + 2)
        self.ram_write(self.ram[reg_num_a], self.reg[reg_num_b])
        self.pc += 3

    def handle_shl(self):        
        num_a = self.ram_read(self.pc + 1)
        num_b = self.ram_read(self.pc + 2)
        self.alu("SHL", num_a, num_b)
        self.pc += 3

    def handle_shr(self):        
        num_a = self.ram_read(self.pc + 1)
        num_b = self.ram_read(self.pc + 2)
        self.alu("SHR", num_a, num_b)
        self.pc += 3
    
    def handle_sub(self):        
        num_a = self.ram_read(self.pc + 1)
        num_b = self.ram_read(self.pc + 2)
        self.alu("SUB", num_a, num_b)
        self.pc += 3
    
    def handle_xor(self):        
        num_a = self.ram_read(self.pc + 1)
        num_b = self.ram_read(self.pc + 2)
        self.alu("XOR", num_a, num_b)
        self.pc += 3

    def run(self):
        """Run the CPU."""
        self.halted = False
        self.reg[7] = 244
        start_time = time()

        while not self.halted:
            new_time = time()
            if new_time - start_time >= 1:
                print('It\'s been a second')
                self.reg[6] = 0b00000000
                start_time = new_time
            ir = self.ram[self.pc]
            self.branchtable[ir]()
            # self.trace()