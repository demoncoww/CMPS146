import json
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

# Container class for holding compiled recipes
Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []
for name, rule in Crafting['Recipes'].items:
	checker = make_checker(rule)
	effector = make_effector(rule)
	recipe = Recipe(name, checker, effector, rule['Time'])
	all_recipes.append(recipe)


def make_checker(rule):
    # TODO: Add code here
	# this code runs once
	# do something with rule['Consumes'] and rule['Requires']
	def check(state):
        # TODO: Add code here
		# this code runs millions of times
		return True # or False

	return check

def make_effector(rule):
    # TODO: Add code here
    # this code runs once
    # do something with rule['Produces'] and rule['Consumes']
	def effect(state):
        # TODO: Add code here
		# this code runs millions of times
        return state
		#return next_state

	return check
