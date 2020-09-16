# coding=utf8

import sys
import networkx as nx
from collections import defaultdict as dd
g = nx.DiGraph()

VSPACE = 100
HSPACE = 50
last_pos = dd(list)

with open(sys.argv[1]) as f:
    for i, line in enumerate(f):
        line = line.rstrip("\n")
        data = line.split("\t")
        label1, label2 = data[:2]
        color = data[2].split("=")[1]
        path = data[3].split("=")[1]
        for j, lab in enumerate([label1, label2]):
            g.add_node(lab)
            try:
                rid, pos, tgt = map(int, lab.split("_"))
            except ValueError:
                rid = int(lab.split("_")[0])
                pos = -10
                tgt = rid

            last_pos[rid].append((rid, pos, tgt, lab))
            g.nodes[lab]["read"] = rid

            try:
                _ = g.nodes[lab]["order"]
            except KeyError:
                g.nodes[lab]["order"] = i * 2 + j

        is_cyclic = color == "green"
        g.add_edge(label1, label2, color=color, path=path, cyclic=is_cyclic)


# Placing nodes
for rid in last_pos.keys():
    for i, (rid, pos, tgt, lab) in enumerate(sorted(set(last_pos[rid]))):
        g.nodes[lab]["x"] = .1 * pos * HSPACE +i
        g.nodes[lab]["y"] = rid * VSPACE


nx.write_graphml(g, sys.argv[1] + ".graphml")
