# coding=utf-8
# Remove sequences containing a N in fasta/fastq files

import sys
import re

sequence_rule = re.compile(r"[ATCGN]+")
form = "fasta"
loop = True

with open(sys.argv[1]) as f:
    qual = ""
    while loop:
        try:
            line = next(f).rstrip("\n")
            if(line[0] == "@"):
                form = "fastq"
            seq = next(f)

            if("N" not in seq):
                # if fastq,keeping quality score
                if(form == "fastq"):
                    qual += next(f)
                    qual += next(f)
                print(line)
                print(seq.rstrip("\n"))
                if(qual):
                    print(qual.rstrip("\n"))
                qual = ""
        except StopIteration:
            loop = False
