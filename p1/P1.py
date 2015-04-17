from p1_support import load_level, show_level
from math import sqrt
from heapq import heappush, heappop

class DijkstrasDungeon:
    def __init__(self, filename):
        self.filename = filename
        self.level = load_level(filename)

    def findRoute(self, src, dst):
        path = self.dijkstra(src, dst)

        if path:
            show_level(self.level, path)
        else:
            print "No path available"

	def dijkstras_shortest_path(self, src, dst):
        path = []
        parents = {}

        src_pos = self.level['waypoints'][src]
        dst_pos = self.level['waypoints'][dst]
        parents[src_pos] = None
        print "src: ", src_pos, " dst:", dst_pos

        queue = [(0,src_pos)]
        pathSuccess = False
        workingPaths = []
		checkedPaths = {}
        checked = {}
        checkedPaths[src_pos] = [src_pos]

		while queue:
            node = heappop(queue)
            if node[1] == dst_pos:
                pathSuccess = True
                print "Reached the goal!"
                break

            for neighbor in self.getNeighbors(node):
                if neighbor[1] not in parents:
                    heappush(queue, neighbor)
                    parents[neighbor[1]] = node[1]
                    checkedPaths[neighbor[1]] = list(checkedPaths[node[1]])
                    checkedPaths[neighbor[1]].append(neighbor[1])

            checked[node[1]] = 1  

if __name__ ==  '__main__':
	import sys
	_, filename, src_waypoint, dst_waypoint = sys.argv
	test_route(filename, src_waypoint, dst_waypoint)





  
