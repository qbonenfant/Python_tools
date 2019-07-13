# coding=utf-8
# Remove sequences containing a N in fasta/fastq files

import sys
import re

sequence_rule = re.compile(r"[ATCGN]+")
form = "fasta"
loop = True

with open(sys.argv[1]) as f:
    acc = ""
    seq = ""
    while loop:
        try:
            line = next(f).rstrip("\n")
            if(line[0] == ">"):
                if(acc and "N" not in seq):
                    print(acc)
                    print(seq)
                acc = line
                seq = ""
            else:
                seq += line
        except StopIteration:
            if(acc and "N" not in seq):
                print(acc)
                print(seq)
            loop = False
