# coding=utf-8

import sys
import os
import igraph as ig

edgeFile = sys.argv[1]
outFile = sys.argv[2]

outPath = os.path.dirname(outFile)
filename = os.path.basename(outFile)

g = ig.Graph()
nodes = {}
counter = 0
with open(edgeFile) as f:
    for i, line in enumerate(f):
        # Skipping the first two line of .edge file,
        # they contains informations about the run.
        if(i >= 2):
            print(i)
            data = line.rstrip("\n").split("\t")
            fRead = data[0]
            l1 = int(data[1])
            read = data[2]
            l2 = int(data[3])
            orientation = data[4]
            pos = [tuple(int(a) for a in el.split(",")) for el in data[5:]]
            weight = len(pos)

            for r in [fRead, read]:
                if(r not in nodes):
                    nodes[r] = str(counter)
                    counter += 1
                    g.add_vertex(r)
            g.add_edge( fRead, read, weight = weight, dir = orientation)

g.write_graphml(outFile)