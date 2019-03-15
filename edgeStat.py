# coding=utf-8

# Check proportion of unassigned reads

import sys

edgeFile = sys.argv[1]
tagFile = sys.argv[2]
readTag = {}


def getTag(value, tags):
    tag = ""
    try:
        tag = tags[value]
    except KeyError:
        tag = "UNASSIGNED"
    finally:
        return(tag)


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

allTag = {}
with open(edgeFile, "r") as f:
    next(f)
    next(f)

    for line in f:
        data = line.rstrip("\n").split("\t")
        origin = data.pop(0)
        allTag[origin] = getTag(origin, readTag)
        newData = []
        for read in data[::2]:
            allTag[read] = getTag(read, readTag)
val = list(allTag.values())
total = len(val)
tagCount = {}
for tag in set(val):
    print(tag, val.count(tag), sep='\t')
