# coding=utf-8

import igraph as ig
import sys

nk_limit = int(sys.argv[2])
outFile = sys.argv[3]
g = ig.Graph.Read_GraphML(sys.argv[1])
print("Previous node count:", g.vcount())
g.delete_edges(g.es.select(nk_lt=nk_limit))
print("New node count:", g.vcount())
g.write_graphml(outFile)
