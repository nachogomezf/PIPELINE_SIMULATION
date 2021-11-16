'''
            if (units[dict[FU]].busy is False and elem.src.status == "" and isFull(buf2) is False and ):
                units[dict[FU]].busy = True
                
                units[dict[FU]].op = elem.opcode
                if (elem.type == 1):
                    units[dict[FU]].fi = elem.rt
                    units[dict[FU]].fj = elem.offset
                    units[dict[FU]].fk = elem.base
                    units[dict[FU]].qj = ""
                    units[dict[FU]].qk = results[elem.base]
                elif (elem.type == 2):
                    units[dict[FU]].fi = elem.dest
                    units[dict[FU]].fj = elem.src1
                    units[dict[FU]].fk = elem.src2
                    units[dict[FU]].qj = results[elem.src1.num]
                    units[dict[FU]].qk = results[elem.src2.num]
                elif (elem.type == 3):
                    units[dict[FU]].fi = elem.dest
                    units[dict[FU]].fj = elem.src
                    units[dict[FU]].fk = elem.imm
                    units[dict[FU]].qj = results[elem.src.num]
                    units[dict[FU]].qk = ""
                units[dict[FU]].rj = (units[dict[FU]].qj == "")
                units[dict[FU]].rk = (units[dict[FU]].qk == "")
                elem.src.status = FU

                if (units[dict[FU]].rj and units[dict[FU]].rk):



            
            

            
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
                            buf1 = dequeue(buf1,index)'''


if (dis[c].subtype == 1 and 
                        registers[dis[c].rs].readable is True and
                        registers[dis[c].rd].readable is True):