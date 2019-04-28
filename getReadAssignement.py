# coding=utf-8

# Search read if in G2R file and print a TSV output containing gene and transcript associated to this read
# input format plain text for the list of reads, one read id per line,
# and g2rl for the gene/ read map
# (easier / lighter to store / move around than a bam file and a GTF)
import igraph as ig
import sys


listFile = sys.argv[1]
g2rFile = sys.argv[2]

readList = []


def parsg2r(g2rFile):
    readTag = {}
    with open(g2rFile, 'r') as g2rf:
        currentGene = ""
        currentTrans = ""
        for line in g2rf:
            value = line.split("\t")[1].rstrip("\n")
            if(line[0] == "G"):
                currentGene = value
            elif(line[0] == "T"):
                currentTrans = value
            elif(line[0] == "R"):
                read = value
                if(read in readList):
                    print(read, currentTrans, currentGene, sep = "\t")
                    readList.pop(readList.index(read))
                readTag[read] = currentGene
    return(readTag)


with open(listFile, "r") as f:
    readSet = set()  # used to avoid redundant read names.
    for line in f:
        readSet.add(line.rstrip("\n"))
    readList = list(readSet)

parsg2r(g2rFile)
if(len(readList) != 0 ):
    for elem in readList:
        print(elem, "UNASSIGNED", "UNASSIGNED", sep = "\t")
