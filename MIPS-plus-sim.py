import math
memory = [0] *4096 #Remember when ever you get an address in hex subtract 8192 from it then write to it
				#Dynamic Instruction Count
registers = {"$0": 0, "$8":0,"$9": 0, "$10":0,"$11": 0, 
                  "$12":0,"$13": 0, "$14":0,"$15": 0, "$16":0,"$17": 0, 
                  "$18":0,"$19": 0, "$20":0,"$21": 0, "$22":0,"$23": 0, "$lo":0,"$hi":0}




ft = {"instr": " ", "type": " ", "stall": 0, "name": " ", "nop": 2, "branch": 0,
            "reghold": {"rs": " ", "rd": " ", "rt": " "},
            "fowarding": {"instr": "", "reg": " ", "regval": 0}

            }

de = {"instr": " ", "type": " ", "stall": 0, "name": " ", "nop": 2, "branch": 0,
            "reghold": {"rs": " ", "rd": " ", "rt": " "},
            "fowarding": {"instr": "", "reg": " ", "regval": 0}

            }

ex = {"instr": " ", "type": " ", "stall": 0, "name": " ", "nop": 2, "branch": 0,
            "reghold": {"rs": " ", "rd": " ", "rt": " "},
            "fowarding": {"instr": "", "reg": " ", "regval": 0}

            }

m = {"instr": " ", "type": " ", "stall": 0, "name": " ", "nop": 2, "branch": 0,
            "reghold": {"rs": " ", "rd": " ", "rt": " "},
            "fowarding": {"instr": "", "reg": " ", "regval": 0}

            }

wb = {"instr": " ", "type": " ", "stall": 0, "name": " ", "nop": 2, "branch": 0,
            "reghold": {"rs": " ", "rd": " ", "rt": " "},
            "fowarding": {"instr": "", "reg": " ", "regval": 0}
            }


controlSignals = {"AluScrA":0,"AluScrB":'01',"MemWrite":0,"RegDst":0,"MemtoReg":0,"RegWrite":0,"Branch":0, "c3":0, c4:0, "c5":0}

labelIndex = []
labelName = []
pcAssign= []


def multiCycle(instrs, DIC, pc, cycles):
    cycle1=0
    cycle2=0
    cycle3=0
    cycle4=0
    cycle5=0
    while True:
        cycles= cycle1+ cycle2+ cycle3+ cycle4+ cycle5
        l = instrs[int(pc/4)]
        if (int(pc/4) >= len(instrs)):
            print("Dynamic Instruction Count: ",DIC)
            return DIC, pc, cycles;
        DIC+=1
        #cycle1
        cycle1+=1
        controlSignals["AluScrA"]+=0
        controlSignals["AluScrB"]='01'
        #controlSignals["PCSrc"]=0
        #controlSignals["IorD"]=0
       # controlSignals["AluOp"]='00'
       # controlSignals["IRWrite"]=1
        #controlSignals["PCWrite"]=1
        #pc=pc+4
   #cycle2  
        cycle2+=1
        controlSignals["AluScrA"]+=0 
        controlSignals["AluScrB"]='11'
       # controlSignals["AluOp"]='00'
        if "w" in l:
       #cycle3 
            cycle3+=1
            controlSignals["AluScrA"]+=1
            controlSignals["AluScrB"]='10'
           # controlSignals["AluOp"]='00'
       #cycle4
            pc= instrExecution(l, pc)
            #controlSignals["IorD"]=0
            cycle4+=1
            if "sw" in l:
                controlSignals["c4"]+=1
                controlSignals["MemWrite"]+=1
            else:
                 cycle5+=1
                 controlSignals["c5"]+=1
                 controlSignals["RegDst"]+= 0
                 controlSignals["MemtoReg"]+=1
                 controlSignals["RegWrite"]+=1
        elif "bne" or "beq" in l:
      #cycle3 
            cycle3+=1
            controlSignals["c3"]+=1
            controlSignals["AluScrA"]+= 1
            controlSignals["AluScrB"]='10'
          #  controlSignals["AluOp"]='01'
           # controlSignals["PCSrc"]=1
            controlSignals["Branch"]+=1
            pc= instrExecution(l, pc)
        else:
            controlSignals["c4"]+=1
            if "i" in l:    
           #cycle3
                cycle3+=1
                controlSignals["AluScrA"]+= 1
                controlSignals["AluScrB"]='10'
              #  controlSignals["AluOp"]='10'
                #cycle4
                cycle4+=1
                pc= instrExecution(l, pc)
                controlSignals["RegDst"]+= 0
                controlSignals["MemtoReg"]+=0
                controlSignals["RegWrite"]+=1
            else:
                controlSignals["AluScrA"]+=1 
                controlSignals["AluScrB"]='00'
              #  controlSignals["AluOp"]='10'
                #cycle4
                cycle4+=1
                pc= instrExecution(l, pc)
                controlSignals["RegDst"]+= 1
                controlSignals["MemtoReg"]+=0
                controlSignals["RegWrite"]+=1
           

    
