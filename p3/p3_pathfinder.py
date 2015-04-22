import math
import heapq
from heapq import heappush, heappop

def find_path(src, dst, mesh):
    visited_boxes = []
    fwd_distances = {}
    bck_distances = {}
    path = []
    box_fringe = []
    fwd_parent = {}
    bck_parent = {}
    detail_points = {} #holds the endpoint of a segment going through that box
    found_src = False
    found_dst = False
    srcBox = (0,0,0,0)
    dstBox = (0,0,0,0)

    for box in mesh['boxes']:
        if src[0] in range (box[0], box[1]) and src[1] in range (box[2], box[3]):
            print "Src Box is", box, " and Source is ", src
            found_src = True
            heappush(box_fringe, (0, box, 'dst'))
            fwd_distances[box] = 0
            visited_boxes.append(box)
            srcBox = box
            detail_points[box] = src
        if dst[0] in range (box[0], box[1]) and dst[1] in range (box[2], box[3]):
            print "Dst Box is", box, " and Destination is ", dst
            found_dst = True
            heappush(box_fringe, (0, box, 'src'))
            bck_distances[box] = 0
            visited_boxes.append(box)
            dstBox = box
            detail_points[box] = dst
        if found_dst and found_src:
            break
    if not found_src:
        print "Source point not on graph."
        return path, visited_boxes
    if not found_dst:
        print "Destination point not on graph."
        return path, visited_boxes
    #print visited_boxes
    
    if srcBox == dstBox:
        path.append((src, dst))
        return path, visited_boxes
    
    while (box_fringe): #pop the first item on the fringe
        priority, popped_box, popped_goal = heappop(box_fringe)
        children = mesh['adj'][popped_box]
        for child in children:
            if popped_goal is 'dst' and child not in fwd_distances:
                visited_boxes.append(child)
                x1 = (popped_box[2] + popped_box[3])/2
                y1 = (popped_box[0] + popped_box[1])/2
                x2 = (child[2] + child[3])/2
                y2 = (child[0] + child[1])/2
                fwd_distances[child] = fwd_distances[popped_box] + euclidDist(x1, y1, x2, y2)
                score = fwd_distances[child] + euclidBoxHeuristic(child, dstBox)
                heappush(box_fringe, (score, child, 'dst'))
                fwd_parent[child] = popped_box
            if popped_goal is 'src' and child not in bck_distances:
                visited_boxes.append(child)
                x1 = (popped_box[2] + popped_box[3])/2
                y1 = (popped_box[0] + popped_box[1])/2
                x2 = (child[2] + child[3])/2
                y2 = (child[0] + child[1])/2
                bck_distances[child] = bck_distances[popped_box] + euclidDist(x1, y1, x2, y2)
                score = bck_distances[child] + euclidBoxHeuristic(child, srcBox)
                heappush(box_fringe, (score, child, 'src'))
                bck_parent[child] = popped_box
            if ((popped_goal is 'dst' and child in bck_distances) or (popped_goal is 'src' and child in fwd_distances)):
                currBox = child
                prevBox = currBox
                nextBox = currBox
                if nextBox is not srcBox:
                    nextBox = fwd_parent[currBox]
                    segment = buildSegment((((child[0]+child[1])/2),((child[2]+child[3])/2)), currBox, nextBox) #build from destination through curr to next
                    path.append(segment)
                    detail_points[currBox] = segment[1]
                    prevBox = currBox
                    currBox = nextBox
                if nextBox is not srcBox:
                    nextBox = fwd_parent[nextBox]
                while (nextBox is not srcBox):
                    this_segment = buildSegment(detail_points[prevBox], currBox, nextBox)
                    path.append(this_segment)
                    detail_points[currBox] = this_segment[1]
                    prevBox = currBox
                    currBox = nextBox
                    nextBox = fwd_parent[nextBox]
                last_segment = buildSegment(detail_points[prevBox], currBox, nextBox)
                path.append(last_segment)
                detail_points[currBox] = last_segment[1]
                path.append((detail_points[currBox], src))
                #print path

                currBox = child
                prevBox = currBox
                nextBox = currBox
                if nextBox is not dstBox:
                    nextBox = bck_parent[currBox]
                    x = (child[2]+child[3])/2
                    y = (child[0]+child[1])/2
                    segment = buildSegment((y, x), currBox, nextBox) #build from destination through curr to next
                    path.append(segment)
                    detail_points[currBox] = segment[1]
                    prevBox = currBox
                    currBox = nextBox
                if nextBox is not dstBox:
                    nextBox = bck_parent[nextBox]
                while (nextBox is not dstBox):
                    this_segment = buildSegment(detail_points[prevBox], currBox, nextBox)
                    path.append(this_segment)
                    detail_points[currBox] = this_segment[1]
                    prevBox = currBox
                    currBox = nextBox
                    nextBox = bck_parent[nextBox]
                last_segment = buildSegment(detail_points[prevBox], currBox, nextBox)
                path.append(last_segment)
                detail_points[currBox] = last_segment[1]
                path.append((detail_points[currBox], dst))
                #print path
                return path, visited_boxes
    print "No path found!"
    return (path, visited_boxes)


