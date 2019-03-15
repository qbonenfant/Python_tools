# coding=utf-8

# remove nodes with name  containing "UNASSIGNED"

import sys
import igraph as ig

graphFile = sys.argv[1]
outFile = sys.argv[2]

g = ig.Graph.Read_GraphML(sys.argv[1])
nodes = []
for vertex in g.vs:
    if("UNASSIGNED" in vertex["id"]):
        try:
            nodes.append(vertex)
        except ValueError:
            print("Already deleted " + vertex["id"])

g.delete_vertices(nodes)

g.write_graphml(outFile)
