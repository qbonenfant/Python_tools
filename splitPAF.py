# coding=utf-8

# Split a PAF file in different communities based on a clustering.

import sys
import os
from collections import defaultdict as dd

pafFileName = sys.argv[1]
clusterFile = sys.argv[2]
cluster_path = sys.argv[3] if len(sys.argv) >= 4 else "./tmp"

# Creating path to output clusters edge file
buff = ""
for element in os.path.split(cluster_path):
    buff = os.path.join(buff, element)
    if(not os.path.isdir(buff)):
        os.mkdir(buff)


paf = dd(dict)

with open(pafFileName, "r") as f:
    for line in f:
        data = line.rstrip("\n").split()
        # print(data)
        if(len(data) > 2):
            r1 = data[0]
            r2 = data[5]

            # Filling edge dictionnary
            paf[r1][r2] = data

# making a set out of edge keys / sources
key_set = set(paf.keys())

with open(clusterFile) as f:
    # each line is a cluster, line number is cluster number
    for cl_nb, line in enumerate(f):
        nodes = line.rstrip("\n").split("\t")
        # concerting nodes in a cluster set
        cluster = set(nodes)
        out = open(os.path.join(
            cluster_path, "cluster_" + str(cl_nb) + ".paf"), 'w')
        # starting by source node, find edges between elements in the cluster
        for source in cluster & key_set:
            for target in paf[source].keys():
                if(target in nodes):
                    out.write("\t".join(paf[source][target]))
                    out.write("\n")
        out.close()
