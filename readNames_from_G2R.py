# coding=utf-8

# fetch the list of reads belonging to a gene using a G2R file

import sys

gene_name = sys.argv[2]
with open(sys.argv[1]) as f:
    gene_found = False
    for line in f:

        if(line[0] == "G"):
            if(line.split("\t")[1].rstrip("\n") == gene_name):
                gene_found = True
            else:
                gene_found = False
        elif(gene_found and line[0] == "R"):
            print(line.split("\t")[1].rstrip("\n"))
