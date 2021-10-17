# coding=utf-8
# Append tag to read name in tabulated cluster file
import sys


tagFile = sys.argv[1]
inFile = sys.argv[2]
outFile = sys.argv[3]
tag_flag = "G" if len(sys.argv) < 5 else sys.argv[4]


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


def appendTag(value, tags):
    tag = ""
    try:
        tag = tags[value]
    except KeyError:
        tag = "UNASSIGNED"
    finally:
        return(tag)


if(len(sys.argv) > 4):
    tag_flag = sys.argv[4]

readTag = parsg2r(tagFile, tag_flag)

with open(inFile) as f:
    out = open(outFile, "w")
    single_count = 0
    for line in f:
        data = line.rstrip("\n").split("\t")
        buff = []
        for read in data:
            tag = appendTag(read, readTag)
            if(tag == "UNASSIGNED"):
                tag += str(single_count)
                single_count += 1
                # print(read + "_" + tag, file=sys.stderr)
            buff.append(read + "_" + tag)
        if(len(buff) != (0)):
            out.write("\t".join(buff) + "\n")
