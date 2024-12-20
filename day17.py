import pytest
import math
from time import perf_counter as clock
from helpers import load_lines

""" At last the virtual machine question :-)
Part A no problem.
Part B looks worrying, it seems quick, but not sure if brute force will work.
manages 1 million in 9.3 seconds & doesn't find it.

Improved version can check 1 million in 1.84 seconds, but still too slow.
Either a logic error or we need to address it differently.
~30 minutes for 1 billion items. Leaving this.
"""

def parse_data(fname):
    "returns (a,b,c,[ops])"
    data=load_lines(fname)
    post_colon = lambda s : s.split(":")[1]
    a=int(post_colon(data[0]))
    b=int(post_colon(data[1]))
    c=int(post_colon(data[1]))
    ops=[int(v) for v in post_colon(data[4]).split(",")]
    return (a,b,c,ops)


def process(a,b,c,ops):
    "returns a,b,c,[output]"
    ip=0 # instruction ptr
    lnops=len(ops)
    output=[]

    def literal(oc):
        "returns the literal value"
        return oc

    def combo(oc):
        "returns the combo value"
        if oc<=3: return oc
        if oc==4: return a
        if oc==5: return b
        if oc==6: return c
        print("invalid opcode",oc)
        assert False
    
    while 0<=ip and ip<lnops:
        opcode=ops[ip]
        operand=ops[ip+1]
        if opcode == 0: #adv
            a//= 2** combo(operand)
        elif opcode==1: # bxl
            b ^= literal(operand)
        elif opcode==2: # bst
            b = combo(operand) % 8
        elif opcode==3: # jnz
            if a!= 0:
                ip=literal(operand)-2 # -2 to offset the +2 later
        elif opcode==4: # bxc
            b ^= c
        elif opcode==5: #out
            output.append(combo(operand)%8)
        elif opcode==6: #bdv
            b = a// 2**combo(operand)
        elif opcode==7: #cdv
            c = a// 2**combo(operand)
        else:
            print(f"bad opcode {opcode} at IP {ip} operand {operand}")
            break
##        print(f"ip {ip} abc {a} {b} {c}")
        ip+=2
    return a,b,c,output


def day17a(fname):
    a,b,c,ops = parse_data(fname)
    a,b,c,out= process(a,b,c,ops)
    return ",".join((str(v) for v in out))

def slow_day17b(a,b,c,ops):
    "takes 9.3 seconds to process 1 million items"
    a=0
    start=clock()
    while a<1000*1000:
        _,_,_,out= process(a,b,c,ops)
        if out==ops:
            return a        
        a+=1
        if a%10000==0:
            taken=clock()-start
            print(f"{a} {taken:.2f}")
    print("not found")
    

def process_to_match(a,b,c,ops, expected):
    "returns if output matches expected"
    ip=0 # instruction ptr
    lnops=len(ops)
    outlen=0 # length of output

    def literal(oc):
        "returns the literal value"
        return oc

    def combo(oc):
        "returns the combo value"
        if oc<=3: return oc
        if oc==4: return a
        if oc==5: return b
        if oc==6: return c
        print("invalid opcode",oc)
        assert False
    
    while 0<=ip and ip<lnops:
        opcode=ops[ip]
        operand=ops[ip+1]
        if opcode == 0: #adv
            a//= 2** combo(operand)
        elif opcode==1: # bxl
            b ^= literal(operand)
        elif opcode==2: # bst
            b = combo(operand) % 8
        elif opcode==3: # jnz
            if a!= 0:
                ip=literal(operand)-2 # -2 to offset the +2 later
        elif opcode==4: # bxc
            b ^= c
        elif opcode==5: #out
            val = combo(operand)%8
            # check expected[outlen]== val
            if outlen<len(expected) and expected[outlen]==val:
                outlen+=1
            else:
                return False
        elif opcode==6: #bdv
            b = a// 2**combo(operand)
        elif opcode==7: #cdv
            c = a// 2**combo(operand)
        else:
            print(f"bad opcode {opcode} at IP {ip} operand {operand}")
            break
##        print(f"ip {ip} abc {a} {b} {c}")
        ip+=2
    return outlen==len(expected)

def day17b(a,b,c,ops):
    "quicker: 3 minutes for 100 million, but its still too slow"
    a=0
    start=clock()
    while a<1000*1000*1000:
        if process_to_match(a,b,c,ops,ops):
            return a

        a+=1
        if a%10000==0:
            taken=clock()-start
            print(f"{a} {taken:.2f}")
    print("not found")

def ops_to_str(ops):
    "converts operations to a 'user readable form'"

    def combo(operand):
        if operand<=3: return str(operand)
        if operand == 4: return "a"
        if operand==5: return "b"
        if operand==6: return "c"
    
    ip=0
    while ip<len(ops):
        opcode=ops[ip]
        operand=ops[ip+1]
        if opcode==0:
            print(f"{ip}: adv {combo(operand)}")
        elif opcode==1:
            print(f"{ip}: bxl {combo(operand)}")
        elif opcode==2:
            print(f"{ip}: bst {combo(operand)}")
        elif opcode==3:
            print(f"{ip}: jnz {operand}")
        elif opcode==4:
            print(f"{ip}: bxc")
        elif opcode==5:
            print(f"{ip}: out {combo(operand)}")
        elif opcode==6:
            print(f"{ip}: bdv {combo(operand)}")
        elif opcode==7:
            print(f"{ip}: cdv {combo(operand)}")
        ip+=2
        
        

################################################################
if __name__ == "__main__":
##    print("day17a", day17a("input17.txt"))
##    _,_,_,out=process(2024,0,0,[0,3,5,4,3,0])
##    print("partb-2024",out)
##    _,_,_,out=process(117440,0,0,[0,3,5,4,3,0])
##    print("partb-117440",out)
    a,b,c,ops=parse_data("input17.txt")
    ops_to_str(ops)
##    print("day17b",day17b(a,b,c,ops))
    

################################################################


def test_parse_data():
    a,b,c,ops = parse_data("test17.txt")
    assert (a,b,c)==(729,0,0)
    assert ops==[0,1,5,4,3,0]

def test_process():
    a,b,c,out= process(0,0,9,[2,6])
    assert b==1

    a,b,c,out= process(10,0,0,[5,0,5,1,5,4])
    assert out==[0,1,2]

    a,b,c,out= process(2024,0,0,[0,1,5,4,3,0])
    assert out==[4,2,5,6,7,7,7,7,3,1,0]
    assert a == 0

    a,b,c,out= process(0,29,0,[1,7])
    assert b==26

    a,b,c,out= process(0,2024,43690,[4,0])
    assert b==44354

def test_day17a():
    assert day17a("test17.txt") == "4,6,3,5,6,3,5,2,1,0"

def test_day17b():
    assert slow_day17b(2024,0,0,[0,3,5,4,3,0]) == 117440

def test_day17b_2():
    assert day17b(2024,0,0,[0,3,5,4,3,0]) == 117440
