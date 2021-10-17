# coding=utf-8
# Convert edge files into simple abc graph format.
# format: node1 node2 [weight]

import sys


if(len(sys.argv) < 1):
    print("Please, supply an edge file.")
    exit()

edge_filename = sys.argv[1]
graph_name = ".".join(edge_filename.split(".")[:-1]) + ".abc"
eq_list = ".".join(edge_filename.split(".")[:-1]) + ".eq_list"

nodes = set()
edges = []
# Parsing edgefile
with open(edge_filename) as edgeFile:
    for i, line in enumerate(edgeFile):
        if(i >= 2):
            data = line.rstrip("\n").split("\t")
            nodes.add(data[0])
            nodes.add(data[2])
            weight = len(data[6:])
            edges.append((data[0], data[2], weight))

# converting node set to indexable node list
node_list = sorted(list(nodes))

# exporting equivalence list
with open(eq_list, "w") as eq_out:
    for i, node in enumerate(node_list):
        eq_out.write(node + " " + str(i) + "\n")

# exporting graph in abc format
with open(graph_name, "w") as graph:
    for edge in edges:
        n1 = node_list.index(edge[0])
        n2 = node_list.index(edge[1])
        w = edge[2]
        graph.write(" ".join(str(el) for el in [n1, n2, w]))
        graph.write("\n")
