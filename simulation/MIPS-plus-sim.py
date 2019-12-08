import math
import re
import ctypes
memory = [0] *4096 #Remember when ever you get an address in hex subtract 8192 from it then write to it
				#Dynamic Instruction Count
defaultregisters = {"$0": 0, "$8":0,"$9": 0, "$10":0,"$11": 0, 
                  "$12":0,"$13": 0, "$14":0,"$15": 0, "$16":0,"$17": 0, 
                  "$18":0,"$19": 0, "$20":0,"$21": 0, "$22":0,"$23": 0, "$lo":0,"$hi":0}

global registers 
#registers = dict.fromkeys(defaultregisters,0)


defaultpipe = {"instr": " ", "type": " ", "stall": 0, "name": " ", "nop": 2, "branch": 0,
           "reghold": {"rs": " ", "rd": " ", "rt": " "},


            }
global ft
global de
global ex
global m
global wb
#ft = defaultpipe.copy()
##ft = defaultpipe.copy()
#de = defaultpipe.copy()
#ex = defaultpipe.copy()
#m = defaultpipe.copy()
#wb = defaultpipe.copy()


#ft = {"instr": " ", "type": " ", "stall": 0, "name": " ", "nop": 2, "branch": 0,
#            "reghold": {"rs": " ", "rd": " ", "rt": " "},


#            }

#de = {"instr": " ", "type": " ", "stall": 0, "name": " ", "nop": 2, "branch": 0,
#            "reghold": {"rs": " ", "rd": " ", "rt": " "},


#            }

#ex = {"instr": " ", "type": " ", "stall": 0, "name": " ", "nop": 2, "branch": 0,
#            "reghold": {"rs": " ", "rd": " ", "rt": " "},


#            }

#m = {"instr": " ", "type": " ", "stall": 0, "name": " ", "nop": 2, "branch": 0,
#            "reghold": {"rs": " ", "rd": " ", "rt": " "},


#            }

#wb = {"instr": " ", "type": " ", "stall": 0, "name": " ", "nop": 2, "branch": 0,
#            "reghold": {"rs": " ", "rd": " ", "rt": " "},

#            }

stats = {"delay" : 0,
        "flush" : 0,
        "ALUOutM -> srcAE" : 0,
        "ALUOutM ‐> srcBE" : 0,
        "ALUOutM ‐> WriteDataE" : 0,
        "ALUOutM ‐> EqualD" : 0,
        "ResultW ‐> SrcAE" : 0,
        "ResultW ‐> SrcBE" : 0,
        "ResultW ‐> WriteDataE" : 0,
        "ResultW ‐> EqualD" : 0}

global controlSignals
global controlSignals2
controls= {"AluScrA":0,"AluScrB":'01',"MemWrite":0,"RegDst":0,"MemtoReg":0,"RegWrite":0,"Branch":0, "c3":0, "c4":0, "c5":0}
controls2= {"AluScrA":0,"AluScrB":'01',"MemWrite":0,"RegDst":0,"MemtoReg":0,"RegWrite":0,"Branch":0, "PC": 0}
#controlSignals = controls.copy()
#controlSignals2 = ccontrols2.copy()
global cache_type
global blk_size   #Block size in Bytes
global num_ways   #Number of ways
global total_s 
global total_blk
global Misses 
global Hits
global diagnosis
cache_type = 0
blk_size = 0    #Block size in Bytes
num_ways = 0    #Number of ways
total_s = 0   #Number of blocks/sets
total_blk = 0
diagnosis = 0
Misses = 0
Hits = 0

labelIndex = []
labelName = []
pcAssign= []

def int32_to_uint32(i):
    print(i)
    return ctypes.c_uint32(i).value

