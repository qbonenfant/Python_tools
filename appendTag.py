# coding=utf-8

# Append tag to read name
# input format is graphml for the graph
# and g2rl for the gene/ read map
import igraph as ig
import sys


graphFile = sys.argv[1]
tagFile = sys.argv[2]
outFile = sys.argv[3]

readTag = {}


def appendTag(value, tags):
    tag = ""
    try:
        tag = "_" + tags[value]
    except KeyError:
        tag = "_UNASSIGNED"
    finally:
        return(value + tag)


def parsg2r(g2rFile):
    readTag = {}
    with open(g2rFile, 'r') as g2rf:
        currentGene = ""
        for line in g2rf:
            if(line[0] == "G"):
                currentGene = line.split("\t")[1].rstrip("\n")
            elif(line[0] == "R"):
                read = line.split("\t")[1].rstrip("\n")
                readTag[read] = currentGene
    return(readTag)


with open(tagFile, "r") as f:
    readTag = parsg2r(tagFile)

g = ig.Graph.Read_GraphML(graphFile)

for node in g.vs:
    name = appendTag(node["id"], readTag)
    node["id"] = name

g.write_graphml(outFile)
