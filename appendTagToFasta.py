# coding=utf-8

# Append tag to read name in fasta

import igraph as ig
# import networkx as nx
import sys


inFile = sys.argv[1]
tagFile = sys.argv[2]
outFile = sys.argv[3]
tag_flag = "G" if len(sys.argv)<5 else sys.argv[4]

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



if(len(sys.argv) > 4):
    tag_flag = sys.argv[4]

readTag = parsg2r(tagFile, tag_flag)

with open(inFile) as f:
    out = open(outFile, "w")
    single_count = 0
    for line in f:
        line = line.rstrip("\n")
        if(line[0] == ">"):
            tag = appendTag(line[1:], readTag)
            if(tag == "UNASSIGNED"):
                tag += str(single_count)
                single_count += 1
            line += "_" + tag
        out.write(line + "\n")