def multiCycle(instrs, DIC, pc, cycles, set_offset, word_offset):
    cycle1=0
    cycle2=0
    cycle3=0
    cycle4=0
    cycle5=0
    
    global cache_type
    global blk_size   #Block size in Bytes
    global num_ways   #Number of ways
    global total_s 
    global total_blk
    global Misses 
    global Hits
    global diagnosis
    global controlSignals
    global controlSignals2
        
    LRU = [['' for j in range(num_ways)] for i in range(total_s)]
    Valid = [[0 for j in range(num_ways)] for i in range(total_s)]
    Tag = [["0" for j in range(num_ways)] for i in range(total_s)]
    Cache = [[[0 for j in range(num_ways)] for i in range(blk_size)] for i in range(total_s)] #Cache data    
    
    while True:
        cycles= cycle1+ cycle2+ cycle3+ cycle4+ cycle5
        if (int(pc/4) >= len(instrs)):
            print("Dynamic Instruction Count: ",DIC)
            return DIC, pc, cycles;
        DIC+=1
  #      if DIC == 173:
   #         print("pause")
        #cycle1
        l = instrs[int(pc/4)]
        cycle1+=1
        controlSignals["AluScrA"]+=0
        controlSignals["AluScrB"]='01'
        
        controlSignals2["AluScrA"]=0
        controlSignals2["AluScrB"]='01'
        controlSignals2["RegDst"]= 3
        controlSignals2["MemtoReg"]=3
        controlSignals2["RegWrite"]=3
        controlSignals2["Branch"]=3
        controlSignals2["MemWrite"]=0
        if(diagnosis== "1"):
            print("instruction {} at cycle 1\n Current PC content = {}".format(l,controlSignals2["PC"]))
            printSignals2= str(controlSignals2)
            printSignals2= printSignals2.replace("'","")
            printSignals2= printSignals2.replace("{","")
            printSignals2= printSignals2.replace("}","")
            printSignals2= printSignals2.replace(",","\n")
            printSignals2= printSignals2.replace("3","X")
            printSignals2= printSignals2.replace(":","=")
            print(" "+ printSignals2)
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
        
        controlSignals2["PC"]+=4
        controlSignals2["AluScrA"]=0
        controlSignals2["AluScrB"]='11'
        controlSignals2["RegDst"]= 3
        controlSignals2["MemtoReg"]=3
        controlSignals2["RegWrite"]=3
        controlSignals2["Branch"]=3
        controlSignals2["MemWrite"]=3
        if(diagnosis== "1"):
            print("instruction {} at cycle 2\n Current PC content = {}".format(l,controlSignals2["PC"]))
            printSignals2= str(controlSignals2)
            printSignals2= printSignals2.replace("'","")
            printSignals2= printSignals2.replace("{","")
            printSignals2= printSignals2.replace("}","")
            printSignals2= printSignals2.replace(",","\n")
            printSignals2= printSignals2.replace("3","X")
            printSignals2= printSignals2.replace(":","=")
            print(" "+ printSignals2)
       # controlSignals["AluOp"]='00'
        if "w" in l[0:2]:
       #cycle3 
            cycle3+=1
            controlSignals["AluScrA"]+=1
            controlSignals["AluScrB"]='10'
           
            controlSignals2["AluScrA"]=0
            controlSignals2["AluScrB"]='10'
            controlSignals2["RegDst"]= 3
            controlSignals2["MemtoReg"]=3
            controlSignals2["RegWrite"]=3
            controlSignals2["Branch"]=0
            controlSignals2["MemWrite"]=3
            if(diagnosis== "1"):
                print("instruction {} at cycle 3\n Current PC content = {}".format(l,controlSignals2["PC"]))
                printSignals2= str(controlSignals2)
                printSignals2= printSignals2.replace("'","")
                printSignals2= printSignals2.replace("{","")
                printSignals2= printSignals2.replace("}","")
                printSignals2= printSignals2.replace(",","\n")
                printSignals2= printSignals2.replace("3","X")
                printSignals2= printSignals2.replace(":","=")
                print(" "+ printSignals2)
           # controlSignals["AluOp"]='00'
       #cycle4
            print("word_offset", word_offset)
            pc, Cache, LRU, Tag, Valid = instrExecution(l, pc, set_offset, word_offset, Cache, LRU, Tag, Valid)
            #controlSignals["IorD"]=0
            cycle4+=1
            controlSignals2["AluScrA"]=3
            controlSignals2["AluScrB"]='3'
            controlSignals2["RegDst"]= 3
            controlSignals2["MemtoReg"]=3
            controlSignals2["RegWrite"]=3
            controlSignals2["Branch"]=3
            if "sw" in l:
                controlSignals["c4"]+=1
                controlSignals["MemWrite"]+=1
                controlSignals2["MemWrite"]=1
                if(diagnosis== "1"):
                    print("instruction {} at cycle 4\n Current PC content = {}".format(l,controlSignals2["PC"]))
                    printSignals2= str(controlSignals2)
                    printSignals2= printSignals2.replace("'","")
                    printSignals2= printSignals2.replace("{","")
                    printSignals2= printSignals2.replace("}","")
                    printSignals2= printSignals2.replace(",","\n")
                    printSignals2= printSignals2.replace("3","X")
                    printSignals2= printSignals2.replace(":","=")
                    print(" "+ printSignals2)
            else:
                controlSignals["RegDst"]+= 0
                controlSignals["MemtoReg"]+=0
                controlSignals["RegWrite"]+=0
                 
                controlSignals2["AluScrA"]=3
                controlSignals2["AluScrB"]='3'
                controlSignals2["RegDst"]= 3
                controlSignals2["MemtoReg"]=3
                controlSignals2["RegWrite"]=3
                controlSignals2["Branch"]=3
                controlSignals2["MemWrite"]=0
                if(diagnosis== "1"):
                    print("instruction {} at cycle 4\n Current PC content = {}".format(l,controlSignals2["PC"]))
                    printSignals2= str(controlSignals2)
                    printSignals2= printSignals2.replace("'","")
                    printSignals2= printSignals2.replace("{","")
                    printSignals2= printSignals2.replace("}","")
                    printSignals2= printSignals2.replace(",","\n")
                    printSignals2= printSignals2.replace("3","X")
                    printSignals2= printSignals2.replace(":","=")
                    print(" "+ printSignals2)

                cycle5+=1
                controlSignals["c5"]+=1
                controlSignals["RegDst"]+= 0
                controlSignals["MemtoReg"]+=1
                controlSignals["RegWrite"]+=1
                 
                controlSignals2["AluScrA"]=3
                controlSignals2["AluScrB"]='3'
                controlSignals2["RegDst"]= 0
                controlSignals2["MemtoReg"]=1
                controlSignals2["RegWrite"]=1
                controlSignals2["Branch"]=3
                controlSignals2["MemWrite"]=0
                if(diagnosis== "1"):
                    print("instruction {} at cycle 5\n Current PC content = {}".format(l,controlSignals2["PC"]))
                    printSignals2= str(controlSignals2)
                    printSignals2= printSignals2.replace("'","")
                    printSignals2= printSignals2.replace("{","")
                    printSignals2= printSignals2.replace("}","")
                    printSignals2= printSignals2.replace(",","\n")
                    printSignals2= printSignals2.replace("3","X")
                    printSignals2= printSignals2.replace(":","=")
                    print(" "+ printSignals2)
        elif "bne" in l:
      #cycle3 
            cycle3+=1
            controlSignals["c3"]+=1
            controlSignals["AluScrA"]+= 1
            controlSignals["AluScrB"]='10'
            controlSignals["Branch"]+=1
            
            controlSignals2["AluScrA"]=1
            controlSignals2["AluScrB"]='00'
            controlSignals2["RegDst"]= 3
            controlSignals2["MemtoReg"]=3
            controlSignals2["RegWrite"]=3
            controlSignals2["Branch"]=1
            controlSignals2["MemWrite"]=3
            if(diagnosis== "1"):
                print("instruction {} at cycle 3\n Current PC content = {}".format(l,controlSignals2["PC"]))
                printSignals2= str(controlSignals2)
                printSignals2= printSignals2.replace("'","")
                printSignals2= printSignals2.replace("{","")
                printSignals2= printSignals2.replace("}","")
                printSignals2= printSignals2.replace(",","\n")
                printSignals2= printSignals2.replace("3","X")
                printSignals2= printSignals2.replace(":","=")
                print(" "+ printSignals2)
            pc, Cache, LRU, Tag, Valid = instrExecution(l, pc, set_offset, word_offset, Cache, LRU, Tag, Valid)
        elif "beq" in l:
      #cycle3 
            cycle3+=1
            controlSignals["c3"]+=1
            controlSignals["AluScrA"]+= 1
            controlSignals["AluScrB"]='10'
            controlSignals["Branch"]+=1
            
            controlSignals2["AluScrA"]=1
            controlSignals2["AluScrB"]='00'
            controlSignals2["RegDst"]= 3
            controlSignals2["MemtoReg"]=3
            controlSignals2["RegWrite"]=3
            controlSignals2["Branch"]=1
            controlSignals2["MemWrite"]=3
            if(diagnosis== "1"):
                print("instruction {} at cycle 3\n Current PC content = {}".format(l,controlSignals2["PC"]))
                printSignals2= str(controlSignals2)
                printSignals2= printSignals2.replace("'","")
                printSignals2= printSignals2.replace("{","")
                printSignals2= printSignals2.replace("}","")
                printSignals2= printSignals2.replace(",","\n")
                printSignals2= printSignals2.replace("3","X")
                printSignals2= printSignals2.replace(":","=")
                print(" "+ printSignals2)
            pc, Cache, LRU, Tag, Valid = instrExecution(l, pc, set_offset, word_offset, Cache, LRU, Tag, Valid)
        else:
            controlSignals["c4"]+=1
            if "i" in l:    
           #cycle3
                cycle3+=1
                controlSignals["AluScrA"]+= 1
                controlSignals["AluScrB"]='10'
                
                controlSignals2["AluScrA"]=1
                controlSignals2["AluScrB"]='10'
                controlSignals2["RegDst"]= 3
                controlSignals2["MemtoReg"]=3
                controlSignals2["RegWrite"]=3
                controlSignals2["Branch"]=0
                controlSignals2["MemWrite"]=3
                if(diagnosis== "1"):
                    print("instruction {} at cycle 3\n Current PC content = {}".format(l,controlSignals2["PC"]))
                    printSignals2= str(controlSignals2)
                    printSignals2= printSignals2.replace("'","")
                    printSignals2= printSignals2.replace("{","")
                    printSignals2= printSignals2.replace("}","")
                    printSignals2= printSignals2.replace(",","\n")
                    printSignals2= printSignals2.replace("3","X")
                    printSignals2= printSignals2.replace(":","=")
                    print(" "+ printSignals2)
              #  controlSignals["AluOp"]='10'
                #cycle4
                cycle4+=1
                pc, Cache, LRU, Tag, Valid = instrExecution(l, pc, set_offset, word_offset, Cache, LRU, Tag, Valid)
                controlSignals["RegDst"]+= 0
                controlSignals["MemtoReg"]+=0
                controlSignals["RegWrite"]+=1

                controlSignals2["AluScrA"]=3
                controlSignals2["AluScrB"]='3'
                controlSignals2["RegDst"]= 0
                controlSignals2["MemtoReg"]=0
                controlSignals2["RegWrite"]=1
                controlSignals2["Branch"]=3
                controlSignals2["MemWrite"]=3
                if(diagnosis== "1"):
                    print("instruction {} at cycle 4\n Current PC content = {}".format(l,controlSignals2["PC"]))
                    printSignals2= str(controlSignals2)
                    printSignals2= printSignals2.replace("'","")
                    printSignals2= printSignals2.replace("{","")
                    printSignals2= printSignals2.replace("}","")
                    printSignals2= printSignals2.replace(",","\n")
                    printSignals2= printSignals2.replace("3","X")
                    printSignals2= printSignals2.replace(":","=")
                    print(" "+ printSignals2)
            else:
                controlSignals["AluScrA"]+=1 
                controlSignals["AluScrB"]='00'
               
                controlSignals2["AluScrA"]=1
                controlSignals2["AluScrB"]='00'
                controlSignals2["RegDst"]= 3
                controlSignals2["MemtoReg"]=3
                controlSignals2["RegWrite"]=3
                controlSignals2["Branch"]=0
                controlSignals2["MemWrite"]=3
                if(diagnosis== "1"):
                    print("instruction {} at cycle 3\n Current PC content = {}".format(l,controlSignals2["PC"]))
                    printSignals2= str(controlSignals2)
                    printSignals2= printSignals2.replace("'","")
                    printSignals2= printSignals2.replace("{","")
                    printSignals2= printSignals2.replace("}","")
                    printSignals2= printSignals2.replace(",","\n")
                    printSignals2= printSignals2.replace("3","X")
                    printSignals2= printSignals2.replace(":","=")
                    print(" "+ printSignals2)
              #  controlSignals["AluOp"]='10'
                #cycle4
                cycle4+=1
                pc, Cache, LRU, Tag, Valid = instrExecution(l, pc, set_offset, word_offset, Cache, LRU, Tag, Valid)
                controlSignals["RegDst"]+= 1
                controlSignals["MemtoReg"]+=0
                controlSignals["RegWrite"]+=1
                
                controlSignals2["AluScrA"]=3
                controlSignals2["AluScrB"]='3'
                controlSignals2["RegDst"]= 1
                controlSignals2["MemtoReg"]=0
                controlSignals2["RegWrite"]=1
                controlSignals2["Branch"]=3
                controlSignals2["MemWrite"]=3
                if(diagnosis== "1"):
                    print("instruction {} at cycle 4\n Current PC content = {}".format(l,controlSignals2["PC"]))
                    printSignals2= str(controlSignals2)
                    printSignals2= printSignals2.replace("'","")
                    printSignals2= printSignals2.replace("{","")
                    printSignals2= printSignals2.replace("}","")
                    printSignals2= printSignals2.replace(",","\n")
                    printSignals2= printSignals2.replace("3","X")
                    printSignals2= printSignals2.replace(":","=")
                    print(" "+ printSignals2)

