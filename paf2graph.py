########################################################################
# Convert a paf file to a graphml file in the most dirty way possible.
# It's ugly, but this script works on BIG datasets.
# It will generate two temp files.
# Since RM command a used to remove them, do not use this
# script with high level perm, to avoid potential accidental deletions.
########################################################################
# coding=utf-8

import sys
import networkx as nx 

pafFile = sys.argv[1]
outFile = sys.argv[2]

g = nx.Graph()
print("PARSING PAF FILE")
with open(pafFile) as f:
  for line in f:
    data = line.rstrip("\n").split("\t")
    read1 = data[0]
    read2 = data[5]
    if(read1 != read2):
        g.add_edge(read1,read2)
print("Exporting graph")
nx.write_graphml(g,outFile)
