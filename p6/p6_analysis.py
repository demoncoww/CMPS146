from p6_game import Simulator
from heapq import heappush, heappop
import Queue as Q
import p6_tool

ANALYSIS = {}

def analyze(design):
    """ANALYSIS.clear()
    VISITED.clear()
    PREV.clear()
    Specials.clear"""
    sim = Simulator(design)
    p, a = sim.get_initial_state() #states are position, abilities
    queue = Q.PriorityQueue()
    queue.put((0, p, a))

    while not queue.empty():
        curr_state = queue.get()
        moves = sim.get_moves()
        states = []
        for m in moves:
            if sim.get_next_state((curr_state[1], curr_state[2]), m) != None:
                pos, abs = sim.get_next_state((curr_state[1], curr_state[2]), m)
                state = (curr_state[0] + 1, pos, abs)
                states.append(state)
        for s in states:
            this = (s[1], s[2])
            if this not in ANALYSIS:
                ANALYSIS[this] = (curr_state[1], curr_state[2])
                queue.put(s)



def inspect((i,j), draw_line):

    for this in ANALYSIS:
        if this[0] == (i, j):
            curr = this
            color = p6_tool.make_color()
            offset = p6_tool.make_offset()
            while ANALYSIS[curr] != None:
                draw_line(curr[0], ANALYSIS[curr][0], offset, color)
                curr = ANALYSIS[curr]
        
        
        