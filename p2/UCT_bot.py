import time
import random
import math
THINK_DURATION = 1

class Node:
	def __init__(self, move = None, parent = None, state = None):
		self.move = move # the move that got us to this node - "None" for the root node
		self.parentNode = parent # "None" for the root node
		self.childNodes = []
		self.visits = 0
		self.wins = 0
		self.untriedMoves = state.get_moves() # future child nodes
		self.playerJustMoved = state.get_whos_turn() # the only part of the state that the Node needs later

	def UCTSelectChild(self):
		s = sorted(self.childNodes, key = lambda c: (float(c.wins)/float(c.visits)) + math.sqrt(2 * math.log(float(self.visits) / float(c.visits))))
		return s

	def AddChild(self, m, s):
		n = Node(move = m, parent = self, state = s)
		self.untriedMoves.remove(m)
		self.childNodes.append(n)
		return n

	def Update(self, result):
		self.visits += 1
		self.wins += result

	def __repr__(self):
		return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

	def TreeToString(self, indent):
		s = self.IndentString(indent) + str(self)
		for c in self.childNodes:
			s += c.TreeToString(indent+1)
		return s

	def IndentString(self,indent):
		s = "\n"
		for i in range (1,indent+1):
			s += "| "
		return s

	def ChildrenToString(self):
		s = ""
		for c in self.childNodes:
			s += str(c) + "\n"
		return s

def think(state, quip):

	rootnode = Node(state = state)
	t_start = time.time()
	t_time = time.time()
	t_deadline = t_start + THINK_DURATION

	iterations = 0
	rollouts = 0

	def their_score(score, opponent):
		if opponent == 'red':
			return score['red'] - score['blue']
		else:
			return score['blue'] - score['red']

	while iterations in range(1000):

		iterations += 1
		t_time = time.time()
		node = rootnode
		copy_state = state.copy()

		#check to make sure non-terminal, use given UCB call
		while node.childNodes != [] and node.untriedMoves == []:
			node = node.UCTSelectChild()
			copy_state.apply_move(node.move)

		#try to expand and move down the tree
		if node.untriedMoves != []:
			turn = state.get_whos_turn()
			move = random.choice(node.untriedMoves)
			copy_state.apply_move(move)
			node = node.AddChild(move,copy_state)

		#Rollout Function
		while copy_state.get_moves() != []:
			copy_state.apply_move(random.choice(copy_state.get_moves()))

		#Propagate
		score = copy_state.get_score()
		while node != None:
			result = their_score(score, node.playerJustMoved)
			node.Update(result)
			node = node.parentNode

	rate = float(iterations)/(t_time - t_start)
	print "Rollout Rate is ", rate
	return sorted( node.childNodes , key = lambda c: c.visits)[-1].move
	
