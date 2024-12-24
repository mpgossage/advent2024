import pytest
import math
from helpers import load_lines

""" This looks complex, brushfire should work,
but the cheat mechanism is going to make it more complex.
Part A ok, Part B failed with too high!
Found issue as I didn't consider it must be manhatten 20.
Now it fails with item too small.
I think its an issue as I brushfire from the start to end, not the other way.
No, that makes no difference.
Abandoned.
"""

WALL='#'
SPACE='.'
START,END='S','E'
DIR=[(0,1),(0,-1),(-1,0),(1,0)]
BIG=1e7

def parse_data(fname):
    "returns 2d grid of int/WALL & start,end pos"
    start,end=None,None
    result=[]
    for y,line in enumerate(load_lines(fname)):
        r=[]
        for x,v in enumerate(line):
            if v==START:
                start=(x,y)
            elif v== END:
                end=(x,y)
            if v== WALL:
                r.append(WALL)
            else:
                r.append(BIG)
        result.append(r)
    return result,start,end

def brushfire(grid,start):
    sx,sy=len(grid[0]),len(grid)
    todo=set([start])
    grid[start[1]][start[0]]=0
    while todo:
        px,py=todo.pop()
        cost=grid[py][px]+1
        for dx,dy in DIR:
            nx,ny=px+dx,py+dy
            if 0<=nx<sx and 0<=ny<sy and grid[ny][nx]!=WALL:
                if grid[ny][nx]>cost:
                    grid[ny][nx]=cost
                    todo.add((nx,ny))
    return grid
        
def find_shortcuts(grid):
    "returns a dict of shortcuts"
    cheats={}
    sx,sy=len(grid[0]),len(grid)
    for y in range(1,sy-1):
        for x in range(1,sx-1):
            cost=grid[y][x]
            if cost==WALL: continue
            # going to look for 2 steps
            for dx1,dy1 in DIR:
                tx,ty=x+dx1,y+dy1
                # must be a wall
                if 0<=tx<sx and 0<=ty<sy:
                    if grid[ty][tx]!=WALL: continue
                    for dx2,dy2 in DIR:
                        # must be clear & higher value
                        tx,ty=x+dx1+dx2,y+dy1+dy2
                        if 0<=tx<sx and 0<=ty<sy:
                            c=grid[y+dy1+dy2][x+dx1+dx2]
                            if c!= WALL and c>cost+2:
                                delta=c-cost-2 # still have to pay for the 2 steps
                                cheats[delta]=cheats.get(delta,0)+1
    return cheats


def day20a(fname):
    grid,start,end = parse_data(fname)
    grid=brushfire(grid,start)
    cheats=find_shortcuts(grid)
##    print("cheats",cheats)
    result=0
    for k,v in cheats.items():
        if k>=100:
            result+=v
    return result

def find_shortcuts2(grid,limit):
    "returns a dict of shortcuts"
    #helper
    manhatten=lambda dx,dy:abs(dx)+abs(dy)
    
    cheats={}
    sx,sy=len(grid[0]),len(grid)
    for y in range(sy):
        for x in range(sx):
            cost=grid[y][x]
            if cost==WALL: continue
            # look limits
            lminx,lmaxx=max(0,x-limit),min(sx,x+limit)
            lminy,lmaxy=max(0,y-limit),min(sy,y+limit)
            for cy in range(lminy,lmaxy):
                for cx in range(lminx,lmaxx):
                    mdist=manhatten(cx-x,cy-y)
                    if grid[cy][cx]==WALL or mdist>limit: continue
                    delta=cost-grid[cy][cx]-mdist
                    if delta>0:
                        cheats[delta]=cheats.get(delta,0)+1
    return cheats

def day20b(fname):
    grid,start,end = parse_data(fname)
    grid=brushfire(grid,end)
    cheats=find_shortcuts2(grid,20)
    result=0
    for k,v in cheats.items():
        if k>=100:
            result+=v
    return result
 
    
################################################################
if __name__ == "__main__":
    print("day20a", day20a("input20.txt"))
    print("day20b", day20b("input20.txt"))


################################################################


def test_parse_data():
    grid,start,end = parse_data("test20.txt")
    assert len(grid) == 15
    assert len(grid[0])==15
    assert start==(1,3)
    assert end==(5,7)
    
def test_brushfire():
    grid,start,end = parse_data("test20.txt")
    grid=brushfire(grid,start)
    assert grid[3][1]==0
    assert grid[1][1]==2
    assert grid[7][5]==84

def test_find_shortcuts():
    grid,start,end = parse_data("test20.txt")
    grid=brushfire(grid,start)
    cheats=find_shortcuts(grid)
    assert len(cheats)==11
    assert cheats[2]==14
    assert cheats[64]==1
    
def test_find_shortcuts2():
    grid,start,end = parse_data("test20.txt")
    grid=brushfire(grid,start)
    cheats=find_shortcuts2(grid,20)
    assert cheats[50]==32
    assert cheats[52]==31
    assert cheats[54]==29
    assert cheats[56]==39
    assert cheats[58]==25
    assert cheats[60]==23
    assert cheats[62]==20
    assert cheats[64]==19
    assert cheats[66]==12
    assert cheats[68]==14
    assert cheats[70]==12
    assert cheats[72]==22
    assert cheats[74]==4
    assert cheats[76]==3
