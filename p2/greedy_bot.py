import random

MAX_DEPTH = 1

def think(state, quip):

	moves = state.get_moves()

	best_move = moves[0]
	best_expecation = float('-inf')

	me = state.get_whos_turn()

	def outcome(score):
		if me == 'red':
			return score['red'] - score['blue']
		else:
			return score['blue'] - score['red']

	for move in moves:

		total_score = 0.0

		greedy_state = state.copy()

		greedy_state.apply_move(move)

		for i in range(MAX_DEPTH):
			if greedy_state.is_terminal():
				break
			greedy_move = random.choice( greedy_state.get_moves() )
			greedy_state.apply_move( greedy_move )

		total_score += outcome(greedy_state.get_score())

		expectation = float(total_score)

		if expectation > best_expecation:
			best_expecation = expectation
			best_move = move

	#print "Picking %s with expected score %f" % (str(best_move), best_expecation)
	return best_move