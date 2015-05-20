from p6_game import Simulator
from heapq import heappush, heappop
import Queue as Q
import p6_tool

ANALYSIS = {}

def analyze(design):

    sim = Simulator(design)
    init = sim.get_initial_state() #states are position, abilities
    ANALYSIS = {init: None}
    queue = Q.PriorityQueue()
    queue.put((0, init[0], init[1]))

    while not queue.empty():
        curr_state = queue.get()
        moves = sim.get_moves()
        states = []

        for m in moves:
            print curr_state
            if sim.get_next_state((curr_state[1], curr_state[2]), m) != None:
                pos, abs = sim.get_next_state((curr_state[1], curr_state[2]), m)
                state = (curr_state[0] + 1, pos, abs)
                states.append(state)

        for s in states:
            this = (s[1], s[2])
            if this not in ANALYSIS:
                ANALYSIS[this] = (curr_state[1], curr_state[2])
                queue.put(s)

    return ANALYSIS

def inspect((i,j), draw_line, analysis):

    for this in analysis:
        if this[0] == (i, j):
            curr = this
            color = p6_tool.make_color()
            offset = p6_tool.make_offset()
            while analysis[curr] != None:
                print "drawing at", curr[0]
                draw_line(curr[0], analysis[curr][0], offset, color)
                curr = analysis[curr]
        
        
        