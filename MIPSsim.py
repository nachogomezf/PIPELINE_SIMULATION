'''On my honor, I have neither given nor receiven any unauthorised aid in this assignment'''
import math as m
import sys
import os
import queue
def twoscomp(num):
    l = list(num)
    if l[0] == "1":
        l = l[1:len(l)]
        for x in range(len(l)):
            if (l[x] == "0"):
                l[x] = "1"
            elif (l[x] == "1"):
                l[x] = "0"
        return -(int(''.join(l), 2)+1)
    else:
        return int(num, 2)

class Instruction1:
    def __init__(self,pc,inst):
        self.opcode = inst[3:6]
        if (self.opcode == "000"):
            self.addr = int((inst[7:32] + "00"), 2)
            self.name = "\t%d\tJ #%d\n" % (pc, self.addr)
        elif (self.opcode == "001"):
            self.addr = int((inst[16:32] + "00"), 2)
            self.rs = int(inst[6:11], 2)
            self.rd = int(inst[11:16], 2)
            self.name = "\t%d\tBEQ R%d, R%d, #%d\n" % (pc, self.rs, self.rd, self.addr)
        elif (self.opcode == "010"):
            self.name = "\t%d\tBNE R%d, R%d, #%d\n" % (pc, self.rs, self.rd, self.addr)
            self.addr = int((inst[16:32] + "00"), 2)
            self.rs = int(inst[6:11], 2)
            self.rd = int(inst[11:16], 2)
        elif (self.opcode == "011"):
            self.name = "\t%d\tBGTZ R%d, #%d\n" % (pc, self.rs, self.addr)
            self.addr =  int((inst[16:32] + "00"), 2)
            self.rs = int(inst[6:11], 2)
        elif (self.opcode == "100"):
            self.base = int(inst[6:11], 2)
            self.rt = int(inst[11:16], 2)
            self.offset = int(inst[16:32], 2)
            self.name = "\t%d\tSW R%d, %d(R%d)\n" % (pc, self.rt, self.offset, self.base)
        elif (self.opcode == "101"):
            self.name = "\t%d\tLW R%d, %d(R%d)\n" % (pc, self.rt, self.offset, self.base)
            self.base = int(inst[6:11], 2)
            self.rt = int(inst[11:16], 2)
            self.offset = int(inst[16:32], 2)
        elif (self.opcode == "110"):
            self.name = "\t%d\tBREAK\n" % pc
    
    
class Instruction2:
    def __init__(self,pc,inst):
        self.opcode = inst[3:6]
        self.dest = int(inst[6:11], 2)
        self.src1 = int(inst[11:16], 2)
        self.src2 = int(inst[16:21], 2)
        if (self.opcode == "100"):
            self.name = "\t%d\tSRL R%d, R%s, #%s\n" % (pc, self.dest, self.src1, self.src2)
        elif (self.opcode == "101"):
            self.name = "\t%d\tSRA R%d, R%s, #%s\n" % (pc, self.dest, self.src1, self.src2)
        elif (self.opcode == "000"):
            self.name = "\t%d\tADD R%d, R%d, R%d\n" % (pc, self.dest, self.src1, self.src2)
        elif (self.opcode == "001"):
            self.name = "\t%d\tSUB R%d, R%d, R%d\n" % (pc, self.dest, self.src1, self.src2)
        elif (self.opcode == "010"):
            self.name = "\t%d\tAND R%d, R%d, R%d\n" % (pc, self.dest, self.src1, self.src2)
        elif ( self.opcode == "011"):
            self.name = "\t%d\tOR R%d, R%d, R%d\n" % (pc, self.dest, self.src1, self.src2)
        elif (self.opcode == "110"):
            self.name = "\t%d\tMUL R%d, R%d, R%d\n" % (pc, self.dest, self.src1, self.src2)


class Instruction3:
    def __init__(self,pc,inst):
        self.dest = int(inst[6:11], 2)
        self.src = int(inst[11:16], 2)
        self.imm = twoscomp(inst[16:32])
        if (self.opcode == "000"):
            self.name = "\t%d\tADDI R%d, R%d, #%d\n" % (pc, self.dest, self.src, self.imm)
        elif (self.opcode == "001"):
            
        elif (self.opcode == "010"):


class Register:

    def __init__(self,num,value,readable=True,writable=True):
        self.num = num
        self.value = value
        self.readable = readable
        self.writable = writable

    def isReadable(self):
        return self.readable
    
    def isWritable(self):
        return self.writable
     
    def getValue(self):
        return self.value
    
    def getNum(self):
        return self.getNum

class fetchUnit:

    def __init__(self,isStalled=False,bufFull=False):
        self.isStalled = isStalled
        self.bufFull = bufFull
    
    def stalled(self):
        return self.isStalled

    def full(self):
        return self.bufFull

