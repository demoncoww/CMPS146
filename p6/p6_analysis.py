from p6_game import Simulator
from heapq import heappush, heappop
from collections import OrderedDict

ANALYSIS = OrderedDict()
PREV = OrderedDict()
VISITED = {}
Specials = {}

def analyze(design):
    ANALYSIS.clear()
    VISITED.clear()
    PREV.clear()
    Specials.clear
    sim = Simulator(design)
    init = sim.get_initial_state() #states are position, abilities
    pos, abilities = init
    moves = sim.get_moves() #get_moves returns UP, DOWN, ... , NOTHING
    queue = []
    heappush(queue, init)
    VISITED[init] = True
    PREV[(1,1)] = (1,1)

    for i in sim.specials:
        Specials[i] = sim.specials[i]

    while queue:
        curr_state = heappop(queue)
        pos, abilities = curr_state
        if pos not in ANALYSIS:
            ANALYSIS[pos] = abilities
        for m in moves:
            next_state = sim.get_next_state(curr_state, m)
            if next_state:
                if not VISITED.get(next_state):
                    heappush(queue, next_state)
                    VISITED[next_state] = True
                    if not PREV.get(next_state[0]):
                        PREV[next_state[0]] = pos



def inspect((i,j), draw_line):
    dst = (i, j)
    if dst in ANALYSIS:
        src = Specials[0]
        curr = PREV[dst]
        prev = dst
        path = []

        if ANALYSIS[dst]:
            num = len(ANALYSIS[dst])


        else:
            while prev != src:
                path.append((prev, curr))
                prev = curr
                curr = PREV[curr]

        for c, p in path:
            draw_line(p, c)


        print "Looking at", dst, "is reachable with", ANALYSIS[dst]
    else:
        print "Unreachable location", dst
        
        
        