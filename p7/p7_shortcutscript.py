from subprocess import Popen
from subprocess import PIPE

p1 = Popen(["gringo", "level-core.lp", "level-style.lp", "level-sim.lp", "level-shortcuts.lp"], stdout=PIPE)
p2 = Popen(["reify"], stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()
p3 = Popen(["clingo", "-", "meta.lp", "metaD.lp", "metaO.lp", "metaS.lp", "--parallel-mode=4", "--outf=2"], stdin=p2.stdout, stdout=PIPE)
p2.stdout.close()
output = p3.communicate()[0]
print ""
print "output:"
print ""
print output
open("example_noshortcut.json", "w").write(output)