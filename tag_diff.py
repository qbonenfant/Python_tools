# coding=utf-8

import sys
import os
# Report the difference between 2 G2R files.


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


file1 = sys.argv[1]
file2 = sys.argv[2]

tag1 = parsg2r(file1)
tag2 = parsg2r(file2)

all_reads = set(tag1.keys()) | set(tag2.keys())
f1missing = 0
f2missing = 0
mismatch = 0
for read in all_reads:

    try:
        if(tag1[read] != tag2[read]):
            print("DIFF:", read, tag1[read], tag2[read], sep="\t")
            mismatch += 1

    except KeyError:
        # finding exception origin
        if(read not in tag1.keys()):
            #print("READ", read, "not in file", os.path.basename(file1), sep="\t")
            f1missing += 1
        elif(read not in tag2.keys()):
            #print("READ", read, "not in file", os.path.basename(file2), sep="\t")
            f2missing += 1
print("Mismatch:", mismatch, sep="\t")
print("Missing in file 1:", f1missing, sep="\t")
print("Missing in file 2:", f2missing, sep="\t")
