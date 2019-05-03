# coding=utf-8

# Convert edge files into MCL abs graph format.

import sys
with open(sys.argv[1]) as edgeFile:

    for line in edgeFile:
        data = line.rstrip("\n").split("\t")
        main_node = data.pop(0)
        [print(" ".join([main_node, data[i], data[i + 1]])) for i in range(0, len(data), 2)]
