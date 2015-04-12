import time

THINK_DURATION = 1

def think(state, quip):

    t_start = time.time()
    t_deadline = t_start + THINK_DURATION

    iterations = 0

    while True:

        iterations += 1
        # select, expand, rollout, then backpropagate logic here

        t_now = time.time()
        if t_now > t_deadline:
            break

    sample_rate = float(iterations)/(t_now - t_start)