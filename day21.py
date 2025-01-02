import pytest
import math
from helpers import load_lines

""" This looks horrible.
Some versions of this code is able to get the correct answer for the mocks
but not for the main puzzle. Abandoned.
"""


DIR={'v':(0,1),'^':(0,-1),'<':(-1,0),'>':(1,0)}

KEYPAD={'A':(0,0),'0':(-1,0),
        '1':(-2,-1),'2':(-1,-1),'3':(0,-1),
        '4':(-2,-2),'5':(-1,-2),'6':(0,-2),
        '7':(-2,-3),'8':(-1,-3),'9':(0,-3)}

DIRPAD={'A':(0,0),'^':(-1,0),
        '<':(-2,1),'v':(-1,1),'>':(0,1)}


def _pad_to_directional(codes, pad):
    "returns directional movements to get codes in the pad"
    # note to self, there will be multiple routes, just returning one for now
    # & hoping the they it will be shorter when convered later
    result=""
    x,y=pad['A']
    for k in codes:
        tx,ty=pad[k]
        # get from x,y to tx,ty, then press
        dx,dy=tx-x,ty-y
##        print(f"key {k} delta {(dx,dy)}")
        if dx<0:
            result+='<'*abs(dx)
        elif dx>0:
            result+='>'*abs(dx)
        if dy<0:
            result+='^'*abs(dy)
        elif dy>0:
            result+='v'*abs(dy)
        result+='A'
        x,y=tx,ty
    return result

def pad_to_directional(codes, pad):
    "returns directional movements to get codes in the pad"
    # note to self, there will be multiple routes, just returning one for now
    # & hoping the they it will be shorter when convered later
    result=""
    x,y=pad['A']
    for k in codes:
        tx,ty=pad[k]
        # get from x,y to tx,ty, then press
        # special case: it HAS to go via existing keys,
        # it cannot enter an area with no key's

        dx,dy=tx-x,ty-y
        # check if can go on X all the way
        # (don't need to check all the the end)
        if (tx,y) in pad.values():
            if dx<0:
                result+='<'*abs(dx)
            elif dx>0:
                result+='>'*abs(dx)
            if dy<0:
                result+='^'*abs(dy)
            elif dy>0:
                result+='v'*abs(dy)
        else:
            # go Y first
            if dy<0:
                result+='^'*abs(dy)
            elif dy>0:
                result+='v'*abs(dy)
            if dx<0:
                result+='<'*abs(dx)
            elif dx>0:
                result+='>'*abs(dx)
        result+='A'
        x,y=tx,ty
    return result

def keypad_to_directional(keypad):
    "returns directional movements to get keypad"
    return pad_to_directional(keypad,KEYPAD)
        
def dirpad_to_directional(direct):
    "returns directional movements to get direct"
    return pad_to_directional(direct,DIRPAD)


def day21a(fname):
    total=0
    for line in load_lines(fname):
        r1=keypad_to_directional(line)
        r2=dirpad_to_directional(r1)
        result=dirpad_to_directional(r2)
        lnresult=len(result)
        key=int(line[:3])
        print(line,"\n",r1,"\n",r2,"\n",result)
        print(lnresult,key)
        total+=lnresult*key
    return total
    
################################################################
if __name__ == "__main__":
    print("day21a", day21a("input21.txt"))
##    print("day20b", day20b("input20.txt"))


################################################################


def test_keypad_to_directional():
    assert keypad_to_directional("029A")=="<A^A>^^AvvvA"
    
def test_dirpad_to_directional():
    assert dirpad_to_directional("<A^A>^^AvvvA")=="v<<A>>^A<A>AvA<^AA>A<vAAA>^A"

def test_steps():
    # all the steps
    # cannot use the case from the page as sometimes the ordering changes
    k0="029A"
    k1=keypad_to_directional(k0)
    k2=dirpad_to_directional(k1)
    k3=dirpad_to_directional(k2)
    assert k1=="<A^A>^^AvvvA"
    assert k2=="v<<A>>^A<A>AvA<^AA>A<vAAA>^A"
    assert k3=="<vA<AA>>^AvAA<^A>Av<<A>>^AvA^A<vA>^Av<<A>^A>AAvA^Av<<A>A>^AAAvA<^A>A"

def test_steps2():
    cases={"029A": "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A",
    "980A": "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A",
    "179A": "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
    "456A": "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A",
    "379A": "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"}

    for source,expected in cases.items():
        # note: my algo gives "v<<A" instead of "<v<A", so accepting either
        expected2=expected.replace("<v<A","v<<A")
        r1=keypad_to_directional(source)
        r2=dirpad_to_directional(r1)
        result=dirpad_to_directional(r2)
        print(result)
        print(expected)
        print(expected2)
        assert result==expected or result==expected2

def test_day21a():
    assert day21a("test21.txt")==126384
