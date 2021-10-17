# coding=utf-8
import sys


def parse_fasta(fasta_file):
    fasta = {}
    seq = ""
    acc = ""
    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.rstrip("\n")
            if(line[0] == ">"):
                if(seq != ""):
                    fasta[acc] = seq
                    seq = ""
                acc = line[1:]
            else:
                seq += line
        fasta[acc] = seq
    return(fasta)


fasta = parse_fasta(sys.argv[1])

for acc in sorted(fasta.keys(), reverse=True, key=lambda x: len(fasta[x])):
    print(">" + acc)
    print(fasta[acc])
