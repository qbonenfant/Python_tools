# coding=utf-8
# Convert the results from Louvain implementation to a ....

import sys
from collections import defaultdict as dd
eq_listfile = sys.argv[1]
affiliation_file = sys.argv[2]

nodes = {}
clustering = dd(list)
# Parsing equivalence list
with open(eq_listfile) as eq_file:
    for line in eq_file:
        read, index = line.rstrip("\n").split()
        nodes[index] = read

# Parsing affiliation list
with open(affiliation_file) as affiliation:
    for line in affiliation:
        index, community = line.rstrip("\n").split()
        clustering[community].append(index)

for community, elements in clustering.items():
    print("G\t"+community)
    for read_id in elements:
        print("R\t" + nodes[read_id])