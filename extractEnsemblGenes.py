# coding=utf-8
# create a fasta file from a sequence name list and an ENSEMBL reference transcriptome

import sys
from Bio import SeqIO


list_file = sys.argv[1]
fastFile = sys.argv[2]
extension = fastFile.split(".")[-1]

idList = []
with open(list_file) as f:
    for line in f:
        acc = line.rstrip("\n").split()[0]
        idList.append(acc)

records = SeqIO.parse(fastFile, extension)
for record in records:

    record_dict = {}
    for el in str(record.description).split(" "):
        data = el.split(":")
        if(len(data) == 2 ):
            k,v = data
            record_dict[k] = v
    if(record_dict["gene"] in idList):
        print(record.format(extension), end="")