def pipeline(instrs, DIC, pc, cycles, diagnostic):
    while True:

        l = instrs[int(pc / 4)]
        currentpc = pc
        if (int(pc / 4) >= len(instrs)):
            print("Dynamic Instruction Count: ", DIC)
            return DIC, pc, cycles;
        DIC += 1

        cycles += 1

        wb = m

        m = ex

        ex = de

        de = ft

        pc = instrExecution(l, pc)
        ft["instr"] = l
        ft["nop"] = 0
        if "w" in l:
            ft["type"] = "i"
        elif "i" in l:
            ft["type"] = "i"
        else:
            ft["type"] = "r"

        tmp = l
        tmp = tmp.replace(",", "")
        tmp = tmp.split("")
        i = 0

        while tmp[i].isalpha():
            inst = inst + tmp[i]
            i += 1

        ft["name"] = inst
        while i >= 0:
            tmp.pop(0)
            i -= 1

        regs = tmp
        if ft["name"] == "lw" or "sw":
            ft["reghold"]["rt"] = regs[0]
            ft["reghold"]["rs"] = regs[2]
        elif ft["type"] == "i" and ft["name"] != "bne" or "beq":
            ft["reghold"]["rt"] = regs[0]
            ft["reghold"]["rs"] = regs[1]
        elif ft["type"] == "r":
            ft["reghold"]["rd"] = regs[0]
            ft["reghold"]["rs"] = regs[1]
            ft["reghold"]["rt"] = regs[2]
        else:
            ft["reghold"]["rs"] = regs[0]
            ft["reghold"]["rt"] = regs[1]

        ft["branch"] = 0
        ft["stall"] = 0
        if "lw" in l:
            ft["stall"] = 1
        elif "beq" in l:
            if currentpc + 4 != pc:
                ft["branch"] = 1
            else:
                ft["branch"] = 0

            if de["type"] == "i" and de["name"] != "sw":
                if ft["reghold"]["rs"] == de["reghold"]["rt"]:
                    if de["name"] == "lw":
                        de["stall"] = 2
                    else:
                        de["stall"] = 1
                if ft["reghold"]["rt"] == de["reghold"]["rt"]:
                    if de["name"] == "lw":
                        de["stall"] = 2
                    else:
                        de["stall"] = 1
            elif de["type"] == "r":
                if ft["reghold"]["rs"] == de["reghold"]["rd"]:
                    de["stall"] = 1
                elif ft["reghold"]["rt"] == de["reghold"]["rd"]:
                    de["stall"] = 1
        else:
            ft["branch"] = 0
            ft["stall"] = 0
            ft["nop"] = 0

        if diagnostic == 1:

            print("current instruction's in each cycle and fowarding path")
            if ft["nop"] == 1:
                fetch = "bubble stall"
            elif ft["nop"] == 2:
                fetch = "empty"
            elif ft["nop"] == 3:
                fetch = "bubble flush"
            else:
                fetch = ft["instr"]

            if de["nop"] == 1:
                decode = "bubble"
            elif de["nop"] == 2:
                decode = "empty"
            elif de["nop"] == 3:
                decode = "bubble flush"
            else:
                decode = ft["instr"]

            if ex["nop"] == 1:
                execution = "bubble"
            elif ex["nop"] == 2:
                execution = "empty"
            elif ex["nop"] == 3:
                execution = "bubble flush"
            else:
                execution = ft["instr"]

            if m["nop"] == 1:
                mem = "bubble"
            elif m["nop"] == 2:
                mem = "empty"
            elif m["nop"] == 3:
                mem = "bubble flush"
            else:
                mem = ft["instr"]
            aluoutm1 = 0
            aluoutm2 = 0
            if m["type"] == "i" and m["name"] != "sw" or "lw":
                if ex["reghold"]["rs"] == m["reghold"]["rt"]:
                    aluoutm1 = 1
                    print("ALUOutM -> srcAE")
                if ft["reghold"]["rt"] == de["reghold"]["rt"]:
                    if ex["name"] == "sw":
                        aluoutm2 = 1
                        print("ALUOutM ‐> WriteDataE")
                    else:
                        aluoutm2 = 1
                        print("ALUOutM -> srcBE")

            if m["type"] == "r":
                if ex["reghold"]["rs"] == m["reghold"]["rd"]:
                    aluoutm1 = 1
                    print("ALUOutM -> srcAE")
                if ex["reghold"]["rt"] == m["reghold"]["rd"]:
                    if ex["name"] == "sw":
                        aluoutm2 = 1
                        print("ALUOutM ‐> WriteDataE")
                    else:
                        aluoutm2 = 1
                        print("ALUOutM -> srcBE")

            if de["name"] == "beq" or "bne" :
                if m["type"] == "r" and m["reghold"]["rd"] == de["reghold"]["rs"] or de["reghold"]["rt"]:
                    print("ALUOutM -> EqualD")
                if m["type"] == "i" and m["name"] != "sw" or "sw" and m["reghold"]["rt"] == de["reghold"]["rs"] or de["reghold"]["rt"]:
                    print("ALUOutM -> EqualD")


            if wb["nop"] == 1:
                writeBack = "bubble"
            elif wb["nop"] == 2:
                writeBack = "empty"
            elif wb["nop"] == 3:
                writeBack = "bubble flush"

            if wb["type"] == "i" and wb["name"] != "sw":
                if ex["reghold"]["rs"] == wb["reghold"]["rt"] and aluoutm1 != 1:
                    print("ALUOutM -> srcAE")
                if ex["reghold"]["rt"] == wb["reghold"]["rt"] and aluoutm2 != 1:
                    if ex["name"] == "sw":
                        print("ALUOutM ‐> WriteDataE")
                    else:
                        print("ALUOutM -> srcBE")

            if m["type"] == "r":
                if ex["reghold"]["rs"] == m["reghold"]["rd"]:
                    print("ALUOutM -> srcAE")
                if ex["reghold"]["rt"] == m["reghold"]["rd"]:
                    if ex["name"] == "sw":
                        print("ALUOutM ‐> WriteDataE")
                    else:
                        print("ALUOutM -> srcBE")

            if de["name"] == "beq" or "bne" :
                if m["type"] == "r" and m["reghold"]["rd"] == de["reghold"]["rs"] or de["reghold"]["rt"]:
                    print("ALUOutM -> EqualD")
                if m["type"] == "i" and m["name"] != "sw" or "sw" and m["reghold"]["rt"] == de["reghold"]["rs"] or de["reghold"]["rt"]:
                    print("ALUOutM -> EqualD")

            else:
                writeBack = ft["instr"]

            print("fetch: " + fetch + "decode: " + decode + "execution: " + execution + "memory: " + mem + "write back: " + writeBack)
            input("press enter to continue")


        if ex["stall"] == 2:
            cycles += 1
            wb = m
            m = ex
            ex["nop"] = 1

            if diagnostic == 1:

                print("current instruction's in each cycle")
                if ft["nop"] == 1:
                    fetch = "bubble stall"
                elif ft["nop"] == 2:
                    fetch = "empty"
                elif ft["nop"] == 3:
                    fetch = "bubble flush"
                else:
                    fetch = ft["instr"]

                if de["nop"] == 1:
                    decode = "bubble"
                elif de["nop"] == 2:
                    decode = "empty"
                elif de["nop"] == 3:
                    decode = "bubble flush"
                else:
                    decode = ft["instr"]

                if ex["nop"] == 1:
                    execution = "bubble"
                elif ex["nop"] == 2:
                    execution = "empty"
                elif ex["nop"] == 3:
                    execution = "bubble flush"
                else:
                    execution = ft["instr"]

                if m["nop"] == 1:
                    mem = "bubble"
                elif m["nop"] == 2:
                    mem = "empty"
                elif m["nop"] == 3:
                    mem = "bubble flush"
                else:
                    mem = ft["instr"]

                if wb["nop"] == 1:
                    writeBack = "bubble"
                elif wb["nop"] == 2:
                    writeBack = "empty"
                elif wb["nop"] == 3:
                    writeBack = "bubble flush"
                else:
                    writeBack = ft["instr"]

                print(
                    "fetch: " + fetch + "decode: " + decode + "execution: " + execution + "memory: " + mem + "write back: " + writeBack)
                input("press enter to continue")
            cycles += 1
            wb = m
            m["nop"] = 1
            if diagnostic == 1:

                print("current instruction's in each cycle")
                if ft["nop"] == 1:
                    fetch = "bubble stall"
                elif ft["nop"] == 2:
                    fetch = "empty"
                elif ft["nop"] == 3:
                    fetch = "bubble flush"
                else:
                    fetch = ft["instr"]

                if de["nop"] == 1:
                    decode = "bubble"
                elif de["nop"] == 2:
                    decode = "empty"
                elif de["nop"] == 3:
                    decode = "bubble flush"
                else:
                    decode = ft["instr"]

                if ex["nop"] == 1:
                    execution = "bubble"
                elif ex["nop"] == 2:
                    execution = "empty"
                elif ex["nop"] == 3:
                    execution = "bubble flush"
                else:
                    execution = ft["instr"]

                if m["nop"] == 1:
                    mem = "bubble"
                elif m["nop"] == 2:
                    mem = "empty"
                elif m["nop"] == 3:
                    mem = "bubble flush"
                else:
                    mem = ft["instr"]

                if wb["nop"] == 1:
                    writeBack = "bubble"
                elif wb["nop"] == 2:
                    writeBack = "empty"
                elif wb["nop"] == 3:
                    writeBack = "bubble flush"
                else:
                    writeBack = ft["instr"]

                print(
                    "fetch: " + fetch + "decode: " + decode + "execution: " + execution + "memory: " + mem + "write back: " + writeBack)
                input("press enter to continue")

        if ex["stall"] == 1:
            cycles += 1
            wb = m
            m = ex
            ex["nop"] = 1
            if diagnostic == 1:

                print("current instruction's in each cycle")
                if ft["nop"] == 1:
                    fetch = "bubble stall"
                elif ft["nop"] == 2:
                    fetch = "empty"
                elif ft["nop"] == 3:
                    fetch = "bubble flush"
                else:
                    fetch = ft["instr"]

                if de["nop"] == 1:
                    decode = "bubble"
                elif de["nop"] == 2:
                    decode = "empty"
                elif de["nop"] == 3:
                    decode = "bubble flush"
                else:
                    decode = ft["instr"]

                if ex["nop"] == 1:
                    execution = "bubble"
                elif ex["nop"] == 2:
                    execution = "empty"
                elif ex["nop"] == 3:
                    execution = "bubble flush"
                else:
                    execution = ft["instr"]

                if m["nop"] == 1:
                    mem = "bubble"
                elif m["nop"] == 2:
                    mem = "empty"
                elif m["nop"] == 3:
                    mem = "bubble flush"
                else:
                    mem = ft["instr"]

                if wb["nop"] == 1:
                    writeBack = "bubble"
                elif wb["nop"] == 2:
                    writeBack = "empty"
                elif wb["nop"] == 3:
                    writeBack = "bubble flush"
                else:
                    writeBack = ft["instr"]

                print(
                    "fetch: " + fetch + "decode: " + decode + "execution: " + execution + "memory: " + mem + "write back: " + writeBack)
                input("press enter to continue")

        if ft["branch"] == 1:
            cycles += 1
            wb = m
            m = ex
            ex = de
            de = ft


            l = instrs[int(currentpc + 4 / 4)]
            ft["instr"] = l
            tmp = l
            tmp = tmp.replace(",", "")
            tmp = tmp.split("")
            i = 0

            while tmp[i].isalpha():
                inst = inst + tmp[i]
                i += 1

            ft["name"] = inst
            while i >= 0:
                tmp.pop(0)
                i -= 1

            regs = tmp
            if ft["name"] == "lw" or "sw":
                ft["reghold"]["rt"] = regs[0]
                ft["reghold"]["rs"] = regs[2]
            elif ft["type"] == "i" and ft["name"] != "bne" or "beq":
                ft["reghold"]["rt"] = regs[0]
                ft["reghold"]["rs"] = regs[1]
            elif ft["type"] == "r":
                ft["reghold"]["rd"] = regs[0]
                ft["reghold"]["rs"] = regs[1]
                ft["reghold"]["rt"] = regs[2]
            else:
                ft["reghold"]["rs"] = regs[0]
                ft["reghold"]["rt"] = regs[1]
            ft["branch"] = 0
            ft["stall"] = 0
            ft["nop"] = 0

            if diagnostic == 1:

                print("current instruction's in each cycle")
                if ft["nop"] == 1:
                    fetch = "bubble stall"
                elif ft["nop"] == 2:
                    fetch = "empty"
                elif ft["nop"] == 3:
                    fetch = "bubble flush"
                else:
                    fetch = ft["instr"]

                if de["nop"] == 1:
                    decode = "bubble"
                elif de["nop"] == 2:
                    decode = "empty"
                elif de["nop"] == 3:
                    decode = "bubble flush"
                else:
                    decode = ft["instr"]

                if ex["nop"] == 1:
                    execution = "bubble"
                elif ex["nop"] == 2:
                    execution = "empty"
                elif ex["nop"] == 3:
                    execution = "bubble flush"
                else:
                    execution = ft["instr"]

                if m["nop"] == 1:
                    mem = "bubble"
                elif m["nop"] == 2:
                    mem = "empty"
                elif m["nop"] == 3:
                    mem = "bubble flush"
                else:
                    mem = ft["instr"]

                if wb["nop"] == 1:
                    writeBack = "bubble"
                elif wb["nop"] == 2:
                    writeBack = "empty"
                elif wb["nop"] == 3:
                    writeBack = "bubble flush"
                else:
                    writeBack = ft["instr"]

                print(
                    "fetch: " + fetch + "decode: " + decode + "execution: " + execution + "memory: " + mem + "write back: " + writeBack)
                input("press enter to continue")

            ft["nop"] = 3
        if (int(pc / 4) >= len(instrs)):
            cycles += 1
            wb = m
            m = ex
            ex = de
            de = ft
            ft["nop"] = 2

            if diagnostic == 1:

                print("current instruction's in each cycle")
                if ft["nop"] == 1:
                    fetch = "bubble stall"
                elif ft["nop"] == 2:
                    fetch = "empty"
                elif ft["nop"] == 3:
                    fetch = "bubble flush"
                else:
                    fetch = ft["instr"]

                if de["nop"] == 1:
                    decode = "bubble"
                elif de["nop"] == 2:
                    decode = "empty"
                elif de["nop"] == 3:
                    decode = "bubble flush"
                else:
                    decode = ft["instr"]

                if ex["nop"] == 1:
                    execution = "bubble"
                elif ex["nop"] == 2:
                    execution = "empty"
                elif ex["nop"] == 3:
                    execution = "bubble flush"
                else:
                    execution = ft["instr"]

                if m["nop"] == 1:
                    mem = "bubble"
                elif m["nop"] == 2:
                    mem = "empty"
                elif m["nop"] == 3:
                    mem = "bubble flush"
                else:
                    mem = ft["instr"]

                if wb["nop"] == 1:
                    writeBack = "bubble"
                elif wb["nop"] == 2:
                    writeBack = "empty"
                elif wb["nop"] == 3:
                    writeBack = "bubble flush"
                else:
                    writeBack = ft["instr"]

                print(
                    "fetch: " + fetch + "decode: " + decode + "execution: " + execution + "memory: " + mem + "write back: " + writeBack)
                input("press enter to continue")
            cycles += 1
            wb = m
            m = ex
            ex = de
            de["nop"] = 2

            if diagnostic == 1:

                print("current instruction's in each cycle")
                if ft["nop"] == 1:
                    fetch = "bubble stall"
                elif ft["nop"] == 2:
                    fetch = "empty"
                elif ft["nop"] == 3:
                    fetch = "bubble flush"
                else:
                    fetch = ft["instr"]

                if de["nop"] == 1:
                    decode = "bubble"
                elif de["nop"] == 2:
                    decode = "empty"
                elif de["nop"] == 3:
                    decode = "bubble flush"
                else:
                    decode = ft["instr"]

                if ex["nop"] == 1:
                    execution = "bubble"
                elif ex["nop"] == 2:
                    execution = "empty"
                elif ex["nop"] == 3:
                    execution = "bubble flush"
                else:
                    execution = ft["instr"]

                if m["nop"] == 1:
                    mem = "bubble"
                elif m["nop"] == 2:
                    mem = "empty"
                elif m["nop"] == 3:
                    mem = "bubble flush"
                else:
                    mem = ft["instr"]

                if wb["nop"] == 1:
                    writeBack = "bubble"
                elif wb["nop"] == 2:
                    writeBack = "empty"
                elif wb["nop"] == 3:
                    writeBack = "bubble flush"
                else:
                    writeBack = ft["instr"]

                print(
                    "fetch: " + fetch + "decode: " + decode + "execution: " + execution + "memory: " + mem + "write back: " + writeBack)
                input("press enter to continue")

            cycles += 1
            wb = m
            m = ex
            ex["nop"] = 2

            if diagnostic == 1:

                print("current instruction's in each cycle")
                if ft["nop"] == 1:
                    fetch = "bubble stall"
                elif ft["nop"] == 2:
                    fetch = "empty"
                elif ft["nop"] == 3:
                    fetch = "bubble flush"
                else:
                    fetch = ft["instr"]

                if de["nop"] == 1:
                    decode = "bubble"
                elif de["nop"] == 2:
                    decode = "empty"
                elif de["nop"] == 3:
                    decode = "bubble flush"
                else:
                    decode = ft["instr"]

                if ex["nop"] == 1:
                    execution = "bubble"
                elif ex["nop"] == 2:
                    execution = "empty"
                elif ex["nop"] == 3:
                    execution = "bubble flush"
                else:
                    execution = ft["instr"]

                if m["nop"] == 1:
                    mem = "bubble"
                elif m["nop"] == 2:
                    mem = "empty"
                elif m["nop"] == 3:
                    mem = "bubble flush"
                else:
                    mem = ft["instr"]

                if wb["nop"] == 1:
                    writeBack = "bubble"
                elif wb["nop"] == 2:
                    writeBack = "empty"
                elif wb["nop"] == 3:
                    writeBack = "bubble flush"
                else:
                    writeBack = ft["instr"]

                print(
                    "fetch: " + fetch + "decode: " + decode + "execution: " + execution + "memory: " + mem + "write back: " + writeBack)
                input("press enter to continue")

            cycles += 1
            wb = m
            m["nop"] = 2

            if diagnostic == 1:

                print("current instruction's in each cycle")
                if ft["nop"] == 1:
                    fetch = "bubble stall"
                elif ft["nop"] == 2:
                    fetch = "empty"
                elif ft["nop"] == 3:
                    fetch = "bubble flush"
                else:
                    fetch = ft["instr"]

                if de["nop"] == 1:
                    decode = "bubble"
                elif de["nop"] == 2:
                    decode = "empty"
                elif de["nop"] == 3:
                    decode = "bubble flush"
                else:
                    decode = ft["instr"]

                if ex["nop"] == 1:
                    execution = "bubble"
                elif ex["nop"] == 2:
                    execution = "empty"
                elif ex["nop"] == 3:
                    execution = "bubble flush"
                else:
                    execution = ft["instr"]

                if m["nop"] == 1:
                    mem = "bubble"
                elif m["nop"] == 2:
                    mem = "empty"
                elif m["nop"] == 3:
                    mem = "bubble flush"
                else:
                    mem = ft["instr"]

                if wb["nop"] == 1:
                    writeBack = "bubble"
                elif wb["nop"] == 2:
                    writeBack = "empty"
                elif wb["nop"] == 3:
                    writeBack = "bubble flush"
                else:
                    writeBack = ft["instr"]

                print(
                    "fetch: " + fetch + "decode: " + decode + "execution: " + execution + "memory: " + mem + "write back: " + writeBack)
                input("press enter to continue")

            cycles += 1
            wb["nop"] = 2

            if diagnostic == 1:

                print("current instruction's in each cycle")
                if ft["nop"] == 1:
                    fetch = "bubble stall"
                elif ft["nop"] == 2:
                    fetch = "empty"
                elif ft["nop"] == 3:
                    fetch = "bubble flush"
                else:
                    fetch = ft["instr"]

                if de["nop"] == 1:
                    decode = "bubble"
                elif de["nop"] == 2:
                    decode = "empty"
                elif de["nop"] == 3:
                    decode = "bubble flush"
                else:
                    decode = ft["instr"]

                if ex["nop"] == 1:
                    execution = "bubble"
                elif ex["nop"] == 2:
                    execution = "empty"
                elif ex["nop"] == 3:
                    execution = "bubble flush"
                else:
                    execution = ft["instr"]

                if m["nop"] == 1:
                    mem = "bubble"
                elif m["nop"] == 2:
                    mem = "empty"
                elif m["nop"] == 3:
                    mem = "bubble flush"
                else:
                    mem = ft["instr"]

                if wb["nop"] == 1:
                    writeBack = "bubble"
                elif wb["nop"] == 2:
                    writeBack = "empty"
                elif wb["nop"] == 3:
                    writeBack = "bubble flush"
                else:
                    writeBack = ft["instr"]

                print(
                    "fetch: " + fetch + "decode: " + decode + "execution: " + execution + "memory: " + mem + "write back: " + writeBack)
                input("press enter to continue")

