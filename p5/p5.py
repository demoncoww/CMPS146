import json
from heapq import heappush, heappop
from collections import namedtuple

with open('Crafting.json') as f:
    Crafting = json.load(f)

# List of items that can be in your inventory:
#print Crafting['Items']

# List of items in your initial inventory with amounts:
#print Crafting['Initial']

# List of items needed to be in your inventory at the end of the plan:
# (okay to have more than this; some might be satisfied by initial inventory)
#print Crafting['Goal']

# Dict of crafting recipes (each is a dict):
#print Crafting['Recipes']['craft stone_pickaxe at bench']

def make_checker(rule):
    # rule['Consumes'] and rule['Requires']
    consumes = []
    requires = []
    for index, name in enumerate(Crafting['Items']):
        if 'Consumes' in rule:
            if name in rule['Consumes']:
                consumes.append((index, rule['Consumes'][name]))
        if 'Requires' in rule:
            if name in rule['Requires']:
                requires.append((index, rule['Requires'][name]))

    def check(state):
        for i,a in consumes:
            if state[i] < a:
                return False
        for i,a in requires:
            if state[i] != a:
                return False
        return True

    return check

def make_effector(rule):
    # rule['Produces'] and rule['Consumes']
    consumes = []
    produces = []
    for index, name in enumerate(Crafting['Items']):
        if 'Consumes' in rule:
            if name in rule['Consumes']:
                consumes.append((index, rule['Consumes'][name]))
        if 'Produces' in rule:
            if name in rule['Produces']:
                produces.append((index, rule['Produces'][name]))
    def effect(state):
        next_state = []
        for i in state:
            next_state.append(i)
        #print next_state
        for i,a in consumes:
            next_state[i] -= a
        for i,a in produces:
            #print next_state[i],a
            next_state[i] += a
        return tuple(next_state)

    return effect

def make_goal_checker(goal):
    goal_state = []
    for index, name in enumerate(Crafting['Items']):
        if name in goal:
           goal_state.append((index, goal[name]))
    def is_goal(state):
        for i,a in goal_state:
            if state[i] < a:
                return False
        return True

    return is_goal

is_goal = make_goal_checker(Crafting['Goal'])

def graph(state):
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)

def heuristic(state):
    return 0

def inventory_to_tuple(d):
    return tuple(d.get(name,0) for i,name in enumerate(Crafting['Items']))

#h = inventory_to_tuple(state_dict)

def make_initial_state(inventory):
    return inventory_to_tuple(inventory)

initial_state = make_initial_state(Crafting['Initial'])

def search(graph, initial, is_goal, limit, heuristic):
    start = initial
    queue = [(0, start)]
    parent = {start : None}
    dist = {start : 0}
    while limit > 0:
        cDist, node = heappop(queue)
        if is_goal(node):
            plan, curr = [], node
            while parent[curr] is not None:
                cost,action, par = parent[curr]
                plan.append((cost,action,curr))
                curr = par
            plan.reverse()
            return dist[node], plan
        for adj in graph(node):
            #print neighbor
            action, neighbor, cost = adj
            newDist = dist[node] + cost
            if (neighbor not in dist) or (newDist < dist[neighbor]):
                dist[neighbor] = newDist
                heappush(queue, (newDist+heuristic(neighbor), neighbor))
                parent[neighbor] = (cost,action,node)
        limit -= 1
    return 0, []

# Container class for holding compiled recipes
Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []
for name, rule in Crafting['Recipes'].items():
    checker = make_checker(rule)
    effector = make_effector(rule)
    recipe = Recipe(name, checker, effector, rule['Time'])
    all_recipes.append(recipe)

#print initial_state
#print is_goal(initial_state)
search(graph,initial_state,is_goal,5000,heuristic)
















t_initial = 'a'
t_limit = 20

edges = {'a': {'b':1,'c':10}, 'b':{'c':1}}

def t_graph(state):
	for next_state, cost in edges[state].items():
		yield ((state,next_state), next_state, cost)

def t_is_goal(state):
	return state == 'c'

def t_heuristic(state):
	return 0

#print search(t_graph, t_initial, t_is_goal, t_limit, t_heuristic)