def buildSegment(pt, currBox, nextBox):
    nextPt = pt
    if(currBox[2] == nextBox[3]): #sharing currBox left edge
        xPt = currBox[2]
        yMax = min(currBox[1], nextBox[1])
        yMin = max(currBox[0], nextBox[0])
        prevDist = 100000000.0
        currDist = prevDist - 1
        yPt = yMin
        while(prevDist > currDist and yPt <= yMax):
            prevDist = currDist
            currDist = euclidDist(pt[1], pt[0], xPt, yPt)
            yPt+=1
        nextPt = (yPt - 1, xPt)
    if(currBox[3] == nextBox[2]): #sharing currBox right edge
        xPt = currBox[3]
        yMax = min(currBox[1], nextBox[1])
        yMin = max(currBox[0], nextBox[0])
        prevDist = 100000000.0
        currDist = prevDist - 1
        yPt = yMin
        while(prevDist > currDist and yPt <= yMax):
            prevDist = currDist
            currDist = euclidDist(pt[1], pt[0], xPt, yPt)
            yPt+=1
        nextPt = (yPt - 1, xPt)
    if(currBox[0] == nextBox[1]): #sharing currBox top edge
        yPt = currBox[0]
        xMax = min(currBox[3], nextBox[3])
        xMin = max(currBox[2], nextBox[2])
        prevDist = 100000000.0
        currDist = prevDist - 1
        xPt = xMin
        while(prevDist > currDist and xPt <= xMax):
            prevDist = currDist
            currDist = euclidDist(pt[1], pt[0], xPt, yPt)
            xPt+=1
        nextPt = (yPt, xPt - 1)
    if(currBox[1] == nextBox[0]): #sharing currBox bottom edge
        yPt = currBox[1]
        xMax = min(currBox[3], nextBox[3])
        xMin = max(currBox[2], nextBox[2])
        prevDist = 100000000.0
        currDist = prevDist - 1
        xPt = xMin
        while(prevDist > currDist and xPt <= xMax):
            prevDist = currDist
            currDist = euclidDist(pt[1], pt[0], xPt, yPt)
            xPt+=1
        nextPt = (yPt, xPt - 1)
    return pt, nextPt

def euclidDist(x1, y1, x2, y2):
    x = ((x1-x2)**2)
    y = ((y1-y2)**2)
    return math.sqrt(x+y)

class boxnode:
    def __init__(self,  box = None, parent = None):
        self.box = box
        self.parent = parent
        
def euclidBoxHeuristic (myBox, dstBox):
    x1 = (myBox[2] + myBox[3])/2
    y1 = (myBox[0] + myBox[1])/2
    x2 = (dstBox[2] + dstBox[3])/2
    y2 = (dstBox[0] + dstBox[1])/2
    return euclidDist(x1, y1, x2, y2)