# coding=utf-8

# Append tag to graph nodes.
# input format is graphml for the graph
# and g2rl for the gene/ read map
# (easier / lighter to store / move around than a bam file and a GTF)
import igraph as ig
# import networkx as nx
import sys


graphFile = sys.argv[1]
tagFile = sys.argv[2]
outFile = sys.argv[3]

readTag = {}


def appendTag(value, tags):
    tag = ""
    try:
        tag = tags[value]
    except KeyError:
        tag = "UNASSIGNED"
    finally:
        return(tag)


def parsg2r(g2rFile, tag_flag):
    readTag = {}
    with open(g2rFile, 'r') as g2rf:
        currentGene = ""
        for line in g2rf:
            if(line[0] == tag_flag):
                currentGene = line.split("\t")[1].rstrip("\n")
            elif(line[0] == "R"):
                read = line.split("\t")[1].rstrip("\n")
                readTag[read] = currentGene
    return(readTag)


tag_flag = "G"
if(len(sys.argv) >4 ):
    tag_flag = sys.argv[4]

readTag = parsg2r(tagFile, tag_flag)

g = ig.Graph.Read_GraphML(graphFile)
# g = nx.read_graphml(graphFile)
single_count = 0
for node in g.vs:
    # for node in g.nodes:
    tag = appendTag(node["id"], readTag)
    #tag = appendTag(g.node[node]["id"], readTag)

    if(tag == "UNASSIGNED"):
        tag += str(single_count)
        single_count += 1
    node["tag"] = tag
g.write_graphml(outFile)
#nx.write_graphml(g, outFile)
