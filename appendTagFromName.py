# coding=utf-8

# Append tag to graph nodes.
# input format is graphml for the graph
# and g2rl for the gene/ read map
# (easier / lighter to store / move around than a bam file and a GTF)
import igraph as ig
import sys


graphFile = sys.argv[1]
outFile = sys.argv[2]

readTag = {}


def appendTag(value):
    
    tag = value.split("_")[-1]
    
    # if("ENSMUS" not in tag):
    #     tag = "UNASSIGNED"
    
    return(tag)


g = ig.Graph.Read_GraphML(graphFile)
single_count = 0
for node in g.vs:
    tag = appendTag(node["id"])

    if(tag == "UNASSIGNED"):
        tag += str(single_count)
        single_count += 1
    node["tag"] = tag
g.write_graphml(outFile)
