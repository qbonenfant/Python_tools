# coding=utf-8
# Parse an ENSEMBL fasta file and collects some of the metadata

import sys
from collections import defaultdict as dd

def parse_ensembl_fasta(fasta_file):
    fasta = {}
    with open(fasta_file) as f:
        current_element = {}
        sequence = ""
        for line in f:
            if(line[0] == ">"):
                current_element["sequence"] = sequence
                sequence = ""
                data = line[1:].rstrip("\n").split()
                fasta[data[0]] = {}
                current_element = fasta[data[0]]
                # data[7] = " ".join(data[7:])

                for element in data[2:7]:
                    sub_elements = element.split(":")
                    current_element[sub_elements[0]] = ":".join(
                        sub_elements[1:])

            else:
                sequence += line.rstrip("\n")
        current_element["sequence"] = sequence
    return(fasta)


fasta = parse_ensembl_fasta(sys.argv[1])


#counting the number of transcripts per genes
genes = dd(int)
for acc, data in fasta.items():
    genes[data["gene"]] += 1

# fecthing the "best" ones
best_genes = sorted(genes.keys(), reverse= True, key=lambda x: genes[x])[:20]

# Going through the sequences, and exporting the transcripts belonging to the "best" genes
for acc, data in fasta.items():
    if(data["gene"] in best_genes ):
        print(">" + acc + "_" + data["gene"] )
        print(data["sequence"])
