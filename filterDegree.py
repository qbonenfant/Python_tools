# coding=utf-8

import igraph as ig
import sys

deg_limit = int(sys.argv[2])
outFile = sys.argv[3]
g = ig.Graph.Read_GraphML(sys.argv[1])
g.delete_vertices(g.vs.select(_degree_lt=deg_limit))
g.write_graphml(outFile)
