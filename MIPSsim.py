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
    return (count == len(list))
def isEmpty(list):
    count = 0
    for elem in list:
        if elem is None:
            count += 1
    return (count == len(list))
def getFU(type,subtype):
    if type == 1: return "ALU1"
    if type == 2 and subtype == 4: return "MUL1"
    if type == 2 or type == 3: return "ALU2"


class Instruction1:
    def __init__(self,inst):
        self.stage = ""
        self.pc = 0
        self.res = 0
        self.id = 0
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
            return data
        elif self.opcode == "101":
            registers[self.rt].value = data[(registers[self.base].value+self.offset-firstdata)//4]
            return registers
        elif self.opcode == "110":
            stop = True
            return pc, registers, data, stop
    
class Instruction2:
    def __init__(self,inst):
        self.res = 0
        self.id = 0
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
            return srl(registers[self.src1].value, self.src2)
        elif self.opcode == "101":
            return registers[self.src1].value >> self.src2
        elif self.opcode == "000":
            return registers[self.src1].value + registers[self.src2].value
        elif self.opcode == "001":
            return registers[self.src1].value - registers[self.src2].value
        elif self.opcode == "010":
            return registers[self.src1].value & registers[self.src2].value
        elif self.opcode == "011":
            return registers[self.src1].value | registers[self.src2].value
        elif self.opcode == "110":
            return registers[self.src1].value * registers[self.src2].value

class Instruction3:
    def __init__(self,inst):
        self.id = 0
        self.res = 0
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
            return registers[self.src].value + self.imm
        elif self.opcode == "001":
            return registers[self.src].value & self.imm
        elif self.opcode == "010":
            return registers[self.src].value | self.imm

class Register:

    def __init__(self,num,value,readable=True, writable=True, stage="", status=""):
        self.num = num
        self.value = value
        self.readable = readable
        self.writable = writable
        self.stage = stage
        self.status = status
    
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
    #sim = open("mysim.txt", "w")
    buf1,buf2,buf3,buf4,buf5,buf6,buf7,buf8,buf9,buf10 = [None for i in range(8)],[None for i in range(2)],[None for i in range(2)],[None for i in range(2)],[None],[None],[None],[None],[None],[None]
    fetch = fetchUnit()
    pc = 260
    readList = []
    writeList =[]
    readIds = []
    writeIds = []
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
    dict = { "IS" : 0, "ALU1" : 1, "ALU2" : 2, "MUL1" : 3, "MUL2" : 4, "MUL3" : 5, "MEM" : 6, "WB" : 7}
    for a in units_names: units.append(FunctionalUnit(name=a))
    results = ["" for a in range(32)]
    firstdata = j*4 + 264
    instructions = [None] * (j+1)
    initialdata = [0] * (len(linelist)-j-1)
    data = [0] * (len(linelist)-j-1)
    id = 0
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
    c=0
    cycle=1
    while (stop is False):
        b3consumed, b4consumed, b5consumed, b6consumed, b7consumed, b8consumed, b9consumed, b10consumed = False,False,False,False,False,False,False, False
        for elem in buf1: 
            if elem is not None: elem.consumed = False
        for elem in buf2: 
            if elem is not None: elem.consumed = False
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
        
        

        if fetch.stalled is True and isEmpty(buf1) and fetch.wait != "":
            if ((fetch.wait.subtype == 0 and fetch.wait.rs not in writeList and fetch.wait.rs not in issueWrite)
                or (fetch.wait.subtype == 1 and fetch.wait.rs not in writeList and fetch.wait.rs not in issueWrite and fetch.wait.rd not in writeList and fetch.wait.rd not in issueWrite)
                or (fetch.wait.subtype == -1)): 
                fetch.exec = fetch.wait
                fetch.wait = ""


        '''
        INSTRUCTION FETCH
        
        '''
        fetchRead = []
        fetchWrite = []
        
        for i in range(4):
            if (fetch.stalled is False and fetch.full is False):
                if (dis[c].isBranch is True): 
                    if (dis[c].subtype == 1 and 
                        registers[dis[c].rs].readable is True and
                        registers[dis[c].rd].readable is True):
                        fetch.exec = dis[c]
                        fetch.stalled = False
                        c = (pc-260)//4
                        break
                    elif (dis[c].subtype == -1):
                        fetch.exec = dis[c]
                        pc = dis[c].addr
                        fetch.stalled = False
                        c = (pc-260)//4
                        break
                    else:
                        if ((dis[c].subtype == 1 and dis[c].rs not in writeList and dis[c].rs.readable is True) or (dis[c].subtype == 0 and dis[c].rs not in writeList and dis[c].rs.readable is True and dis[c].rd not in writeList and dis[c].rd.readable is True)):
                            fetch.stalled = False
                            fetch.exec = dis[c]
                            pc, registers, data, stop = fetch.exec.exec(registers, firstdata, data, stop, pc)
                            c = (pc-260)//4
                            break
                        else:
                            fetch.stalled = True
                            fetch.wait = dis[c]
                        break
                else:
                    if (isFull(buf1)):
                        fetch.full = True 
                        break
                    dis[c].consumed = True
                    dis[c].stage = "IF"
                    buf1 = enqueue(buf1,dis[c])
                    if dis[c].type == 1:
                            registers[dis[c].rt].writable = False
                            registers[dis[c].base].readable = False
                            registers[dis[c].base].writable = False
                    elif (dis[c].type == 2):
                        registers[dis[c].src1].writable = False
                        registers[dis[c].src2].writable = False
                        registers[dis[c].dest].readable = False
                        registers[dis[c].dest].writable = False
                    elif (dis[c].type == 3):
                        registers[dis[c].src].writable = False
                        registers[dis[c].dest].readable = False
                        registers[dis[c].dest].writable = False
                    c += 1


        '''
        INSTRUCTION ISSUE
        '''
        issueRead = []
        issueWrite = []
        index = 0

        for elem in buf1:
            elem = buf1[index]
            if elem is None: break
            #check the operands to see possible hazards
            FU = getFU(elem.type,elem.subtype)
            if (elem.type == 1):
                if (elem.consumed is False and isFull(buf2) is False and elem.rt not in writeList and elem.rt not in issueRead and elem.rt not in issueWrite):
                    elem.id = id
                    buf2 = enqueue(buf2,elem)
                    buf1 = dequeue(buf1,index)
                    readList.append(elem.base)
                    readIds.append(id)
                    writeList.append(elem.rt)
                    writeIds.append(id)
                    elem.consumed = True
                    index -= 1
                    id += 1
                issueRead.append(elem.base)
                issueWrite.append(elem.rt)
            elif (elem.type == 2 and elem.subtype != 4):
                if (elem.consumed is False and isFull(buf3) is False and elem.dest not in writeList and elem.dest not in issueWrite and elem.dest not in issueRead and elem.src1 not in writeList and elem.src2 not in writeList and elem.src1 not in issueWrite and elem.src2 not in issueWrite):
                    elem.id = id
                    buf3 = enqueue(buf3,elem)
                    buf1 = dequeue(buf1,index)
                    readList.append(elem.src1)
                    writeList.append(elem.dest)
                    readList.append(elem.src2)
                    readIds.append(id)
                    readIds.append(id)
                    writeIds.append(id)
                    elem.consumed = True
                    index -= 1
                    id += 1
                issueRead.append(elem.src1)
                issueRead.append(elem.src2)
                issueWrite.append(elem.dest)
            elif (elem.subtype == 4):
                if (elem.consumed is False and isFull(buf4) is False and elem.dest not in writeList and elem.dest not in issueWrite and elem.dest not in issueRead and elem.src1 not in writeList and elem.src2 not in writeList and elem.src1 not in issueWrite and elem.src2 not in issueWrite):
                    elem.id = id
                    buf4 = enqueue(buf4,elem)
                    buf1 = dequeue(buf1,index)
                    readList.append(elem.src1)
                    writeList.append(elem.dest)
                    readList.append(elem.src2)
                    readIds.append(id)
                    readIds.append(id)
                    writeIds.append(id)
                    elem.consumed = True
                    index -= 1
                    id += 1
            elif (elem.type == 3):
                if (elem.consumed is False and isFull(buf3) is False and elem.dest not in writeList and elem.dest not in issueWrite and elem.dest not in issueRead
                and elem.src not in writeList and elem.src not in issueWrite):
                    elem.id = id
                    buf3 = enqueue(buf3,elem)
                    buf1 = dequeue(buf1,index)
                    readList.append(elem.src)
                    writeList.append(elem.dest)
                    readIds.append(id)
                    writeIds.append(id)
                    elem.consumed = True
                    id += 1
                index -= 1
                issueRead.append(elem.src)
                issueWrite.append(elem.dest)
            index += 1

        if (len(buf2) != 0 and buf2[0] is not None):

            '''for a in buf6:
                if a is not None:
                    mapping = [n for n, x in enumerate(readIds) if x == a.id]
                    readList = readList[:mapping[0]] + readList[mapping[0]+1:]
                    readIds = readIds[:mapping[0]] + readIds[mapping[0]+1:]'''
            if (buf2[0].consumed is False):
                buf2[0].consumed = True
                #buf2[0].res = buf2[0].exec(pc,registers,data,stop)
                if (isFull(buf5)): buf5.append(buf2[0])
                else: buf5 = enqueue(buf5, buf2[0])
                buf2 = dequeue(buf2, 0)
        
        if (len(buf3) != 0 and buf3[0] is not None):
            '''for a in buf6:
                if a is not None:
                    mapping = [n for n, x in enumerate(readIds) if x == a.id]
                    if a.type == 3:
                        readList = readList[:mapping[0]] + readList[mapping[0]+1:]
                        readIds = readIds[:mapping[0]] + readIds[mapping[0]+1:]
                    else:
                        readIds = readIds[:min(mapping)] + readIds[max(mapping)+1:]
                        readList = readList[:mapping[0]] + readList[mapping[0]+1:]'''
            if (buf3[0].consumed is False and b3consumed is False):
                b3consumed = True
                buf3[0].consumed = True
                buf3[0].res = buf3[0].exec(registers)
                buf3[0].name = "[%d, R%s]" % (buf3[0].dest, buf3[0].res)
                if (isFull(buf6)): buf6.append(buf3[0])
                else: buf6 = enqueue(buf6, buf3[0])
                buf3 = dequeue(buf3,0)
        
        if (len(buf4) != 0 and buf4[0] is not None and b4consumed is False):
            '''for a in buf4:
                if a is not None:
                    mapping = [n for n, x in enumerate(readIds) if x == a.id]
                    readIds = readIds[:min(mapping)] + readIds[max(mapping)+1:]
                    readList = readList[:min(mapping)] + readList[max(mapping)+1:]'''
            if (buf4[0].consumed is False):
                b4consumed = True
                buf4[0].consumed = True
                buf4[0].res = buf4[0].exec(registers)
                if (isFull(buf7)): buf7.append(buf4[0])
                else: buf7 = enqueue(buf7,buf4[0])
                buf4 = dequeue(buf4,0)
        
        if (len(buf5) != 0 and buf5[0] is not None and b5consumed is False):
            if (buf5[0].consumed is False):
                b5consumed = True
                buf5[0].consumed = True
                if (buf5[0].subtype == 2):
                    buf5[0].name = ""
                    data = buf5[0].exec(registers,firstdata,data,stop,pc)
                elif (buf5[0].subtype == 3):
                    buf5[0].name = "[%d, R%s]" % (data[(registers[buf5[0].base].value+buf5[0].offset-firstdata)//4], buf5[0].rt)
                if (isFull(buf8)): buf8.append(buf5[0])
                else: buf8 = enqueue(buf8,buf5[0])
                buf5 = dequeue(buf5,0)
        
        if (len(buf6) != 0 and buf6[0] is not None and b6consumed is False):
            if (buf6[0].consumed is False):
                b6consumed = True
                buf6[0].consumed = True
                registers[buf6[0].dest].value = buf6[0].res
                mapping = writeIds.index(buf6[0].id)
                writeIds = writeIds[:mapping] + writeIds[mapping+1:]
                writeList = writeList[:mapping] + writeList[mapping+1:]
                if (buf6[0].type == 1 and (buf6[0].subtype == 2 or buf6[0].subtype == 3)): #TODO borrar?
                    registers[buf6[0].rs].writable = True
                    registers[buf6[0].rd].readable = True
                    registers[buf6[0].rd].writable = True
                elif (dis[c].type == 2):
                    buf6[0].name = "[%d, %s]" % (buf6[0].dest, buf6[0].res)
                    registers[buf6[0].src1].writable = True
                    registers[buf6[0].src2].writable = True
                    registers[buf6[0].dest].readable = True
                    registers[buf6[0].dest].writable = True
                elif (dis[c].type == 3):
                    buf6[0].name = "[%d, %s]" % (buf6[0].dest, buf6[0].res)
                    registers[buf6[0].src].writable = True
                    registers[buf6[0].dest].readable = True
                    registers[buf6[0].dest].writable = True
                if len(buf6) == 1: buf6[0] = None
                elif len(buf6) == 2: buf6.pop(0)
                pc += 4

        if (len(buf7) != 0 and buf7[0] is not None and b7consumed is False):
            if (buf7[0].consumed is False):
                b7consumed = True
                buf7[0].consumed = True
                if (isFull(buf9)): buf9.append(buf7[0])
                else: buf9 = enqueue(buf9,buf7[0])
                buf7 = dequeue(buf7,0)
        
        if (len(buf8) != 0 and buf8[0] is not None and b8consumed is False):
            if (buf8[0].consumed is False):
                b8consumed = True
                buf8[0].consumed = True
                if (buf8[0].subtype == 3):
                    registers[buf8[0].rt].value = data[(registers[buf8[0].base].value+buf8[0].offset-firstdata)//4]
                    #registers = buf8[0].exec
                mapping = writeIds.index(buf8[0].id)
                writeIds = writeIds[:mapping] + writeIds[mapping+1:]
                writeList = writeList[:mapping] + writeList[mapping+1:]
                buf8 = dequeue(buf8,0)
                pc += 4

        if (len(buf9) != 0 and buf9[0] is not None and b9consumed is False):
            if (buf9[0].consumed is False):
                b9consumed = True
                buf9[0].consumed = True
                buf9[0].name = "[%d, R%s]" % (buf9[0].res, buf9[0].dest)
                if (isFull(buf10)): buf10.append(buf9[0])
                else: buf10 = enqueue(buf10,buf9[0])
                buf9 = dequeue(buf9,0)
        
        if (len(buf10) != 0 and buf10[0] is not None and b10consumed is False):
            if (buf10[0].consumed is False):
                b10consumed = True
                buf10[0].consumed = True
                registers[buf10[0].dest].value = buf10[0].res
                '''mapping = [n for n, x in enumerate(readIds) if x == buf10[0].id]
                readList = readList[:mapping[0]] + readList[mapping[0]+1:]
                readIds = readIds[:mapping[0]] + readIds[mapping[0]+1:]'''
                mapping = writeIds.index(buf10[0].id)
                writeIds = writeIds[:mapping] + writeIds[mapping+1:]
                writeList = writeList[:mapping] + writeList[mapping+1:]
                registers[buf10[0].src1].writable = True
                registers[buf10[0].src2].writable = True
                registers[buf10[0].dest].readable = True
                registers[buf10[0].dest].writable = True
                buf10 = dequeue(buf10,0)
                pc += 4

        if fetch.exec != "":
            if fetch.exec.subtype != -1:
                fetch.stalled = False
                pc, registers, data, stop = fetch.exec.exec(registers, firstdata, data, stop, pc)
                c = (pc-260)//4
        
        

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
        fetch.exec= ""

    index = len(instructions)
    k = 0
    sim.seek(sim.tell() - 1, os.SEEK_SET)
    sim.write('')
    sim.close()
    input.close()