

def find_path(source_point, destination_point, mesh):
    visited_boxes = []
    path = []
    src = source_point
    dst = destination_point
    found_src = False
    found_dst = False

    for box in mesh['boxes']:
        if src[0] in range (box[0], box[1]) and src[1] in range (box[2], box[3]):
            print "Src Box is", box, " and Source is ", src
            found_src = True
            visited_boxes.append(box)
        if dst[0] in range (box[0], box[1]) and dst[1] in range (box[2], box[3]):
            print "Dst Box is", box, " and Destination is ", dst
            found_dst = True
            visited_boxes.append(box)
        if found_dst and found_src:
            break

    print visited_boxes
    return path, visited_boxes