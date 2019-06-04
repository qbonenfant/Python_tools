# coding=utf-8
# create a smaller fasta from a sequence name list and a fasta file

import sys
idList = {}
with open(sys.argv[1]) as listFile:
    for line in listFile:
        data = line.rstrip("\n").split()
        acc = data[0]
        elems = "_" + "_".join(data[1:]) if len(data) > 1 else ""
        elems = elems.rstrip("_")
        idList[acc] = elems

fasta = {}
with open(sys.argv[2]) as readFile:
    name = ""
    oldName = ""
    seq = ""
    for line in readFile:
        if(line[0] == ">"):
            if(seq != ""):
                # Checking if read is NOT in list
                if(name not in idList):
                    fasta[name] = seq
            name = line.rstrip("\n")[1:]
            seq = ""
        else:
            seq += line.rstrip("\n")
    if(name not in idList):
        fasta[name] = seq
for key in fasta:
    print(">" + key)
    print(fasta[key])