def srl(num, shift):
    return (num & 0xffffffff) >> shift # By computing num & 0xffffffff we get the 32-bit binary represation 
                                       # of the number without changing it. Then, we compute the arithmetic shift.

if __name__ == "__main__":

    input = open(sys.argv[1], "r")
    sim = open("sample.txt", "w+")
    pc = 260
    buf1 = queue.PriorityQueue(8)
    buf2 = queue.Queue(2)
    buf3 = queue.Queue(2)
    buf4 = queue.Queue(2)
    buf5 = queue.Queue(1)
    buf6 = queue.Queue(1)
    buf7 = queue.Queue(1)
    buf8 = queue.Queue(1)
    buf9 = queue.Queue(1)
    buf10 = queue.Queue(1)
    fetch = fetchUnit()
    pc = 260
    linelist = input.readlines()
    registers = []
    for i in range(32):
        registers.append(Register(i,0)) 
    stop = False
    i, j, k, l = 0, 0, 0, 0
    while (linelist[j][:6] != "000110"):
        j += 1
    firstdata = j*4 + 264
    instructions = [None] * (j+1)
    initialdata = [0] * (len(linelist)-j-1)
    data = [0] * (len(linelist)-j-1)
    for k in range(len(data)):
        data[k] = twoscomp(linelist[j+1])
        initialdata[k] = twoscomp(linelist[j+1])
        j += 1
    
    for index, i in enumerate(linelist):
        if (linelist[i][:3] == "000"):  # TYPE 1
            if (linelist[i][3:6] == "000"):  # J INSTRUCTION
                addr = int((linelist[i][7:32] + "00"), 2)
                instructions[i] = "\t%d\tJ #%d\n" % (pc, addr)
                #pc = addr
            elif (linelist[i][3:6] == "001"):  # BEQ INSTRUCTION
                addr = int((linelist[i][16:32] + "00"), 2)
                rs = int(linelist[i][6:11], 2)
                rd = int(linelist[i][11:16], 2)
                instructions[i] = "\t%d\tBEQ R%d, R%d, #%d\n" % (pc, rs, rd, addr)
                '''if (registers[rs] == registers[rd]):
                    pc += addr+4
                else:
                    pc += 4'''
            elif (linelist[i][3:6] == "010"):  # BNE INSTRUCTION
                addr = int((linelist[i][16:32] + "00"), 2)
                rs = int(linelist[i][6:11], 2)
                rd = int(linelist[i][11:16], 2)
                instructions[i] = "\t%d\tBNE R%d, R%d, #%d\n" % (pc, rs, rd, addr)
                '''if (registers[rs] != registers[rd]):
                    pc += addr+4
                else:
                    pc += 4'''
            elif (linelist[i][3:6] == "011"):  # BGTZ INSTRUCTION
                addr = int((linelist[i][16:32] + "00"), 2)
                rs = int(linelist[i][6:11], 2)
                instructions[i] = "\t%d\tBGTZ R%d, #%d\n" % (pc, rs, addr)
                '''if (registers[rs] > 0):
                    pc += addr+4
                else:
                    pc += 4'''
            elif (linelist[i][3:6] == "100"):  # SW INSTRUCTION
                base = int(linelist[i][6:11], 2)
                rt = int(linelist[i][11:16], 2)
                offset = int(linelist[i][16:32], 2)
                instructions[i] = "\t%d\tSW R%d, %d(R%d)\n" % (pc, rt, offset, base)
                '''
                data[(registers[base]+offset-firstdata)//4] = registers[rt]
                pc += 4'''
            elif (linelist[i][3:6] == "101"):  # LW INSTRUCTION
                base = int(linelist[i][6:11], 2)
                rt = int(linelist[i][11:16], 2)
                offset = int(linelist[i][16:32], 2)
                instructions[i] = "\t%d\tLW R%d, %d(R%d)\n" % (pc, rt, offset, base)
                '''
                registers[rt] = data[(registers[base]+offset-firstdata)//4]
                pc += 4'''
            elif (linelist[i][3:6] == "110"):  # BREAK INSTRUCTION
                stop = True
                i = (pc-260)//4
                instructions[i] = "\t%d\tBREAK\n" % pc
            else:
                print("Unknown operation")
                break
        elif (linelist[i][:3] == "001"):  # CATEGORY-2 INSTRUCTIONS
            opcode = linelist[i][3:6]
            dest = int(linelist[i][6:11], 2)
            src1 = int(linelist[i][11:16], 2)
            src2 = int(linelist[i][16:21], 2)
            if (opcode == "100"):  # SRL INSTRUCTION
                registers[dest] = srl(registers[src1], src2)
                instructions[i] = "\t%d\tSRL R%d, R%s, #%s\n" % (
                    pc, dest, src1, src2)
            elif (opcode == "101"):  # SRA INSTRUCTION
                registers[dest] = registers[src1] >> src2
                instructions[i] = "\t%d\tSRA R%d, R%s, #%s\n" % (
                    pc, dest, src1, src2)
            elif (opcode == "000"):  # ADD INSTRUCTION
                registers[dest] = registers[src1] + registers[src2]
                instructions[i] = "\t%d\tADD R%d, R%d, R%d\n" % (
                    pc, dest, src1, src2)
            elif (opcode == "001"):  # SUB INSTRUCTION
                registers[dest] = registers[src1] - registers[src2]
                instructions[i] = "\t%d\tSUB R%d, R%d, R%d\n" % (
                    pc, dest, src1, src2)
            elif (opcode == "010"):  # AND INSTRUCTION
                registers[dest] = registers[src1] & registers[src2]
                instructions[i] = "\t%d\tAND R%d, R%d, R%d\n" % (
                    pc, dest, src1, src2)
            elif (opcode == "011"):  # OR INSTRUCTION
                registers[dest] = registers[src1] | registers[src2]
                instructions[i] = "\t%d\tOR R%d, R%d, R%d\n" % (
                    pc, dest, src1, src2)
            elif (opcode == "110"):  # MUL INSTRUCTION
                registers[dest] = registers[src1] * registers[src2]
                instructions[i] = "\t%d\tMUL R%d, R%d, R%d\n" % (
                    pc, dest, src1, src2)
            pc += 4
        elif (linelist[i][:3] == "010"):  # TYPE-3 INSTRUCTIONS
            dest = int(linelist[i][6:11], 2)
            src = int(linelist[i][11:16], 2)
            imm = twoscomp(linelist[i][16:32])
            if (linelist[i][3:6] == "000"):  # ADDI INSRUCTION
                registers[dest] = registers[src] + imm
                instructions[i] = "\t%d\tADDI R%d, R%d, #%d\n" % (
                    pc, dest, src, imm)
            elif (linelist[i][3:6] == "001"):  # ANDI INSTRUCTION
                registers[dest] = registers[src] & imm
                instructions[i] = "\t%d\tANDI R%d, R%d, #%d\n" % (
                    pc, dest, src, imm)
            elif (linelist[i][3:6] == "010"):  # ORI INSTRUCTION
                registers[dest] = registers[src] | imm
                instructions[i] = "\t%d\tORI R%d, R%d, #%d\n" % (
                    pc, dest, src, imm)

    while (stop is False):
        '''fetch
        if (fetch.stalled() is True):
            #something
        elif ( fetch.full() is True):
            #something
        else:
            '''

            
        l += 1
        if (linelist[i][:3] == "000"):  # TYPE 1
            if (linelist[i][3:6] == "000"):  # J INSTRUCTION
                addr = int((linelist[i][7:32] + "00"), 2)
                instructions[i] = "\t%d\tJ #%d\n" % (pc, addr)
                #pc = addr
            elif (linelist[i][3:6] == "001"):  # BEQ INSTRUCTION
                addr = int((linelist[i][16:32] + "00"), 2)
                rs = int(linelist[i][6:11], 2)
                rd = int(linelist[i][11:16], 2)
                instructions[i] = "\t%d\tBEQ R%d, R%d, #%d\n" % (pc, rs, rd, addr)
                '''if (registers[rs] == registers[rd]):
                    pc += addr+4
                else:
                    pc += 4'''
            elif (linelist[i][3:6] == "010"):  # BNE INSTRUCTION
                addr = int((linelist[i][16:32] + "00"), 2)
                rs = int(linelist[i][6:11], 2)
                rd = int(linelist[i][11:16], 2)
                instructions[i] = "\t%d\tBNE R%d, R%d, #%d\n" % (pc, rs, rd, addr)
                '''if (registers[rs] != registers[rd]):
                    pc += addr+4
                else:
                    pc += 4'''
            elif (linelist[i][3:6] == "011"):  # BGTZ INSTRUCTION
                addr = int((linelist[i][16:32] + "00"), 2)
                rs = int(linelist[i][6:11], 2)
                instructions[i] = "\t%d\tBGTZ R%d, #%d\n" % (pc, rs, addr)
                '''if (registers[rs] > 0):
                    pc += addr+4
                else:
                    pc += 4'''
            elif (linelist[i][3:6] == "100"):  # SW INSTRUCTION
                base = int(linelist[i][6:11], 2)
                rt = int(linelist[i][11:16], 2)
                offset = int(linelist[i][16:32], 2)
                instructions[i] = "\t%d\tSW R%d, %d(R%d)\n" % (pc, rt, offset, base)
                '''
                data[(registers[base]+offset-firstdata)//4] = registers[rt]
                pc += 4'''
            elif (linelist[i][3:6] == "101"):  # LW INSTRUCTION
                base = int(linelist[i][6:11], 2)
                rt = int(linelist[i][11:16], 2)
                offset = int(linelist[i][16:32], 2)
                instructions[i] = "\t%d\tLW R%d, %d(R%d)\n" % (pc, rt, offset, base)
                '''
                registers[rt] = data[(registers[base]+offset-firstdata)//4]
                pc += 4'''
            elif (linelist[i][3:6] == "110"):  # BREAK INSTRUCTION
                stop = True
                i = (pc-260)//4
                instructions[i] = "\t%d\tBREAK\n" % pc
            else:
                print("Unknown operation")
                break
        elif (linelist[i][:3] == "001"):  # CATEGORY-2 INSTRUCTIONS
            opcode = linelist[i][3:6]
            dest = int(linelist[i][6:11], 2)
            src1 = int(linelist[i][11:16], 2)
            src2 = int(linelist[i][16:21], 2)
            if (opcode == "100"):  # SRL INSTRUCTION
                registers[dest] = srl(registers[src1], src2)
                instructions[i] = "\t%d\tSRL R%d, R%s, #%s\n" % (
                    pc, dest, src1, src2)
            elif (opcode == "101"):  # SRA INSTRUCTION
                registers[dest] = registers[src1] >> src2
                instructions[i] = "\t%d\tSRA R%d, R%s, #%s\n" % (
                    pc, dest, src1, src2)
            elif (opcode == "000"):  # ADD INSTRUCTION
                registers[dest] = registers[src1] + registers[src2]
                instructions[i] = "\t%d\tADD R%d, R%d, R%d\n" % (
                    pc, dest, src1, src2)
            elif (opcode == "001"):  # SUB INSTRUCTION
                registers[dest] = registers[src1] - registers[src2]
                instructions[i] = "\t%d\tSUB R%d, R%d, R%d\n" % (
                    pc, dest, src1, src2)
            elif (opcode == "010"):  # AND INSTRUCTION
                registers[dest] = registers[src1] & registers[src2]
                instructions[i] = "\t%d\tAND R%d, R%d, R%d\n" % (
                    pc, dest, src1, src2)
            elif (opcode == "011"):  # OR INSTRUCTION
                registers[dest] = registers[src1] | registers[src2]
                instructions[i] = "\t%d\tOR R%d, R%d, R%d\n" % (
                    pc, dest, src1, src2)
            elif (opcode == "110"):  # MUL INSTRUCTION
                registers[dest] = registers[src1] * registers[src2]
                instructions[i] = "\t%d\tMUL R%d, R%d, R%d\n" % (
                    pc, dest, src1, src2)
            pc += 4
        elif (linelist[i][:3] == "010"):  # TYPE-3 INSTRUCTIONS
            dest = int(linelist[i][6:11], 2)
            src = int(linelist[i][11:16], 2)
            imm = twoscomp(linelist[i][16:32])
            if (linelist[i][3:6] == "000"):  # ADDI INSRUCTION
                registers[dest] = registers[src] + imm
                instructions[i] = "\t%d\tADDI R%d, R%d, #%d\n" % (
                    pc, dest, src, imm)
            elif (linelist[i][3:6] == "001"):  # ANDI INSTRUCTION
                registers[dest] = registers[src] & imm
                instructions[i] = "\t%d\tANDI R%d, R%d, #%d\n" % (
                    pc, dest, src, imm)
            elif (linelist[i][3:6] == "010"):  # ORI INSTRUCTION
                registers[dest] = registers[src] | imm
                instructions[i] = "\t%d\tORI R%d, R%d, #%d\n" % (
                    pc, dest, src, imm)
            else:
                print("Unknown instruction")
                break
            pc += 4
        else:
            print("Unkown intruction")
            break
        sim.write("--------------------\nCycle %d:%s\nRegisters" %
                  (l, instructions[i]))
        for a in range(4):
            if (a < 2):
                sim.write("\nR0%d:\t" % (a*8))
            else:
                sim.write("\nR%d:\t" % (a*8))
            for b in range(7):
                sim.write("%d\t" % registers[a*8+b])
            sim.write("%d" % registers[a*8+7])
        sim.write("\n\nData")
        for a in range(m.ceil(len(data)/8)):
            sim.write("\n%d:\t" % (firstdata+32*a))
            for b in range(7):
                if ((a*8+b)<len(data)):
                    sim.write("%d\t" % data[a*8+b])
                else: break
            if (a*8+7)<len(data):
                sim.write("%d" % data[a*8+7])
        if (stop==False):
            sim.write("\n\n")
        else:
            sim.write("\n")
        i = (pc-260)//4

    index = len(instructions)
    k = 0
    sim.seek(sim.tell() - 1, os.SEEK_SET)
    sim.write('')
    sim.close()
    input.close()