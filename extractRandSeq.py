# coding=utf-8
import sys
import random
# Fetch and return a number of 
fasta_file = sys.argv[1]
nb_seq = int(sys.argv[2])
outfile = sys.argv[3]
nb_file = int(sys.argv[4]) if len(sys.argv)>4 else 1



def parse_fasta(fasta_file):
    fasta = {}
    seq = ""
    acc = ""
    with open(fasta_file, 'r') as f:
        for l in f:
            l = l.rstrip("\n")
            if(l[0]==">"):
                if(seq!=""):
                    fasta[acc] = seq
                    seq = ""
                acc = l[1:]
            else:
                seq += l
        fasta[acc] = seq
    return(fasta)

fasta = parse_fasta(fasta_file)
seq_index = list(fasta.keys())
for i in range(nb_file):

    out = open(outfile + "_" + str(i+1) + ".fasta",'w')
    # shuffling
    random.shuffle(seq_index)
    for acc in seq_index[:nb_seq]:
        print(">"+acc+"\n"+fasta[acc], file = out)
    out.close()