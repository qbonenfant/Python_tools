# coding=utf-8

# Split an edge file in different communities based on a clustering.

import sys
import os
from collections import defaultdict as dd

edgeFileName = sys.argv[1]
clusterFile = sys.argv[2]
cluster_path = sys.argv[3] if len(sys.argv) >= 4 else "./tmp"

# Creating path to output clusters edge file
buff = ""
for element in os.path.split(cluster_path):
    buff = os.path.join(buff, element)
    if(not os.path.isdir(buff)):
        os.mkdir(buff)


edges = dd(dict)

with open(edgeFileName, "r") as f:
    for line in f:
        data = line.rstrip("\n").split("\t")
        if(len(data) > 2):
            r1 = data[0]
            r2 = data[2]

            # Filling edge dictionnary
            edges[r1][r2] = data

# making a set out of edge keys / sources
key_set = set(edges.keys())

with open(clusterFile) as f:
        # each line is a cluster, line number is cluster number
    for cl_nb, line in enumerate(f):
        nodes = line.rstrip("\n").split("\t")
        # concerting nodes in a cluster set
        cluster = set(nodes)
        out = open(os.path.join(cluster_path, "cluster_" + str(cl_nb) + ".edges") , 'w')
        # starting by source node, find edges between elements in the cluster
        for source in cluster & key_set:
            for target in edges[source].keys():
                if(target in nodes):
                    out.write("\t".join(edges[source][target]))
                    out.write("\n")
        out.close()