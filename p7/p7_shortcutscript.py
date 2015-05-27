from subprocess import Popen
from subprocess import PIPE
import sys

def createMap (filename):
    p1 = Popen(["gringo", "level-core.lp", "level-style.lp", "level-sim.lp", "level-shortcuts.lp", "-c", "width=7"], stdout=PIPE)
    p2 = Popen(["reify"], stdin=p1.stdout, stdout=PIPE)
    p1.stdout.close()
    p3 = Popen(["clingo", "-", "meta.lp", "metaD.lp", "metaO.lp", "metaS.lp", "--parallel-mode=6", "--outf=2"], stdin=p2.stdout, stdout=PIPE)
    p2.stdout.close()
    output = p3.communicate()[0]
    open(filename, "w+").write(output)
    return 0

filename = "p7_shortcutscript_temp.json"
if len(sys.argv) > 1:
    prog, filename = sys.argv
createMap(filename)