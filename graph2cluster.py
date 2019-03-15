# coding=utf-8

import igraph as ig
import sys

g = ig.Graph.Read_GraphML(sys.argv[1])
vc = g.components()
for sg in vc.subgraphs():
    print("\t".join(node["id"] for node in sg.vs))