def pathsandprint(aluoutm1,aluoutm2):
    global diagnosis
    diagnostic = diagnosis

def pathsandprint(aluoutm1,aluoutm2, diagnostic):
    global ft
    global de
    global ex
    global m
    global wb
    print("\n")
    print("the following are any fowarding paths taken")

    if ft["nop"] == 1:
        fetch = "bubble stall"
    elif ft["nop"] == 2:
        fetch = "empty"
    elif ft["nop"] == 3:
        fetch = "bubble flush"
    else:
        fetch = ft["instr"]

    if de["nop"] == 1:
        decode = "bubble stall"
    elif de["nop"] == 2:
        decode = "empty"
    elif de["nop"] == 3:
        decode = "bubble flush"
    else:
        decode = de["instr"]

    if ex["nop"] == 1:
        execution = "bubble stall"
    elif ex["nop"] == 2:
        execution = "empty"
    elif ex["nop"] == 3:
        execution = "bubble flush"
    else:
        execution = ex["instr"]

    if m["nop"] == 1:
        mem = "bubble stall"
    elif m["nop"] == 2:
        mem = "empty"
    elif m["nop"] == 3:
        mem = "bubble flush"
    else:
        mem = m["instr"]

        if (m["type"] == "i") and ((m["name"] != "sw") or (m["name"] != "lw")):

            if ex["reghold"]["rs"] == m["reghold"]["rt"]:
                aluoutm1 = 1
                if diagnostic == 1:
                    print("ALUOutM -> srcAE")
                stats["ALUOutM -> srcAE"] += 1
            if ft["reghold"]["rt"] == de["reghold"]["rt"]:
                if ex["name"] == "sw":
                    aluoutm2 = 1
                    if diagnostic == 1:
                        print("ALUOutM ‐> WriteDataE")
                    stats["ALUOutM ‐> WriteDataE"] += 1
                else:
                    aluoutm2 = 1
                    if diagnostic == 1:
                        print("ALUOutM ‐> srcBE")
                    stats["ALUOutM ‐> srcBE"] += 1
        if m["type"] == "r":
            if ex["reghold"]["rs"] == m["reghold"]["rd"]:
                aluoutm1 = 1
                if diagnostic == 1:
                    print("ALUOutM -> srcAE")
                stats["ALUOutM -> srcAE"] += 1
            if ex["reghold"]["rt"] == m["reghold"]["rd"]:
                if ex["name"] == "sw":
                    aluoutm2 = 1
                    if diagnostic == 1:
                        print("ALUOutM ‐> WriteDataE")
                    stats["ALUOutM ‐> WriteDataE"] += 1
                else:
                    aluoutm2 = 1
                    if diagnostic == 1:
                        print("ALUOutM ‐> srcBE")
                    stats["ALUOutM ‐> srcBE"] += 1

        if (de["name"] == "beq") or (de["name"] == "bne"):
            if (m["type"] == "r") and ((m["reghold"]["rd"] == de["reghold"]["rs"]) or (m["reghold"]["rd"] ==  de["reghold"]["rt"])):
                if diagnostic == 1:
                    print("ALUOutM ‐> EqualD")
                stats["ALUOutM ‐> EqualD"] += 1
            if (m["type"] == "i") and ((m["name"] != "sw") or (m["name"] !="lw")) and ((m["reghold"]["rd"] == de["reghold"]["rs"]) or (m["reghold"]["rd"] ==  de["reghold"]["rt"])):
                if diagnostic == 1:
                    print("ALUOutM ‐> EqualD")
                stats["ALUOutM ‐> EqualD"] += 1

    if wb["nop"] == 1:
        writeBack = "bubble stall"
    elif wb["nop"] == 2:
        writeBack = "empty"
    elif wb["nop"] == 3:
        writeBack = "bubble flush"
    else:
        writeBack = wb["instr"]

        if wb["type"] == "i" and wb["name"] != "sw":
            if ex["reghold"]["rs"] == wb["reghold"]["rt"] and aluoutm1 != 1:
                if diagnostic == 1:
                    print("ResultW ‐> SrcAE")
                stats["ResultW ‐> SrcAE"] += 1
            if ex["reghold"]["rt"] == wb["reghold"]["rt"] and aluoutm2 != 1:
                if ex["name"] == "sw":
                    if diagnostic == 1:
                        print("ResultW ‐> WriteDataE")
                    stats["ResultW ‐> WriteDataE"] += 1
                else:
                    if diagnostic == 1:
                        print("ResultW ‐> SrcBE")
                    stats["ResultW ‐> SrcBE"] += 1

        if m["type"] == "r":
            if ex["reghold"]["rs"] == wb["reghold"]["rd"] and aluoutm1 != 1:
                if diagnostic == 1:
                    print("ResultW ‐> SrcAE")
                stats["ResultW ‐> SrcAE"] += 1
            if ex["reghold"]["rt"] == wb["reghold"]["rd"] and aluoutm2 != 1:
                if ex["name"] == "sw":
                    if diagnostic == 1:
                        print("ResultW ‐> WriteDataE")
                    stats["ResultW ‐> WriteDataE"] += 1
                else:
                    if diagnostic == 1:
                        print("ResultW ‐> SrcBE")
                    stats["ResultW ‐> SrcBE"] += 1

        if (de["name"] == "beq") or (de["name"] == "bne"):
            if wb["type"] == "r" and ((wb["reghold"]["rd"] == de["reghold"]["rs"]) or (wb["reghold"]["rd"] == de["reghold"]["rt"])):
                if diagnostic == 1:
                    print("ResultW ‐> EqualD")
                stats["ResultW ‐> EqualD"] += 1
            if wb["type"] == "i" and wb["name"] != "sw" and ((wb["reghold"]["rt"] == de["reghold"]["rs"]) or (wb["reghold"]["rt"] ==de["reghold"]["rt"])):
                if diagnostic == 1:
                    print("ResultW ‐> EqualD")
                stats["ResultW ‐> EqualD"] += 1
    if diagnostic == 1:
        print("end of fowarding paths taken\n")

        print("current instruction's in each cycle")
        print("fetch: {} , decode: {}, execution: {} , memory: {} , write back: {}\n".format(fetch, decode,execution,mem,writeBack), sep='|')
      #  input("press enter to continue")


    
