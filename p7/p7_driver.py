from subprocess import Popen
from subprocess import PIPE
import p7_shortcutscript
import p7_visualize

tempFile = "driverTemp.json"

p7_shortcutscript.createMap(tempFile)
print "Map created"
p7_visualize.visualize(tempFile)