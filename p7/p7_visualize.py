import subprocess
import json
import collections
import random
import sys

def parse_json_result(out):
    """Parse the provided JSON text and extract a dict
    representing the predicates described in the first solver result."""

    result = json.loads(out)
    
    assert len(result['Call']) > 0
    assert len(result['Call'][0]['Witnesses']) > 0
    
    witness = result['Call'][0]['Witnesses'][0]['Value']
    
    class identitydefaultdict(collections.defaultdict):
        def __missing__(self, key):
            return key
    
    preds = collections.defaultdict(set)
    env = identitydefaultdict()
    
    for atom in witness:
        if '(' in atom:
            left = atom.index('(')
            functor = atom[:left]
            arg_string = atom[left:]
            try:
                preds[functor].add( eval(arg_string, env) )
            except TypeError:
                pass # at least we tried...
            
        else:
            preds[atom] = True
    
    return dict(preds)

def solve_randomly(*args):
    """Like solve() but uses a random sign heuristic with a random seed."""
    args = list(args) + ["--sign-def=3","--seed="+str(random.randint(0,1<<30))]
    return solve(*args) 

def render_ascii_dungeon(design):
    """Given a dict of predicates, return an ASCII-art depiction of the a dungeon."""
    
    sprite = dict(design['sprite'])
    param = dict(design['param'])
    width = param['width']
    glyph = dict(space='.', wall='W', altar='a', gem='g', trap='_')
    block = ''.join([''.join([glyph[sprite.get((r,c),'space')]+' ' for c in range(width)])+'\n' for r in range(width)])
    return block

def render_ascii_touch(design, target):
    """Given a dict of predicates, return an ASCII-art depiction where the player explored
    while in the `target` state."""
    
    touch = collections.defaultdict(lambda: '-')
    for cell, state in design['touch']:
        if state == target:
            touch[cell] = str(target)
    param = dict(design['param'])
    width = param['width']
    block = ''.join([''.join([str(touch[r,c])+' ' for c in range(width)])+'\n' for r in range(width)])
    return block

def side_by_side(*blocks):
    """Horizontally merge two ASCII-art pictures."""
    
    lines = []
    for tup in zip(*map(lambda b: b.split('\n'), blocks)):
        lines.append(' '.join(tup))
    return '\n'.join(lines)

def visualize(filename): 
  jsonData = open(filename, 'r').read()
  design = parse_json_result(jsonData)
  print render_ascii_dungeon(design)

if len(sys.argv) > 1:
    prog, filename = sys.argv
    visualize(filename)
else:
    print "p7_visualize.py requires a json filename argument to read from"