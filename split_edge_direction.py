# coding utf-8
# Split an edge file in 2 files
# depending on relative orientation of mapped reads.

import sys


if(len(sys.argv) != 2):
    print("USAGE: split_edge_directon <edge_file>")
    exit()

edge_file = sys.argv[1]

with open(sys.argv[1]) as f:

    forward = edge_file + "_forward"
    reverse = edge_file + "_reverse"
    forward_file = open(forward, "w")
    reverse_file = open(reverse, "w")
    for line in f:
        data = line.split("\t")
        if(len(data) > 2):
            # unused for now
            r1 = data[0]
            l1 = data[1]
            r2 = data[2]
            l2 = data[3]
            # read relative orientation
            ori = data[4]
            # forward case
            if(ori == "0"):
                forward_file.write("\t".join(data))
            elif(ori == "1"):
                reverse_file.write("\t".join(data))
        else:
            forward_file.write(line)
            reverse_file.write(line)
    forward_file.close()
    reverse_file.close
