from p1_support import load_level, show_level
from heapq import heappush, heappop
import math

class DijkstrasDungeon:
	def __init__(self, filename):
		self.filename = filename
		self.level = load_level(filename)

	def findRoute(self, src, dst):
		path = self.dijkstras_shortest_path(src, dst)

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
		#print "src: ", src_pos, " dst:", dst_pos

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

		if pathSuccess:
			path = [dst_pos]
			check = dst_pos
			while check != src_pos:
				check = parents[check]
				path.append(check)
				#print check
			return path

		else:
			return []

	def getNeighbors(self, node):

		neighbors = []
		for dx in [-1, 0, 1]:
			for dy in [-1, 0, 1]:
				x = node[1][0] + dx
				y = node[1][1] + dy   
				if (x,y) in self.level["spaces"]:

					if (dx*dy) is not 0:
						cost = math.sqrt(2) + node[0]
					else:
						cost =  1 + node[0] 

					neighbors.append((cost, (x,y)))

		return neighbors


if __name__ ==  '__main__':
	import sys
	_, filename, src_waypoint, dst_waypoint = sys.argv
	dd = DijkstrasDungeon(filename)
	dd.findRoute(src_waypoint, dst_waypoint)





  
