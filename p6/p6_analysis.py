from p6_game import Simulator
from heapq import heappush, heappop
from collections import OrderedDict

ANALYSIS = OrderedDict()
VISITED = {}
Start = {}
ADJ = {}

def analyze(design):
    sim = Simulator(design)
    init = sim.get_initial_state() #states are position, abilities
    pos, abilities = init
    Start[0] = pos
    moves = sim.get_moves() #get_moves returns UP, DOWN, ... , NOTHING
    queue = []
    heappush(queue, init)
    VISITED[init] = True
    lisNpos = [(0,0)]

    while queue:
        curr_state = heappop(queue)
        pos, abilities = curr_state
        ANALYSIS[pos] = abilities
        for m in moves:
            next_state = sim.get_next_state(curr_state, m)
            if next_state: #if move is valid
                """lisNpos[0] = next_state[0]
                if m != 'NOTHING' and pos != next_state[0]:
                    if not pos in ADJ:
                        ADJ[pos] = lisNpos
                    else:
                        ADJ[pos] = ADJ[pos] + lisNpos"""
                if VISITED.get(next_state) != True:
                    heappush(queue, next_state)
                    VISITED[next_state] = True
                    
    #for i in ANALYSIS:
    #    if 
    
    print ADJ

def inspect((i,j), draw_line):
    children = {}
    parent = {}
    dst = (i, j)
    src = Start[0]
    path = []
    queue = {}
    
    
    #while queue:
    #    pos = heappop(queue)
        
        
        