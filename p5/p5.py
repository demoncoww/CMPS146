import json
from heapq import heappush, heappop
from collections import namedtuple

with open('Crafting.json') as f:
    Crafting = json.load(f)

# List of items that can be in your inventory:
print Crafting['Items']

# List of items in your initial inventory with amounts:
print Crafting['Initial']

# List of items needed to be in your inventory at the end of the plan:
# (okay to have more than this; some might be satisfied by initial inventory)
print Crafting['Goal']

# Dict of crafting recipes (each is a dict):
print Crafting['Recipes']['craft stone_pickaxe at bench']

def make_checker(rule):
    # TODO: Add code here
    # this code runs once
    # do something with rule['Consumes'] and rule['Requires']
    def check(state):
        # TODO: Add code here
        # this code runs millions of times
        return True

    return check

def make_effector(rule):
    # TODO: Add code here
    # this code runs once
    # do something with rule['Produces'] and rule['Consumes']
    def effect(state):
        # TODO: Add code here
		# this code runs millions of times
        return next_state

    return effect

def make_goal_checker(goal):
    goal_state = ()
    for index, name in enumerate(Items):
        if name in goal:
           goal_state.append(index, goal[name])
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
    return tuple(d.get(name,0) for i,name in enumerate(Items))

#h = inventory_to_tuple(state_dict)

def make_initial_state(inventory):
    return inventory_to_tuple(inventory)

initial_state = make_initial_state(Crafting['Initial'])

# Container class for holding compiled recipes
Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []
for name, rule in Crafting['Recipes'].items():
    checker = make_checker(rule)
    effector = make_effector(rule)
    recipe = Recipe(name, checker, effector, rule['Time'])
    all_recipes.append(recipe)

def search(graph, initial, is_goal, limit, heuristic):
    start = initial
    queue = [(0, start)]
    parent = {start : None}
    dist = {start : 0}
    while limit > 0:
        cDist, node = heappop(queue)
        if is_goal(node):
            plan, curr = [], node
            while curr is not None:
                plan.append(curr)
                curr = parent[curr]
            plan.reverse()
            return dist[node], plan
        for adj in graph(node):
            #print neighbor
            action, neighbor, cost = adj
            newDist = dist[node] + cost
            if (neighbor not in dist) or (newDist < dist[neighbor]):
                dist[neighbor] = newDist
                heappush(queue, (newDist+heuristic(neighbor), neighbor))
                parent[neighbor] = node
        limit -= 1
    return 0, []















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
