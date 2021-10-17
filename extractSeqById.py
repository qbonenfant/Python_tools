# coding=utf-8
# create a smaller fasta from a sequence name list and a fasta file

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
    if(record.id in idList):
        print(record.format(extension), end="")