def pipeline(instrs, DIC, pc, cycles,set_offset, word_offset):
    global cache_type
    global blk_size   #Block size in Bytes
    global num_ways   #Number of ways
    global total_s 
    global total_blk
    global Misses 
    global Hits
    global diagnosis
    global m
    global ex   #Block size in Bytes
    global ft   #Number of ways
    global de 
    global wb  
        
    LRU = [['' for j in range(num_ways)] for i in range(total_s)]
    Valid = [[0 for j in range(num_ways)] for i in range(total_s)]
    Tag = [["0" for j in range(num_ways)] for i in range(total_s)]
    Cache = [[[0 for j in range(num_ways)] for i in range(blk_size)] for i in range(total_s)] #Cache data   
    
    while True:

        currentpc = pc
        if (int(pc / 4) >= len(instrs)):
            print("Dynamic Instruction Count: ", DIC)
            return DIC, pc, cycles;
        DIC += 1
        l = instrs[int(pc / 4)]
        cycles += 1

        wb = m.copy()
        wb["reghold"]= m["reghold"].copy()
        m = ex.copy()
        m["reghold"]= ex["reghold"].copy()
        ex = de.copy()
        ex["reghold"]= de["reghold"].copy()
        de = ft.copy()
        de["reghold"]= ft["reghold"].copy()
        pc, Cache, LRU, Tag, Valid = instrExecution(l, pc, set_offset, word_offset, Cache, LRU, Tag, Valid)
        ft["instr"] = l
        ft["nop"] = 0
        if "w" in l:
            ft["type"] = "i"
        elif "i" in l:
            ft["type"] = "i"
        elif "bne" in l:
            ft["type"] = "b"
        elif "beq" in l:
            ft["type"] = "b"
        else:
            ft["type"] = "r"


        tmp = l
        tmp = re.split('(\d+)',tmp)
        tmp.pop(2)
        tmp.pop(3)
        ft["name"] = tmp[0]
        tmp.pop(0)
        regs = tmp
        if (ft["name"] == "lw") or (ft["name"] == "sw"):
            ft["reghold"]["rt"] = regs[0]
            if(len(tmp)== 4):
                ft["reghold"]["rs"] = regs[2]
            else:
                ft["reghold"]["rs"] = regs[4]
        elif (ft["type"] == "i") and ((ft["name"] != "bne") or (ft["name"] !="beq")):
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
        if de["name"] == "lw" and (de["reghold"]["rt"] == ft["reghold"]["rs"] or de["reghold"]["rt"] == ft["reghold"]["rt"]):
            ft["stall"] = 1
        if "beq" in l:
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

        aluoutm1 = 0
        aluoutm2 = 0
        pathsandprint(aluoutm1, aluoutm2)

        if ex["stall"] == 2:
            cycles += 1
            wb = m.copy()
            wb["reghold"]= m["reghold"].copy()
            m = ex.copy()
            m["reghold"]= ex["reghold"].copy()
            ex["nop"] = 1
            stats["delay"] += 1

            aluoutm1 = 0
            aluoutm2 = 0
            pathsandprint(aluoutm1, aluoutm2)

            cycles += 1
            wb = m.copy()
            wb["reghold"]= m["reghold"].copy()
            m["nop"] = 1
            stats["delay"] += 1

            aluoutm1 = 0
            aluoutm2 = 0
            pathsandprint(aluoutm1, aluoutm2)

        if ex["stall"] == 1:
            cycles += 1
            wb = m.copy()
            wb["reghold"]= m["reghold"].copy()
            m = ex.copy()
            m["reghold"]= ex["reghold"].copy()
            ex["nop"] = 1
            stats["delay"] += 1

            aluoutm1 = 0
            aluoutm2 = 0
            pathsandprint(aluoutm1, aluoutm2)

        if ft["branch"] == 1:
            cycles += 1
            wb = m.copy()
            wb["reghold"]= m["reghold"].copy()
            m = ex.copy()
            m["reghold"]= ex["reghold"].copy()
            ex = de.copy()
            ex["reghold"]= de["reghold"].copy()
            de = ft.copy()
            de["reghold"]= ft["reghold"].copy()
            stats["flush"] += 1

            currentpc +=4
            l = instrs[int(currentpc/ 4)]


            ft["instr"] = l


            tmp = l
            tmp = re.split('(\d+)',tmp)
            tmp.pop(2)
            tmp.pop(3)
            ft["name"] = tmp[0]
            tmp.pop(0)
            regs = tmp
            
            if (ft["name"] == "lw") or (ft["name"] == "sw"):
                ft["reghold"]["rt"] = regs[0]
                ft["reghold"]["rs"] = regs[2]
            elif (ft["type"] == "i") and ((ft["name"] != "bne") or (ft["name"] != "beq")):
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

            aluoutm1 = 0
            aluoutm2 = 0
            pathsandprint(aluoutm1, aluoutm2)
            #random
            ft["nop"] = 3
        if (int(pc / 4) >= len(instrs)):
            cycles += 1
            wb = m.copy()
            wb["reghold"]= m["reghold"].copy()
            m = ex.copy()
            m["reghold"]= ex["reghold"].copy()
            ex = de.copy()
            ex["reghold"]= de["reghold"].copy()
            de = ft.copy()
            de["reghold"]= ft["reghold"].copy()
            ft["nop"] = 2

            aluoutm1 = 0
            aluoutm2 = 0
            pathsandprint(aluoutm1, aluoutm2)

            cycles += 1
            wb = m.copy()
            wb["reghold"]= m["reghold"].copy()
            m = ex.copy()
            m["reghold"]= ex["reghold"].copy()
            ex = de.copy()
            ex["reghold"]= de["reghold"].copy()
            de["nop"] = 2

            aluoutm1 = 0
            aluoutm2 = 0
            pathsandprint(aluoutm1, aluoutm2)

            cycles += 1
            wb = m.copy()
            wb["reghold"]= m["reghold"].copy()
            m = ex.copy()
            m["reghold"]= ex["reghold"].copy()
            ex["nop"] = 2

            aluoutm1 = 0
            aluoutm2 = 0
            pathsandprint(aluoutm1, aluoutm2)

            cycles += 1
            wb = m.copy()
            wb["reghold"]= m["reghold"].copy()
            m["nop"] = 2

            aluoutm1 = 0
            aluoutm2 = 0
            pathsandprint(aluoutm1, aluoutm2)

            cycles += 1
            wb["nop"] = 2

            aluoutm1 = 0
            aluoutm2 = 0
            pathsandprint(aluoutm1, aluoutm2)