def instrExecution(line, pc):
   #pc = int(0)
        #bcount=0
   #DIC = int(0)
        j= int(0)
   
        #bcount+=1

       # num= len(instrs)
        #if (int(pc/4) >= len(instrs)):
           
         #   print("Dynamic Instruction Count: ",DIC)
          #  return DIC, pc;
        #line = instrs[int(pc/4)]
        print("Current instruction PC =",pc)
        #DIC+=1
        if(line[0:4] == "addi"): # ADDI/U 
            line = line.replace("addi","")
            if(line[0:1] == "u"):
               line = line.replace("u","")
               op = '001001'
            else:
                op = '001000'
            line = line.split(",")
            if(line[2][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[2],n) if (int(line[2],n) >= 0 or op == '001000') else (65536 + int(line[2],n)) # will get the negative or positive inter value. if unsigned and negative will get the unsigned value of th negative integer.
            rs = registers[("$" + str(line[1]))] # reads the value from specified register
            rt = "$" + str(line[0]) # locate the register in which to write to
            instruction = "addi" if(op == '001000') else "addiu"
            print (instruction , rt ,("$" + str(line[1])), imm if(n== 10) else hex(imm))
            result = rs + imm # does the addition operation
            registers[rt]= result # writes the value to the register specified
            print ("result:" ,rt ,"=",  hex(result))
            pc += 4# increments pc by 4 
           # pcprint = hex(pc)
           # print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint)

        elif(line[0:3] == "lui"): #lui 
            line = line.replace("lui","")
            line = line.split(",")
            if(line[1][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[1],n) if (int(line[1],n) >= 0) else (65536 + int(line[2],n)) # will get the negative or positive inter value. if unsigned and negative will get the unsigned value of th negative integer.
            rd = "$" + str(line[0]) # locate the register in which to write to
            instruction = "lui"
            print (instruction , rd, imm if(n== 10) else hex(imm))
            imm = imm << 16
            registers[rd] = imm #Write upper imm to rd designation
            print ("result:",rd ,"=", hex(imm))
            pc += 4# increments pc by 4 
            
            

        elif(line[0:2] == "sw"): # sw
            line = line.replace("sw","")
            line = line.replace(")","")
            line = line.replace("(",",")
            line = line.split(",")
            if(line[1][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[1],n) if (int(line[1],n) >= 0) else (65536 + int(line[1],n))
            rs = int(registers[("$" + str(line[2]))])
            rt = registers[("$" + str(line[0]))]
            instruction = "sw"
            print (instruction , ("$" + str(line[0])) , (str(imm) if(n== 10) else hex(imm))  + "("+("$" + str(line[2]))+")" )
            mem = imm + rs
            memo= mem
            mem = mem - int('0x2000', 16)
            rt= format(rt,'064b')
            first= rt[32:40]
            sec= rt[40:48]
            third= rt[48:56]
            rt= rt[56:64]
            word=  first +sec+ third+ rt
            first= int(first,2)
            sec= int(sec,2)
            third= int(third,2)
            rt= int(rt,2)
            word= int(word,2)
            memory[mem] = rt
            mem+=1
            memory[mem] = third
            mem+=1
            memory[mem] = sec
            mem+=1
            memory[mem] = first
            print ("result memory: ", hex(memo) ,"=", hex(word))
            pc+= 4# increments pc by 4 
             
           # pcprint=  hex(pc)
            #print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint)  
           
        elif(line[0:2] == "sb"): # sb
            line = line.replace("sb","")
            line = line.replace(")","")
            line = line.replace("(",",")
            line = line.split(",")
            if(line[1][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[1],n) if (int(line[1],n) >= 0) else (65536 + int(line[1],n))
            rs = int(registers[("$" + str(line[2]))])
            rt = registers[("$" + str(line[0]))]
            instruction = "sb"
            print (instruction , ("$" + str(line[0])) , (str(imm) if(n== 10) else hex(imm)) + "("+("$" + str(line[2]))+")" )
            mem = imm + rs
            memo= mem
            mem = mem - int('0x2000', 16)
            rt= format(rt,'08b')
            rt= int(rt,2)
            memory[mem] = rt
            print ("result memory:", hex(memo) ,"=", hex(rt))
            pc+= 4# increments pc by 4 
           # pcprint=  hex(pc)
            #print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint)  
       
        elif(line[0:2] == "lb"): # lbu
            line = line.replace("lb","")
            line = line.replace(")","")
            line = line.replace("(",",")
            if(line[0:1] == "u"):
               line = line.replace("u","")
               op = '100100'
            else:
                op = '100000'
            line = line.split(",")
            if(line[1][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[1],n) if (int(line[1],n) >= 0) else (65536 + int(line[1],n))
            rs = int(registers[("$" + str(line[2]))])
            rt = "$" + str(line[0])
            instruction = "lb" if(op == '100000') else "lbu"
            print (instruction , rt , hex(imm)+ "("+("$" + str(line[2]))+")" )
            mem = imm + rs
            mem = mem - int('0x2000', 16)
            temp3 = int(memory[mem]) if (int(memory[mem]) > 0 or op == '100000') else (65536 + int(memory[mem]))
            temp3 = format(temp3, '08b')
            temp3 = int(temp3[:8],2)
            registers[rt] = temp3
            print ("result:",rt ,"=", hex(temp3))
            pc += 4# increments pc by 4 
             
           # pcprint = hex(pc)
            #print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint)

        elif(line[0:3] == "bne"): # bne
            line = line.replace("bne","")
            line = line.split(",")
            for i in range(len(labelName)):
                    if(labelName[i] == line[2]):
                       lpos = int(labelIndex[i]-1)
                       label= labelName[i] 
            temp2= (pcAssign[lpos])+4
            rs = registers[("$" + str(line[1]))]
            rt = registers[("$" + str(line[0]))]
            instruction = "bne" 
            print (instruction , ("$" + str(line[0])) ,("$" + str(line[1])), str(line[2]))
            if(rs != rt):
                temp2= temp2-pc
                pc+=temp2
                print ("branch to" ,label)
            else:
                pc+= 4
                print ("does not branch, go to next instructions" )
           # pcprint=  hex(pc)
            #print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint)
        elif(line[0:3] == "beq"): # bne
            line = line.replace("beq","")
            line = line.split(",")
            for i in range(len(labelName)):
                    if(labelName[i] == line[2]):
                       lpos = int(labelIndex[i]-1)
                       label= labelName[i] 
            temp2= (pcAssign[lpos])+4
            rs = registers[("$" + str(line[1]))]
            rt = registers[("$" + str(line[0]))]
            instruction = "bne" 
            print (instruction , ("$" + str(line[0])) ,("$" + str(line[1])), str(line[2]))
            if(rs == rt):
                temp2= temp2-pc
                pc+=temp2
                print ("branch to" ,label)
            else:
                pc+= 4
                print ("does not branch, go to next instructions" )
           # pcprint=  hex(pc)
            #print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint)

        elif(line[0:3] == "srl"): # SRL
            line = line.replace("srl","")
            line = line.split(",")
            rd = "$" + str(line[0])
            rt = registers[("$" + str(line[1]))]
            shamt = int(line[2])
            instruction = "srl"
            print (instruction , rd ,("$" + str(line[1])), shamt)
            result = rt >> shamt 
            registers[rd]= result
            print ("result:" , rd ,"=", hex(result))
            pc+= 4# increments pc by 4 
             
            #pcprint=  hex(pc)
            #print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint)
        
        elif(line[0:3] == "sll"): # SLL
            line = line.replace("sll","")
            line = line.split(",")
            rd = "$" + str(line[0])
            rt = registers[("$" + str(line[1]))]
            shamt = int(line[2])
            instruction = "sll" 
            print (instruction , rd ,("$" + str(line[1])), shamt)
            result = rt << shamt # does the addition operation
            result = format(result,'064b')
            result = int(result[32:],2)
            registers[rd]= result
            print ("result:" ,rd ,"=", hex(result))
            pc += 4 # increments pc by 4 
           # pcprint =  hex(pc)
           # print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint)     
            
        elif(line[0:5] == "cfold"): # CFOLD
            line = line.replace("cfold","")
            line = line.split(",")
            rs = registers[("$" + str(line[1]))]	#First register
            rt = registers[("$" + str(line[2]))]	#Second register
            instruction = "cfold" 
            print (instruction , ("$" + str(line[0])) ,("$" + str(line[1])), ("$" + str(line[2])))
            HashAndMatch(rt, rs)
            
            pc += 4# increments pc by 4 
           # pcprint =  hex(pc)
           # print(registers)# print all the registers and their values (testing purposes to see what is happening)
           # print(pc)
            #print(pcprint)

        elif(line[0:4] == "mult"): # MULT/U
            line = line.replace("mult","")
            if(line[0:1] == "u"):
               line = line.replace("u","")
               op= '011001'
            else:
                op= '011000'
            line = line.split(",")
            rs = registers[("$" + str(line[0]))]	#First register
            rt = registers[("$" + str(line[1]))]	#Second register
            rs= int(rs) if (int(rs) > 0 or op == '011000') else (65536 + int(rs))
            rt= int(rt) if (int(rt) > 0 or op == '011000') else (65536 + int(rt))
            instruction = "mult" if(op == '011000') else "multu"
            print (instruction , ("$" + str(line[0])) ,("$" + str(line[1])))
            temp = rs * rt	#Multiply
            temp= format(temp,'064b')
            hi=  int(temp[:32],2)
            lo=  int(temp[32:],2)
            registers["$hi"] = hi		#Shift high right 32
            registers["$lo"] = lo	#Shift low left 32
            print ("result:" ,"$hi" ,"=", hex(hi))
            print ("result:" ,"$lo" ,"=", hex(lo))
            pc += 4# increments pc by 4 
             
            #pcprint =  hex(pc)
            #print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint) 

        elif(line[0:4] == "mflo"): #MFLO
            line = line.replace("mflo","")
            op = '001010'
            line = line.split(",")
            rs = "$" + str(line[0])		#Register to write to
            result = registers["$lo"]
            instruction = "mflo" 
            print (instruction , rs )
            registers[rs] = registers["$lo"]	#Write value to register
            print ("result:" ,rs ,"=", hex(result))
            pc += 4# increments pc by 4 
             
           # pcprint =  hex(pc)
            #print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint)

        elif(line[0:4] == "mfhi"): #MFHI
            line = line.replace("mfhi","")
            op = '001000'
            line = line.split(",")
            rd = "$" + str(line[0])		#Register to write to
            result = registers["$hi"]
            instruction = "mfhi" 
            print (instruction ,rd )
            registers[rd] = registers["$hi"]	#Write value to register

            print ("result:" ,rd ,"=", hex(result))
            pc += 4# increments pc by 4 
             
           # print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint)

        elif(line[0:4] == "slti"): # SLTI/U
            line = line.replace("slti","")
            if(line[0:1] == "u"):
               line = line.replace("u","")
               op = '001011'
            else:
                op= '001010'
            line = line.split(",")
            if(line[2][0:2]== "0x"):
                n=16
            else:
                n=10
            
            imm = int(line[2],n) if (int(line[2],n) > 0 or op == '001010') else (65536 + int(line[2],n)) # will get the negative or positive inter value. if unsigned and negative will get the unsigned value of th negative integer.
            rs = registers[("$" + str(line[1]))] # reads the value from specified register
            rt = "$" + str(line[0]) # locate the register in which to write to
            instruction = "slti" if(op == '001010') else "sltiu"
            print (instruction , rt ,("$" + str(line[1])), imm if(n== 10) else hex(imm))
            if(rs < imm):
                result = 1
            else:
                result = 0
            registers[rt]= result # writes the value to the register specified
            print ("result:" ,rt ,"=", hex(result))
            pc += 4 # increments pc by 4 
             
            #pcprint = hex(pc)
            #print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint)
           
        elif(line[0:3] == "xor"): # XOR
            line = line.replace("xor","")
            line = line.split(",")
            rd = "$" + str(line[0])
            rs = registers[("$" + str(line[1]))]
            rt = registers[("$" + str(line[2]))]
            instruction = "xor"
            print (instruction , rd ,("$" + str(line[1])), ("$" + str(line[2])))
            result = rs ^ rt # does the addition operation
            registers[rd]= result
            print ("result:" ,rd ,"=", hex(result))
            
            pc+= 4 # increments pc by 4 
             
           # pcprint =  hex(pc)
           # print(registers)# print all the registers and their values (testing purposes to see what is happening)
           # print(pc)
           # print(pcprint)
       
        elif(line[0:3] == "add"): # ADD
            line = line.replace("add","")
            line = line.split(",")
            rd = "$" + str(line[0])
            rs = registers[("$" + str(line[1]))]
            rt = registers[("$" + str(line[2]))]
            instruction = "add"
            print (instruction , rd ,("$" + str(line[1])), ("$" + str(line[2])))
            result = rs + rt # does the addition operation
            registers[rd]= result
            print ("result:" ,rd ,"=", hex(result))
            pc+= 4 # increments pc by 4 
             
           # pcprint =  hex(pc)
           # print(registers)# print all the registers and their values (testing purposes to see what is happening)
           # print(pc)
           # print(pcprint)
        
        elif(line[0:3] == "ori"): # ori
            line = line.replace("ori","")
            line = line.split(",")
            if(line[2][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[2],n) if (int(line[2],n) > 0) else (65536 + int(line[2],n)) # will get the negative or positive inter value. if unsigned and negative will get the unsigned value of th negative integer.
            rs = registers[("$" + str(line[1]))] # reads the value from specified register
            rt = "$" + str(line[0]) # locate the register in which to write to
            instruction = "ori"
            print (instruction , rt ,("$" + str(line[1])), imm if(n== 10) else hex(imm))
            result = rs | imm # does the addition operation
            registers[rt]= result # writes the value to the register specified
            print ("result:" ,rt ,"=", hex(result))
            pc+= 4 # increments pc by 4 
             
            #pcprint =  hex(pc)
            #print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint)
            
        elif(line[0:4] == "andi"): # andi
            line = line.replace("andi","")
            line = line.split(",")
            if(line[2][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[2],n) if (int(line[2],n) >= 0) else (65536 + int(line[2],n)) # will get the negative or positive inter value. if unsigned and negative will get the unsigned value of th negative integer.
            rs = registers[("$" + str(line[1]))] # reads the value from specified register
            rt = "$" + str(line[0]) # locate the register in which to write to
            instruction = "andi" 
            print (instruction , rt ,("$" + str(line[1])), imm if(n== 10) else hex(imm))
            result = rs & imm # does the addition operation
            registers[rt]= result # writes the value to the register specified
            print ("result:" ,rt ,"=", hex(result))
            pc+= 4 # increments pc by 4 
             
           # pcprint =  hex(pc)
            #print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint)

        elif(line[0:1] == "j"): # JUMP
            line = line.replace("j","")
            line = line.split(",")
            instruction = "j" 
            print (instruction , ("$" + str(line[0])))
           
            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location

            if(line[0].isdigit()): # First,test to see if it's a label or a integer
                pc= int(line[0])
               # hexstr= hex(int(hexstr[0], 2))
               # f.write(hexstr + '\n')#str('000010') + str(format(int(line[0]),'026b')) + '\n'+ hexstr+ '\n')

            else: # Jumping to label
                for i in range(len(labelName)):
                    if(labelName[i] == line[0]):
                        lpos = int(labelIndex[i]-1)
                        
                pc= (pcAssign[lpos])+4
                print ("branch to" ,label)
        print("Next instruction PC =",pc)
        return pc;
                        #pc= format(int(labelIndex[i]),'026b')
                        #pc = int(pc,2)
                        #hexstr= hex(int(hexstr[0], 2))
                       # f.write(hexstr+ '\n')#str('000010') + str(format(int(labelIndex[i]),'026b')) + '\n'+ hexstr+ '\n')
  

def saveJumpLabel(asm,labelIndex, labelName):
    lineCount = 0
    ppc= 0
    for line in asm:
        line = line.replace(" ","")
        if":" in line:
            pcAssign.append(0)
        else:
            pcAssign.append(ppc)
            ppc+=4
        if(line.count(":")):
            labelName.append(line[0:line.index(":")]) # append the label name
            labelIndex.append(lineCount) # append the label's index
            asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

def main():
   # f = open("mc.txt","w+")
    h = open("ProgramA_Testcase1.txt","r")
    asm = h.readlines()
    instrs = []
    FinalDIC= 0
    FinalPC= 0
    TotalCycles= 0
    
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')
       
    saveJumpLabel(asm,labelIndex,labelName) # Save all jump's destinations
    for line in asm:
        #line = line.replace("\t","")
        #line = line.replace('"','')
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0
        instrs.append(line)
       
    print(pcAssign)
    FinalDIC, FinalPC, TotalCycles = multiCycle(instrs, FinalDIC, FinalPC, TotalCycles)
    print("All memory contents:")
    for k in range(0,1024):
        mem= 8192+ (k*4)
        memlo= mem- 8192
        first = format(memory[memlo],"08b")
        memlo+=1
        second = format(memory[memlo],"08b")
        memlo+=1
        third = format(memory[memlo],"08b")
        memlo+=1
        fourth = format(memory[memlo],"08b")
        memlo+=1
        word =  fourth+ third + second+first
        word= int(word,2)
        word = format(word,"08x")
        print("memory", hex(mem)+": 0x"+ word )
    
    print("all register values:")
    proregister= str(registers)
    proregister= proregister.replace("'","")
    proregister= proregister.replace("{","")
    proregister= proregister.replace("}","")
    proregister= proregister.replace(",",";")
    #print(registers)
    print(proregister)
    print("Final PC =",FinalPC)
    print("memory contents from 0x2000 - 0x2050:")
    for l in range(0,21):
        mem= 8192+ (l*4)
        memlo= mem- 8192
        first = format(memory[memlo],"08b")
        memlo+=1
        second = format(memory[memlo],"08b")
        memlo+=1
        third = format(memory[memlo],"08b")
        memlo+=1
        fourth = format(memory[memlo],"08b")
        memlo+=1
        word =  fourth+ third + second+first
        word= int(word,2)
        word = format(word,"08x")
        print("memory", hex(mem)+": 0x"+ word )
    print("Dynamic Instruction Count: ",FinalDIC)

   # print(memory)

    #f.close()

if __name__ == "__main__":
    main()
