# coding=utf-8
import sys
from collections import defaultdict as dd

# Fetch and return reads for a given number genes

fasta_file = sys.argv[1]
nb_genes = int(sys.argv[2])
genes = dd(list)
def parse_fasta(fasta_file):
    fasta = {}
    seq = ""
    acc = ""
    with open(fasta_file, 'r') as f:
        for l in f:
            l = l.rstrip("\n")
            if(l[0]==">"):
                if(seq!=""):
                    gene = acc.split("_")[-1]
                    genes[gene].append(acc)
                    fasta[acc] = seq
                    seq = ""
                acc = l[1:]
            else:
                seq += l
        fasta[acc] = seq
    return(fasta)

fasta = parse_fasta(fasta_file)
exported = 0
#Don't need to shuffle, the ordering of dictionnary key is already random
for gene in list( genes.keys() ):
    reads = genes[gene]
    if(len(reads) >=10 ):
        exported+=1
        for read in reads:
            print(">"+read+"\n"+fasta[read])
    if(exported == nb_genes):
        break
