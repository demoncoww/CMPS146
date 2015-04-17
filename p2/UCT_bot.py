import time
import random
THINK_DURATION = 1

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.visits = 0
        self.wins = state.get_score()
        self.untriedMoves = state.get_moves() # future child nodes
        self.playerJustMoved = state.get_whos_turn() # the only part of the state that the Node needs later

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
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

    t_start = time.time()
    t_deadline = t_start + THINK_DURATION
    nodethatisroot = Node(None, None,state)
    node = nodethatisroot
    copystate = state.copy()
    iterations = 0
   # v[0] = state.copy()
    while iterations in range(1000):

        iterations += 1
        # select, expand, rollout, then backpropagate logic here
        #slect
        while copystate.is_terminal()== False and node.untriedMoves == []:
            node = node.UCTSelectChild()
            copystate.apply_move(node.move)


        bloot = node.untriedMoves
        if bloot != []:
                m = random.choice(node.untriedMoves)
                copystate.apply_move(m)
                node.AddChild(m,copystate)

        #rollout
        while copystate.get_moves()!=[]:
            copystate.apply_move(random.choice(copystate.get_moves()))

        while node.parentNode != None:
             node.Update(state.get_score())
             node = node.parentNode
        t_now = time.time()
        if t_now > t_deadline:
            break
    return sorted( node.childNodes , key = lambda c: c.visits)[-1].move
    sample_rate = float(iterations)/(t_now - t_start)