def cacheAnalysis(Valid, Cache, mem, rt, Tag, LRU, lworsw, set_offset, word_offset):
    print("you are in cache analysis")
    global cache_type
    global blk_size   #Block size in Bytes
    global num_ways   #Number of ways
    global total_s 
    global total_blk
    global Misses 
    global Hits
    global diagnosis
    print("In Progress")
    updated = 0
    mem = format(mem, '016b')
    mem = mem[:16]
    setIndex = mem[16-word_offset-set_offset:16-word_offset]
    wordIndex = mem[16-word_offset:16]
    if(setIndex == ''):
        setIndex = '0'
        
    setIndex = int(setIndex,2)
    wordIndex = int(wordIndex,2)
    
    for o in range(num_ways):
        if(Valid[setIndex][o] == 0):
            Misses += 1
            memo = mem
            me = mem[0:16-word_offset]
            
            for a in range(word_offset):
                me = me + '0'
            
            memo = int(memo, 2)
            memo = memo - int('0x2000', 16)
            me = int(me,2)
            me = me - int('0x2000', 16)
            
            for u in range(blk_size):
                #Grab byte
                byte = format(memory[me+u], '08b')
                byte = int(byte,2)
                Cache[setIndex][u][o] = byte
            
            #Load word or store word
            if(lworsw == 0):
                first = Cache[setIndex][wordIndex][o]
                second = Cache[setIndex][wordIndex+1][o]
                third = Cache[setIndex][wordIndex+2][o]
                fourth = Cache[setIndex][wordIndex+3][o]
                
                fourth = format(fourth, '08b') 
                third = format(third, '08b')
                second = format(second, '08b') 
                first = format(first, '08b')
                word = fourth + third + second + first
                
                if word[0] == '1':
                    word= int(word,2)
                    word = word - 4294967296
                else:
                    word= int(word,2)
                
                registers[rt] = word
                
            elif(lworsw == 1):
                temp = registers[rt]
                if(temp < 0):
                    temp = int32_to_uint32(temp)
                
                temp = format(temp,'064b')
                
                first= temp[32:40]
                second= temp[40:48]
                third= temp[48:56]
                fourth= temp[56:64]
                
                first= int(first,2)
                second = int(second,2)
                third = int(third,2)
                fourth= int(fourth,2)
                
                Cache[setIndex][wordIndex][o] = fourth
                Cache[setIndex][wordIndex+1][o] = third
                Cache[setIndex][wordIndex+2][o] = second
                Cache[setIndex][wordIndex+3][o] = first
                
                memo = mem
                memo = int(memo, 2)
                memo = memo - int('0x2000', 16)
                
                memory[memo] = fourth
                memory[memo+1] = third
                memory[memo+2] = second
                memory[memo+3] = first
                
            Valid[setIndex][o] = 1
            Tag[setIndex][o] = mem[0:16-set_offset-word_offset]
            updated = 1;
            LRU[setIndex].remove('')
            LRU[setIndex].append(o)
            
        if(updated == 1):
            break
        else:
            if(Tag[setIndex][o] == mem[0:16-set_offset-word_offset]):
                if(lworsw == 0):
                    first = Cache[setIndex][wordIndex][o]
                    second = Cache[setIndex][wordIndex+1][o]
                    third = Cache[setIndex][wordIndex+2][o]
                    fourth = Cache[setIndex][wordIndex+3][o]
                    
                    fourth = format(fourth, '08b') 
                    third = format(third, '08b')
                    second = format(second, '08b') 
                    first = format(first, '08b')
                    word = fourth + third + second + first
                
                    if word[0] == '1':
                        word= int(word,2)
                        word = word - 4294967296
                    else:
                        word= int(word,2)
                
                    registers[rt] = word
                elif(lworsw == 1):
                    temp = registers[rt]
                    if(temp < 0):
                        temp = int32_to_uint32(temp)
                
                    temp = format(temp,'064b')
                
                    first= temp[32:40]
                    second= temp[40:48]
                    third= temp[48:56]
                    fourth= temp[56:64]
                
                    first= int(first,2)
                    second = int(second,2)
                    third = int(third,2)
                    fourth= int(fourth,2)
                
                    Cache[setIndex][wordIndex][o] = fourth
                    Cache[setIndex][wordIndex+1][o] = third
                    Cache[setIndex][wordIndex+2][o] = second
                    Cache[setIndex][wordIndex+3][o] = first
                
                    memo = mem
                    memo = int(memo, 2)
                    memo = memo - int('0x2000', 16)
                    
                    memory[memo] = fourth
                    memory[memo+1] = third
                    memory[memo+2] = second
                    memory[memo+3] = first
                        
                Hits += 1
                updated = 1
                LRU[setIndex].remove(o)
                LRU[setIndex].append(o)
        if(updated == 1):
            break
        
    if(updated == 0):
        Misses += 1
        remove_way = LRU[setIndex][0]
        
        memo = mem
        me = mem[0:16-word_offset]
        
        for a in range(word_offset):
            me = me + '0'
            
        memo = int(memo, 2)
        memo = memo - int('0x2000', 16)
        me = int(me,2)
        me = me - int('0x2000', 16)
            
        for u in range(blk_size):
            #Grab byte
            byte = format(memory[me+u], '08b')
            byte = int(byte,2)
            Cache[setIndex][u][remove_way] = byte
        
        if(lworsw == 0):
            first = Cache[setIndex][wordIndex][remove_way]
            second = Cache[setIndex][wordIndex+1][remove_way]
            third = Cache[setIndex][wordIndex+2][remove_way]
            fourth = Cache[setIndex][wordIndex+3][remove_way]
            
            fourth = format(fourth, '08b') 
            third = format(third, '08b')
            second = format(second, '08b') 
            first = format(first, '08b')
            word = fourth + third + second + first
            
            if word[0] == '1':
                word= int(word,2)
                word = word - 4294967296
            else:
                word= int(word,2)
            
            registers[rt] = word
        elif(lworsw == 1):
            temp = registers[rt]
            
            if(temp < 0):
                temp = int32_to_uint32(temp)
                
            temp = format(temp,'064b')
                
            first= temp[32:40]
            second= temp[40:48]
            third= temp[48:56]
            fourth= temp[56:64]
            
            first= int(first,2)
            second = int(second,2)
            third = int(third,2)
            fourth= int(fourth,2)
                
            Cache[setIndex][wordIndex][o] = fourth
            Cache[setIndex][wordIndex+1][o] = third
            Cache[setIndex][wordIndex+2][o] = second
            Cache[setIndex][wordIndex+3][o] = first
            
            memo = mem
            memo = int(memo, 2)
            memo = memo - int('0x2000', 16)
            
            memory[memo] = fourth
            memory[memo+1] = third
            memory[memo+2] = second
            memory[memo+3] = first
            
        Tag[setIndex][remove_way] = mem[0:16-set_offset-word_offset]
        LRU[setIndex].remove(remove_way)
        LRU[setIndex].append(remove_way)
        
    return(Cache, LRU, Tag, Valid)	

