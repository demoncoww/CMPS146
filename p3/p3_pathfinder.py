

def find_path(source_point, destination_point, mesh):
    visited_boxes = []
    path = []
    box_fringe = []
    src = source_point
    dst = destination_point
    found_src = False
    found_dst = False
    parent = {}
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
                    path.append(pathBox)
                    pathBox = parent[pathBox]
                    if pathBox is srcBox:
                        path.reverse()
                        return path, visited_boxes
    print "No path found!"

class boxnode:
    def __init__(self,  box = None, parent = None):
        self.box = box
        self.parent = parent