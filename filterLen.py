# coding=utf-8
# Remove sequences which are shorter than specified lenght

import sys
import re

form = "fasta"
loop = True

with open(sys.argv[1]) as f:
    seq = ""
    while loop:

        try:
            line = next(f).rstrip("\n")
            if(line[0] == "@"):
                form = "fastq"
                acc = line
                seq = ""
            elif(line[0] == ">"):
                form = "fasta"
                acc = line
                seq = ""
            seq += next(f).rstrip("\n")
            if(len(seq) > sys.argv[2]):
                print(acc)
                print(seq)
                # if fastq,keeping quality score
                if(form == "fastq"):
                    print(next(f))
                    print(next(f))
        except StopIteration:
            loop = False
