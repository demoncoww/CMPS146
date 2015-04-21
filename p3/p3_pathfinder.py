import math

def find_path(source_point, destination_point, mesh):
    visited_boxes = []
    path = []
    box_fringe = []
    parent = {}
    detail_points = {} #holds the endpoint of a segment going through that box
    src = source_point
    dst = destination_point
    found_src = False
    found_dst = False
    srcBox = (0,0,0,0)
    dstBox = (0,0,0,0)

    for box in mesh['boxes']:
        if src[0] in range (box[0], box[1]) and src[1] in range (box[2], box[3]):
            print "Src Box is", box, " and Source is ", src
            found_src = True
            box_fringe.append(box)
            visited_boxes.append(box)
            srcBox = box
        if dst[0] in range (box[0], box[1]) and dst[1] in range (box[2], box[3]):
            print "Dst Box is", box, " and Destination is ", dst
            found_dst = True
            dstBox = box
            detail_points[dstBox] = dst
        if found_dst and found_src:
            break

    #print visited_boxes
    while (box_fringe): #pop the first item on the fringe
        curr_box = box_fringe.pop(0)
        children = mesh['adj'][curr_box]
        for child in children:
            if child not in visited_boxes:
                visited_boxes.append(child)
                box_fringe.append(child)
                parent[child] = curr_box
            if child is dstBox:
                pathBox = child
                while parent[pathBox]:
                    print pathBox
                    pathBox = parent[pathBox]
                    if pathBox is srcBox: #build usable path
                        currBox = dstBox
                        nextBox = parent[currBox]
                        segment = buildSegment(dst, currBox, nextBox) #build from destination through curr to next
                        path.append(segment)
                        detail_points[currBox] = segment[1]
                        prevBox = currBox
                        currBox = nextBox
                        nextBox = parent[nextBox]
                        while (nextBox is not srcBox):
                            this_segment = buildSegment(detail_points[prevBox], currBox, nextBox)
                            path.append(this_segment)
                            detail_points[currBox] = this_segment[1]
                            prevBox = currBox
                            currBox = nextBox
                            nextBox = parent[nextBox]
                        last_segment = buildSegment(detail_points[prevBox], currBox, nextBox)
                        path.append(last_segment)
                        detail_points[currBox] = last_segment[1]
                        path.append((detail_points[currBox], src))
                        print path
                        return path, visited_boxes
    print "No path found!"


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
    z = x+y
    return math.sqrt(z)

class boxnode:
    def __init__(self,  box = None, parent = None):
        self.box = box
        self.parent = parent