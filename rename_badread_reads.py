# coding=utf-8

import sys


def rename_badreads(fasta_file):
    with open(fasta_file) as f:
        for line in f:
            line = line.rstrip("\n")
            if(line[0] == ">"):
                data = line.split(",")
                new_name = data[0].replace(" ", "_")
                print(new_name)
            else:
                print(line)


fasta_file = sys.argv[1]

rename_badreads(fasta_file)
