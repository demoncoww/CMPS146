from p6_game import Simulator
from heapq import heappush, heappop

ANALYSIS = {}
VISITED = {}
Start = (0,0)

def analyze(design):
    sim = Simulator(design)
    init = sim.get_initial_state() #states are position, abilities
    pos, abilities = init
    Start = pos
    moves = sim.get_moves() #get_moves returns UP, DOWN, ... , NOTHING
    queue = []
    heappush(queue, init)
    VISITED[init] = True

    while queue:
        curr_state = heappop(queue)
        pos, abilities = curr_state
        ANALYSIS[pos] = abilities
        for m in moves:
            next_state = sim.get_next_state(curr_state, m)
            if next_state: #if move is valid
                if VISITED.get(next_state) != True:
                    heappush(queue, next_state)
                    VISITED[next_state] = True


def inspect((i,j), draw_line):
    dst = (i, j)
    src = Start
    draw_line(src, dst)



