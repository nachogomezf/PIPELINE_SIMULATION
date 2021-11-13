'''On my honor, I have neither given nor receiven any unauthorised aid in this assignment'''
import math as m
import sys
import os
import queue as q
from typing import List
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

def enqueue(list, elem):
    count = 0
    for x in list:
        if x is not None:
            count += 1
    list[count] = elem
    return list

def dequeue(list,pos):
    list.pop(pos)
    list.append(None)
    return list

def isFull(list):
    count = 0
    for elem in list:
        if elem is not None:
            count += 1
    return (count == (len(list)-1))


class Instruction1:
    def __init__(self,inst):
        self.stage = ""
        self.pc = 0
        self.consumed = False
        self.isBranch=False
        self.type=1
        self.subtype=1
        self.opcode = inst[3:6]
        if (self.opcode == "000"):
            self.subtype = -1
            self.addr = int((inst[7:32] + "00"), 2)
            self.name = "J #%d" % (self.addr)
            self.isBranch = True
        elif (self.opcode == "001"):
            self.addr = int((inst[16:32] + "00"), 2)
            self.rs = int(inst[6:11], 2)
            self.rd = int(inst[11:16], 2)
            self.isBranch = True
            self.name = "BEQ R%d, R%d, #%d" % (self.rs, self.rd, self.addr)
        elif (self.opcode == "010"):
            self.addr = int((inst[16:32] + "00"), 2)
            self.rs = int(inst[6:11], 2)
            self.rd = int(inst[11:16], 2)
            self.isBranch = True
            self.name = "BNE R%d, R%d, #%d" % (self.rs, self.rd, self.addr)
        elif (self.opcode == "011"):
            self.subtype = 0
            self.addr =  int((inst[16:32] + "00"), 2)
            self.rs = int(inst[6:11], 2)
            self.isBranch = True
            self.name = "BGTZ R%d, #%d" % (self.rs, self.addr)
        elif (self.opcode == "100"):
            self.rt = int(inst[11:16], 2)
            self.offset = int(inst[16:32], 2)
            self.base = int(inst[6:11], 2)
            self.subtype = 2
            self.name = "SW R%d, %d(R%d)" % (self.rt, self.offset, self.base)
        elif (self.opcode == "101"):
            self.base = int(inst[6:11], 2)
            self.rt = int(inst[11:16], 2)
            self.offset = int(inst[16:32], 2)
            self.name = "LW R%d, %d(R%d)" % (self.rt, self.offset, self.base)
            self.subtype = 3
        elif (self.opcode == "110"):
            self.name = "BREAK"
        self.name = "[%s]" % self.name
    
    def exec(self,registers, firstdata, data, stop, pc):
        if self.opcode == "000":
            pc = self.addr
            return pc
        elif self.opcode == "001":
            if (registers[self.rs].value == registers[self.rd].value):
                pc += self.addr+4
            else:
                pc += 4
            return pc, registers, data, stop
        elif self.opcode == "010":
            if (registers[self.rs].value != registers[self.rd].value):
                    pc += self.addr+4
            else:
                pc += 4
            return pc, registers, data, stop
        elif self.opcode == "011":
            if (registers[self.rs].value > 0):
                    pc += self.addr+4
            else:
                pc += 4
            return pc, registers, data, stop
        elif self.opcode == "100":
            data[(registers[self.base].value+self.offset-firstdata)//4] = registers[self.rt].value
            pc += 4
            return pc, registers, data, stop
        elif self.opcode == "101":
            registers[self.rt].value = data[(registers[self.base]+self.offset-firstdata)//4]
            pc += 4
            return pc, registers, data, stop
        elif self.opcode == "110":
            stop = True
            return pc, registers, data, stop
    
class Instruction2:
    def __init__(self,inst):
        self.stage = ""
        self.consumed = False
        self.isBranch = False
        self.type=2
        self.subtype = 5
        self.pc = 0
        self.opcode = inst[3:6]
        self.dest = int(inst[6:11], 2)
        self.src1 = int(inst[11:16], 2)
        self.src2 = int(inst[16:21], 2)
        if (self.opcode == "100"):
            self.name = "SRL R%d, R%s, #%s" % (self.dest, self.src1, self.src2)
        elif (self.opcode == "101"):
            self.name = "SRA R%d, R%s, #%s" % (self.dest, self.src1, self.src2)
        elif (self.opcode == "000"):
            self.name = "ADD R%d, R%d, R%d" % (self.dest, self.src1, self.src2)
        elif (self.opcode == "001"):
            self.name = "SUB R%d, R%d, R%d" % (self.dest, self.src1, self.src2)
        elif (self.opcode == "010"):
            self.name = "AND R%d, R%d, R%d" % (self.dest, self.src1, self.src2)
        elif ( self.opcode == "011"):
            self.name = "OR R%d, R%d, R%d" % (self.dest, self.src1, self.src2)
        elif (self.opcode == "110"):
            self.name = "MUL R%d, R%d, R%d" % (self.dest, self.src1, self.src2)
            self.subtype = 4
        self.name = "[%s]" % self.name
    
    def exec(self, registers):
        if self.opcode == "100":
            registers[self.dest].value = srl(registers[self.src1].value, self.src2)
        elif self.opcode == "101":
            registers[self.dest].value = registers[self.src1].value >> self.src2
        elif self.opcode == "000":
            registers[self.dest].value = registers[self.src1].value + registers[self.src2].value
        elif self.opcode == "001":
            registers[self.dest].value = registers[self.src1].value - registers[self.src2].value
        elif self.opcode == "010":
            registers[self.dest].value = registers[self.src1].value & registers[self.src2].value
        elif self.opcode == "011":
            registers[self.dest].value = registers[self.src1].value | registers[self.src2].value
        elif self.opcode == "110":
            registers[self.dest].value = registers[self.src1].value * registers[self.src2].value
        return registers

class Instruction3:
    def __init__(self,inst):
        self.stage = ""
        self.consumed = False
        self.subtype = 5
        self.isBranch = False
        self.pc = 0
        self.type=3
        self.dest = int(inst[6:11], 2)
        self.src = int(inst[11:16], 2)
        self.imm = twoscomp(inst[16:32])
        self.opcode = inst[3:6]
        if (self.opcode == "000"):
            self.name = "ADDI R%d, R%d, #%d" % (self.dest, self.src, self.imm)
        elif (self.opcode == "001"):
            self.name = "ANDI R%d, R%d, #%d" % (self.dest, self.src, self.imm)
        elif (self.opcode == "010"):
            self.name = "ORI R%d, R%d, #%d" % (self.dest, self.src, self.imm)
        self.name = "[%s]" % self.name
    
    def exec(self, registers):
        if self.opcode == "000":
             registers[self.dest].value = registers[self.src].value + self.imm
        elif self.opcode == "001":
             registers[self.dest].value = registers[self.src].value & self.imm
        elif self.opcode == "010":
             registers[self.dest].value = registers[self.src].value | self.imm
        return registers

class Register:

    def __init__(self,num,value,readable=True, writable=True, stage=""):
        self.num = num
        self.value = value
        self.readable = readable
        self.writable = writable
        self.stage = stage
    
    '''def __LE__(self,other):
        if ((self.stage == "IF" or self.stage == "IS" ) and (other.stage == "IF" or other.stage == "")): return True
        elif (self.stage == "IS") and (other != "IF")'''


class fetchUnit:

    def __init__(self,isStalled=False,bufFull=False,wait="",exec=""):
        self.stalled = isStalled
        self.full = bufFull
        self.wait = wait
        self.exec = exec

class FunctionalUnit:

    def __init__(self, name="",busy=0, op="", Fi=None, Fj=None, Fk = None, Qj=None, Qk=None, Rj=None, Rk=None) :
        self.name = name
        self.busy = busy
        self.op = op
        self.fi= Fi
        self.fj = Fj
        self.fk = Fk
        self.qj = Qj
        self.qk = Qk
        self.rj = Rj
        self.rk = Rk

    

def srl(num, shift):
    return (num & 0xffffffff) >> shift # By computing num & 0xffffffff we get the 32-bit binary represation 
                                       # of the number without changing it. Then, we compute the arithmetic shift.

if __name__ == "__main__":

    input = open(sys.argv[1], "r")
    sim = sys.stdout
    '''
    buf1 = q.PriorityQueue(8)
    buf2 = q.Queue(2)
    buf3 = q.Queue(2)
    buf4 = q.Queue(2)
    buf5 = q.Queue(1)
    buf6 = q.Queue(1)
    buf7 = q.Queue(1)
    buf8 = q.Queue(1)
    buf9 = q.Queue(1)
    buf10 = q.Queue(1)
    for i in range(8): buf1.put("")
    for i in range(2): buf2.put'''
    buf1,buf2,buf3,buf4,buf5,buf6,buf7,buf8,buf9,buf10 = [None for i in range(8)],[None for i in range(2)],[None for i in range(2)],[None for i in range(2)],[None],[None],[None],[None],[None],[None]
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
    NUM_INSTRUCTIONS = j+1
    units = []
    units_names = ["IS", "ALU1", "ALU2", "MUL1", "MUL2", "MUL3", "MEM", "WB"]
    for a in units_names: units.append(FunctionalUnit(name=a))
    firstdata = j*4 + 264
    instructions = [None] * (j+1)
    initialdata = [0] * (len(linelist)-j-1)
    data = [0] * (len(linelist)-j-1)
    for k in range(len(data)):
        data[k] = twoscomp(linelist[j+1])
        initialdata[k] = twoscomp(linelist[j+1])
        j += 1
    dis=[]
    for a in range(NUM_INSTRUCTIONS):
        if (linelist[a][:3] == "000"):
            dis.append(Instruction1(linelist[a]))
        elif (linelist[a][:3] == "001"):
            dis.append(Instruction2(linelist[a]))
        elif (linelist[a][:3] == "010"):
            dis.append(Instruction3(linelist[a]))
    i=0
    cycle=1
    while (stop is False):
        for elem in buf1: 
            if elem is not None: elem.consumed = False
        for elem in buf2: 
            if elem is not None: 
                elem.consumed = False
        for elem in buf3: 
            if elem is not None: elem.consumed = False
        for elem in buf4:
            if elem is not None: elem.consumed = False
        for elem in buf5: 
            if elem is not None: elem.consumed = False
        for elem in buf6: 
            if elem is not None: elem.consumed = False
        for elem in buf7:
            if elem is not None: elem.consumed = False
        for elem in buf8: 
            if elem is not None: elem.consumed = False
        for elem in buf9:
            if elem is not None: elem.consumed = False
        for elem in buf10: 
            if elem is not None: elem.consumed = False
        '''
        INSTRUCTION FETCH
        
        '''
        if (fetch.stalled is False and fetch.full is False):
            for i in range(4):
                if (dis[i].isBranch is True): 
                    if (dis[i].subtype == 1 and 
                        registers[dis[i].rs].readable == True and
                        registers[dis[i].rd].readable == True):
                        fetch.exec = dis[i]
                    elif (dis[i].subtype == -1):
                        fetch.exec = dis[i]
                    else:
                        fetch.stalled = True
                        fetch.wait = dis[i]
                    break
                else:
                    count = 0
                    if (isFull(buf1)):
                        fetch.full = True 
                        break
                    dis[i].consumed = True
                    dis[i].stage = "IF"
                    buf1 = enqueue(buf1,dis[i])
                    if (dis[i].type == 1 and (
                    dis[i].subtype == 2 or dis[i].subtype == 3)):
                            registers[dis[i].rs].writable = False
                            registers[dis[i].rd].readable = False
                            registers[dis[i].rd].writable = False
                    elif (dis[i].type == 2):
                        registers[dis[i].src1].writable = False
                        registers[dis[i].src2].writable = False
                        registers[dis[i].dest].readable = False
                        registers[dis[i].dest].writable = False
                    elif (dis[i].type == 3):
                        registers[dis[i].src].writable = False
                        registers[dis[i].dest].readable = False
                        registers[dis[i].dest].writable = False

        '''
        INSTRUCTION ISSUE
        '''

        for index,elem in enumerate(buf1):
            if elem is None: break
            if elem.consumed is False:
                if elem.subtype == 2:
                    if (isFull(buf2) is False and elem.rt.readable
                    and elem.rt.writable and elem.base.readable):
                        buf2 = enqueue(buf2,elem)
                        buf1 = dequeue(buf1,index)
                elif elem.subtype == 3:
                    if (isFull(buf2) is False and elem.rt.readable
                    and elem.rt.writable and elem.base.readable):
                        buf2 = enqueue(buf2,elem)
                        dequeue(buf1,index)
                elif elem.subtype == 4:
                    if (isFull(buf3) is False and elem.dest.readable
                    and elem.dest.writable and elem.src1.readable and elem.src2.readable):
                        buf2 = enqueue(buf3,elem)
                        buf1 = dequeue(buf1,index)
                elif elem.subtype == 5:
                    if elem.type == 2:
                        if (isFull(buf4) is False and registers[elem.dest].readable
                        and registers[elem.dest].writable and registers[elem.src1].readable and registers[elem.src2].readable):
                            buf4 = enqueue(buf4,elem)
                            buf1 = dequeue(buf1,index)
                    elif elem.type == 3:
                        if (isFull(buf4) is False and elem.dest.readable
                        and elem.dest.writable and elem.src.readable):
                            buf4 = enqueue(buf4,elem)
                            buf1 = dequeue(buf1,index)


                    

        b1,b2,b3,b4,b5,b6,b7,b8,b9,b10 = buf1,buf2,buf3,buf4,buf5,buf6,buf7,buf8,buf9,buf10    
        l += 1
        if (fetch.wait == ""): w = ""
        else: w = fetch.wait.name
        if (fetch.exec == ""): e = ""
        else: e = fetch.exec.name
        sim.write("--------------------\nCycle %d:\nIF:\n\tWaiting: %s\n\tExecuted: %s\nBuf1:\n" % (cycle, w, e))
        for x in range(8):
            sim.write("\tEntry %d:" % x)
            if (buf1[x] != None):
                sim.write(" %s\n" % (buf1[x]).name)
            else: sim.write("\n")
        sim.write("Buf2:\n")
        for x in range(2):
            sim.write("\tEntry %d:" % x)
            if (buf2[x] != None):
                sim.write(" %s\n" % buf2[x].name)
            else: sim.write("\n")
        sim.write("Buf3:\n")
        for x in range(2):
            sim.write("\tEntry %d:" % x)
            if (buf3[x] != None):
                sim.write(" %s\n" % buf3[x].name)
            else: sim.write("\n")
        sim.write("Buf4:\n")
        for x in range(2):
            sim.write("\tEntry %d:" % x)
            if (buf4[x] != None):
                sim.write(" %s\n" % buf4[x].name)
            else: sim.write("\n")
        sim.write("Buf5:")
        if (buf5[0] != None):
            sim.write(" %s\n" % buf5[0].name)
        else: sim.write("\n")
        sim.write("Buf6:")
        if (buf6[0] != None):
            sim.write(" %s\n" % buf6[0].name)
        else: sim.write("\n")
        sim.write("Buf7:")
        if (buf7[0] != None):
            sim.write(" %s\n" % buf7[0].name)
        else: sim.write("\n")
        sim.write("Buf8:")
        if (buf8[0] != None):
            sim.write(" %s\n" % buf8[0].name)
        else: sim.write("\n")
        sim.write("Buf9:")
        if (buf9[0] != None):
            sim.write(" %s\n" % buf9[0].name)
        else: sim.write("\n")
        sim.write("Buf10:")
        if (buf10[0] != None):
            sim.write(" %s\n" % buf10[0].name)
        else: sim.write("\n")
        sim.write("\nRegisters")
        for a in range(4):
            if (a < 2):
                sim.write("\nR0%d:\t" % (a*8))
            else:
                sim.write("\nR%d:\t" % (a*8))
            for b in range(7):
                sim.write("%d\t" % registers[a*8+b].value)
            sim.write("%d" % registers[a*8+7].value)
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
        cycle += 1

    index = len(instructions)
    k = 0
    sim.seek(sim.tell() - 1, os.SEEK_SET)
    sim.write('')
    sim.close()
    input.close()