def instrExecution(line, pc, set_offset, word_offset, Cache, LRU, Tag, Valid):
        global cache_type
        global blk_size   #Block size in Bytes
        global num_ways   #Number of ways
        global total_s 
        global total_blk
        global Misses 
        global Hits
        global diagnosis
        global registers
      
        print("Current instruction PC =",pc)
        
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
            
        elif(line[0:2] == "lw"): # lw
            line = line.replace("lw","")
            line = line.replace(")","")
            line = line.replace("(",",")
            line = line.split(",")
            if(line[1][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[1],n) if (int(line[1],n) >= 0) else (65536 + int(line[1],n))
            rs = int(registers[("$" + str(line[2]))])
            instruction = "lw"
            print (instruction , ("$" + str(line[0])) , (str(imm) if(n== 10) else hex(imm))  + "("+("$" + str(line[2]))+")" )
            rt = "$" + str(line[0])
            mem = imm + rs
            memo= mem
            mem = mem - int('0x2000', 16)
            
            
            fourth = format(memory[mem], '08b') 
            third= format(memory[mem+1], '08b')
            sec = format(memory[mem+2], '08b') 
            first= format(memory[mem+3], '08b')
            word=  first +sec+ third+ fourth
            if word[0] == '1':
               word= int(word,2)
               word = word - 4294967296
            else:
                word= int(word,2)
            
            Cache, LRU, Tag, Valid = cacheAnalysis(Valid, Cache, memo, rt, Tag, LRU, 0, set_offset, word_offset)
            #registers[("$" + str(line[0]))] = word
            
            print ("result memory to Reg: ", ("$" + str(line[0])) ,"=", hex(word))
            pc+= 4# increments pc by 4 

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
            rt = int(registers[("$" + str(line[0]))])# need int convert here
            if rt < 0:
                maxnu= 4294967296
                 #convert to binary
                rt+= maxnu
                #rt= int("{0:b}".format(rt))
            instruction = "sw"
            print (instruction , ("$" + str(line[0])) , (str(imm) if(n== 10) else hex(imm))  + "("+("$" + str(line[2]))+")" )
            mem = imm + rs
            memo = mem
            mem = mem - int('0x2000', 16)
            rt = format(rt,'064b')
            first= rt[32:40]
            sec= rt[40:48]
            third= rt[48:56]
            fourth= rt[56:64]
            word=  first +sec+ third+ fourth
            first= int(first,2)
            sec= int(sec,2)
            third= int(third,2)
            fourth= int(fourth,2)
            word= int(word,2)
            print(" word_offset", word_offset)
            rt = "$" + str(line[0])

            Cache, LRU, Tag, Valid = cacheAnalysis(Valid, Cache, memo, rt, Tag, LRU, 1, set_offset, word_offset)
            #print ("result memory: ", hex(memo) ,"=", hex(word))
            pc+= 4# increments pc by 4 
            
           
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
            Cache, LRU, Tag, Valid = cacheAnalysisByte(Valid, Cache, memo, rt, Tag, LRU, 1, set_offset, word_offset)
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
            Cache, LRU, Tag, Valid = cacheAnalysisByte(Valid, Cache, memo, rt, Tag, LRU, 0, set_offset, word_offset)
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

        elif(line[0:3] == "beq"): # beq
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
            if rt < 0:
                u=1
            else:
                u=0
            rt= int(rt) if (int(rt) >= 0) else (4294967296 + int(rt))
            shamt = int(line[2])
            instruction = "sll" 
            print (instruction , rd ,("$" + str(line[1])), shamt)
            result = rt << shamt # does the addition operation
            result = format(result,'064b')
            result = int(result[32:],2) 
            print ("result:" ,rd ,"=", hex(result))
            result = result if( u !=1) else (result-4294967296)
            registers[rd]= result
           
            pc += 4 # increments pc by 4 
           # pcprint =  hex(pc)
           # print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
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

        elif(line[0:3] == "slt"): # SLT/U
            line = line.replace("slt","")
            if(line[0:1] == "u"):
               line = line.replace("u","")
               op = '101011'
            else:
                op= '101010'
            line = line.split(",")
            if(line[2][0:2]== "0x"):
                n=16
            else:
                n=10
            rd = "$" + str(line[0])
            rs = registers[("$" + str(line[1]))]
            rt = registers[("$" + str(line[2]))]
            rs= int(rs) if (int(rs) >= 0 or op == '101010') else (4294967296+ int(rs))
            rt= int(rt) if (int(rt) >= 0 or op == '101010') else (4294967296 + int(rt))
            instruction = "slt" if(op == '101010') else "sltu"
            #print (instruction , rt ,("$" + str(line[1])), imm if(n== 10) else hex(imm))
            if(rs < rt):
                result = 1
            else:
                result = 0
            registers[rd]= result # writes the value to the register specified
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
            if ((rt < 0) or (rs < 0)):
                u=1
            else:
                u=0
            rs= int(rs) if (int(rs) >= 0 ) else (4294967296 + int(rs))
            rt= int(rt) if (int(rt) >= 0 ) else (4294967296 + int(rt))
            instruction = "xor"
            print (instruction , rd ,("$" + str(line[1])), ("$" + str(line[2])))
            result = rs ^ rt # does the addition operation
            result = format(result,'064b')
            result = int(result[32:],2)
            print ("result:" ,rd ,"=", hex(result))
            result = result if( u !=1) else (result-4294967296)
            registers[rd]= result
            
            pc+= 4 # increments pc by 4 
             
           # pcprint =  hex(pc)
           # print(registers)# print all the registers and their values (testing purposes to see what is happening)
           # print(pc)
           # print(pcprint)
       
        elif(line[0:3] == "add"): # ADD/U
            line = line.replace("add","")
            if(line[0:1] == "u"):
               line = line.replace("u","")
               op = '100001'
            else:
                op = '100000'
            line = line.split(",")
            rd = "$" + str(line[0])
            rs = registers[("$" + str(line[1]))]
            rt = registers[("$" + str(line[2]))]
            rs= int(rs) if (int(rs) >= 0 or op == '100000') else (4294967296 + int(rs))
            rt= int(rt) if (int(rt) >= 0 or op == '100000') else (4294967296 + int(rt))
            instruction = "add"
            print (instruction , rd ,("$" + str(line[1])), ("$" + str(line[2])))
            result = rs + rt # does the addition operation
            result = format(result,'064b')
            if result[32]== '1':
                result = int(result[32:],2)
                print ("result:" ,rd ,"=", hex(result))
                result = result if( op =='100000') else (result-4294967296)
            else :
                result = int(result[32:],2)
                print ("result:" ,rd ,"=", hex(result))
            registers[rd]= result
            
            pc+= 4 # increments pc by 4 

        elif(line[0:3] == "sub"): # SUB
            line = line.replace("sub","")
            line = line.split(",")
            rd = "$" + str(line[0])
            rs = registers[("$" + str(line[1]))]
            rt = registers[("$" + str(line[2]))]
            instruction = "sub"
            print (instruction , rd ,("$" + str(line[1])), ("$" + str(line[2])))
            result = rs - rt # does the addition operation
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
        return pc, Cache, LRU, Tag, Valid;
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

def cache_def():
    global cache_type
    global blk_size   #Block size in Bytes
    global num_ways   #Number of ways
    global total_s 
    global total_blk
    global Misses 
    global Hits
    global diagnosis
    global registers
    if(cache_type == '1'):
        blk_size = 16    #Block size in Bytes
        num_ways = 1    #Number of ways
        total_s = 4   #Number of blocks/sets
        total_blk = num_ways * total_s
    elif(cache_type == '2'):
        blk_size = 8    #Block size in Bytes
        num_ways = 8    #Number of ways
        total_s = 1   #Number of blocks/sets
        total_blk = num_ways * total_s
    elif(cache_type == '3'):
        blk_size = 8    #Block size in Bytes
        num_ways = 2    #Number of ways
        total_s = 4   #Number of blocks/sets
        total_blk = num_ways * total_s
    elif(cache_type == '4'):
        blk_size = 8    #Block size in Bytes
        num_ways = 4    #Number of ways
        total_s = 2   #Number of blocks/sets
        total_blk = num_ways * total_s
    elif(cache_type == '5'):
        blk_size = input("Please insert a block size that is a power of 2: ")
        blk_size = int(blk_size)
        num_ways = input("Please insert how many ways: ")
        num_ways = int(num_ways)
        total_s = input("Please insert total sets that is a power of 2: ")
        total_s = int(total_s)
        total_blk = num_ways * total_s
    else:
        print("Invalid cache type, exiting program")
        #quit()
        
    return

def main():
    global cache_type
    global blk_size   #Block size in Bytes
    global num_ways   #Number of ways
    global total_s 
    global total_blk
    global Misses 
    global Hits
    global diagnosis
    global registers
    global controlSignals
    global controlSignals2
    global ft
    global de
    global ex
    global m
    global wb

    
   # f = open("mc.txt","w+")
    h = open("ProgramB_Testcase2","r")
    asm = h.readlines()
    instrs = []
    
    
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
    while True: 
        FinalDIC= 0
        FinalPC= 0
        TotalCycles= 0
        registers = defaultregisters.copy()
        controlSignals = controls.copy()
        controlSignals2 = controls2.copy()
        ft = defaultpipe.copy()
        #ft = defaultpipe.copy()
        de = defaultpipe.copy()
        ex = defaultpipe.copy()
        m = defaultpipe.copy()
        wb = defaultpipe.copy()
        print("Please enter if you want to enter diagnosis mode")
        diagnosis = input("0 - For No, 1 - For Yes: ")
        
        print("Please enter the type of cache that you want")
        print("1. a directly-mapped cache, block size of 16 Bytes, a total of 4 blocks (b=16; N=1; S=4)")
        print("2. a fully-associated cache, block size of 8 Bytes, a total of 8 blocks (b=8; N=8; S=1)")
        print("3. a 2-way set-associative cache, block size of 8 Bytes, 4 sets (b=8; N=2; S=4)")
        print("4. a 4-way set-associative cache, block size of 8 Bytes, 2 sets (b=8; N=4; S=2)")
        print("5. a custom cache b = ?, N = ?, S = ?")
        cache_type = input("Enter a choice: ")
        cache_def()
        word_offset = int(math.log(blk_size,2)) 
        set_offset = int(math.log(total_s,2))   
        print("\n")
        cpu = 5
        while cpu != "0" and cpu != "1":
            print("pipe line or multi cycle?")
            print("enter 1 for multicycle")
            print("0 for pipe line")
            cpu = input()
            if cpu != "1" and cpu != "0":
                print("\ninvalid option please enter one of the following options\n")
        print("\n")

        if cpu == "1":
            FinalDIC, FinalPC, TotalCycles = multiCycle(instrs, FinalDIC, FinalPC, TotalCycles, set_offset, word_offset)
        else:
            FinalDIC, FinalPC, TotalCycles = pipeline(instrs, FinalDIC, FinalPC, TotalCycles, set_offset, word_offset)

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
            print("memory","{}: {}".format(hex(mem),word), end='| ')
            if(k%7 == 0 and k > 0):
                print("\n")
            #print("memory", hex(mem)+": 0x"+ word )
    
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
   
        if(cpu=="1"):
            print("Final Multicycle Statistics ")
            per5 = (controlSignals["c5"]/FinalDIC)*100
            per4 = (controlSignals["c4"]/FinalDIC)*100
            per3 = (controlSignals["c3"]/FinalDIC)*100
            print("Dynamic Instruction Count: ",FinalDIC)
            print("Total Cycle Count: ",TotalCycles)
            print("Instruction Count with 3 Cycles: \n{} was executed\n {}%".format(controlSignals["c3"], per3))
            print("Instruction Count with 4 Cycles:  \n{} was executed\n {}%".format(controlSignals["c4"], per4))
            print("Instruction Count with 5 Cycles: \n{} was executed\n {}%".format(controlSignals["c5"], per5))
            cpi= (controlSignals["c5"]*5+controlSignals["c4"]*4+controlSignals["c3"]*3)/FinalDIC
            print("CPI: ({}*5+{}*4+{}*3)/{} = {}".format(controlSignals["c5"],controlSignals["c4"],controlSignals["c3"], FinalDIC, cpi))
            per5 = (controlSignals["MemtoReg"]/TotalCycles)*100
            per4 = (controlSignals["MemWrite"]/TotalCycles)*100
            per3 = (controlSignals["Branch"]/TotalCycles)*100
            per2 = (controlSignals["AluScrA"]/TotalCycles)*100
            per1 = (controlSignals["RegDst"]/TotalCycles)*100
            per0 = (controlSignals["RegWrite"]/TotalCycles)*100
            print("MemtoReg:{}% was 1".format(per5))
            print("MemWrite: {}% was 1".format(per4))
            print("Branch: {}% was 1".format(per3))
            print("ALUSrc: {}% was 1".format(per2))
            print("RegDst: {}% was 1".format(per1))
            print("RegWrite: {}% was 1".format(per0))
        else:
            print("Final Pipeline Statistics ")
            print("Dynamic Instruction Count: ",FinalDIC)
            print("Total Cycle Count: ",TotalCycles)
            stat= str(stats)
            stat= stat.replace("'","")
            stat= stat.replace("{","")
            stat= stat.replace("}","")
            stat= stat.replace(",","\n")
            print(" "+ stat)
            #print(stats, sep= '|')
        print("Hit Rate = ", Hits/(Hits+Misses), "%")
        print("Would you like to exit the program?(y/n)")
        con = input()
        if con == "y":
            registers = defaultregisters.copy()
            return


if __name__ == "__main__":
    main()