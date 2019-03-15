#coding=utf-8
# create a smaller fasta from a sequence name list and a fasta file

import sys
idList=set()
with open(sys.argv[1]) as listFile:
    for line in listFile:
        idList.add(line.rstrip("\n"))

fasta = {}
with open(sys.argv[2]) as readFile:
    name=""
    oldName=""
    seq=""
    for line in readFile:
        if(line[0] == ">"):
            if(seq!=""):
                if(name in idList):
                    fasta[name]=seq
            name = line.rstrip("\n")[1:]
            seq = ""
        else:
            seq += line.rstrip("\n")
    if(name in idList):
        fasta[name]=seq
for key in fasta:
    print(">" + key)
    print(fasta[key])
