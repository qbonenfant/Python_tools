# coding=utf-8
import sys
from collections import defaultdict as dd
# Fetch and return a number of 
g2r_file = sys.argv[1]
nb_seq = int(sys.argv[2])

def parsg2r(g2rFile):
    gene_read= dd(list)
    with open(g2rFile, 'r') as g2rf:
        currentGene = ""
        for line in g2rf:
            if(line[0] == "G"):
                currentGene = line.split("\t")[1].rstrip("\n")
            elif(line[0] == "R"):
                read = line.split("\t")[1].rstrip("\n")
                gene_read[currentGene].append(read)
    return(gene_read)

g2r = parsg2r(g2r_file)
#Don't need to shuffle, the ordering of dictionnary key is already random
seq_index = list(g2r.keys())[:nb_seq]

for acc in seq_index:
    for read in g2r[acc]:
        print(read)


