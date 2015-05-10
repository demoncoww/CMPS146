import json, time, math
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

def inventory_to_tuple(d):
    return tuple(d.get(name,0) for i,name in enumerate(Crafting['Items']))

def make_initial_state(inventory):
    return inventory_to_tuple(inventory)

initial_state = make_initial_state(Crafting['Initial'])

def make_heuristic():
    maxAmount = {}
    for item in Crafting['Items']:
        maxAmount[item] = 0
    goal = Crafting['Goal']
    for action in Crafting['Recipes'].values():
        if 'Produces' in action:
            for item, amount in action['Produces'].items():
                if item in goal:
                    maxCraft = math.ceil(goal[item]/float(amount))*amount
                    #print goal[item]/amount
                    if maxAmount[item] < maxCraft:
                        maxAmount[item] = maxCraft
        if 'Requires' in action:
            for item, amount in action['Requires'].items():
                amount = 1 if amount else 0
                if maxAmount[item] < amount:
                    maxAmount[item] = amount
        if 'Consumes' in action:
            for item, amount in action['Consumes'].items():
                if maxAmount[item] < amount:
                    maxAmount[item] = amount
    maxAmount = inventory_to_tuple(maxAmount)
    print maxAmount
    def heuristic(state):
        h = 0
        #print zip(state,maxAmount)
        for item1, item2 in zip(state,maxAmount):
            if item1 > item2:
                #print item1, item2
                return 1000000
        return h
    return heuristic

heuristic = make_heuristic()

def search(graph, initial, is_goal, limit, heuristic):
    s_time = time.time()
    start = initial
    queue = [(0, start)]
    parent = {start : None}
    dist = {start : 0}
    #print  limit
    while time.time() - s_time < limit:
        cDist, node = heappop(queue)
        if is_goal(node):
            plan, curr = [], node
            while parent[curr] is not None:
                cost,action, par = parent[curr]
                plan.append((cost,action,curr))
                curr = par
            plan.reverse()
            print 'Search Time: ', (time.time() - s_time), '\n'
            return dist[node], plan
        for adj in graph(node):
            #print neighbor
            action, neighbor, cost = adj
            newDist = dist[node] + cost
            if (neighbor not in dist) or (newDist < dist[neighbor]):
                dist[neighbor] = newDist
                heappush(queue, (newDist+heuristic(neighbor), neighbor))
                parent[neighbor] = (cost,action,node)
    return 0, []

# Container class for holding compiled recipes
Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []
for name, rule in Crafting['Recipes'].items():
    checker = make_checker(rule)
    effector = make_effector(rule)
    recipe = Recipe(name, checker, effector, rule['Time'])
    all_recipes.append(recipe)

def printing(total_cost, states):
    # Prints total cost and cost, action name, and current inventory of each step
    if states:
        for cost, action, state in states:
            p_state = []
            for i, name in enumerate(Crafting['Items']):
                if state[i] != 0:
                    p_state.append((name, state[i]))
            print cost, ',', action, ',', p_state, '\n'
        print 'Total Cost: ', total_cost, 'Length: ', len(states)
    else:
        print 'Did not find solution'

c, s = (search(graph,initial_state,is_goal,200,heuristic))
printing(c, s)








