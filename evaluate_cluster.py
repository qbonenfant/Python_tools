# coding=utf-8

# Evaluate the quality of a cluster, comparing a graph file (nodes and link) to the "ground truth"
# I use the original fasta to know the name and number of the nodes.


import sys
import networkx as nx
from sklearn.metrics import *

fasta = sys.argv[1]
graph = sys.argv[2]

reads = []
with open(fasta) as fa:
    for line in fa:
        if(line[0] == ">"):
            reads.append(line[1:].rstrip("\n"))


labels_true = []
labels_pred = []
genes = []
g = nx.read_graphml(graph)

# complelting
g_nodes = set(g.nodes)
to_insert = set(reads) - g_nodes
for n in to_insert:
    g.add_node(n, id=n)

print("COMPUTING METRICS...")
nodes_in_cluster = 0
number_of_cluster = 0
for i, sub in enumerate(nx.connected_components(g)):
    cl_size = 0
    for node in sub:
        tag = node.split("_")[-1]
        cl_size += 1
        if(tag not in genes):
            genes.append(tag)

        labels_true.append(genes.index(tag))
        labels_pred.append(i)
    if(cl_size > 1):
        nodes_in_cluster += cl_size
        number_of_cluster += 1

h, c, v = homogeneity_completeness_v_measure(
    labels_true, labels_pred, beta=1.0)
#f = f1_score(labels_true, labels_pred, average='micro')

print("Number of nodes:", len(reads))
print("Number of cluster:", number_of_cluster)
print("Number of nodes in clusters:", nodes_in_cluster)
print("Number of singletons:", len(reads) - nodes_in_cluster)
print("Homogeneity :", h)
print("Completeness:", c)
print("V-measure   :", v)
