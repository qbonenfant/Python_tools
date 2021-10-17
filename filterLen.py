# coding=utf-8
# Remove sequences which are shorter than specified lenght

import sys

form = "fasta"
loop = True

lower_bound = int(sys.argv[2])
upper_bound = int(sys.argv[3]) if len(sys.argv) > 3 else -1

with open(sys.argv[1]) as f:
    seq = ""
    acc = ""
    for line in f:
        line = line.rstrip("\n")
        if(line[0] == ">"):
            ls = len(seq)
            if(seq != "" and ls >= lower_bound):
                if(upper_bound < 0 or ls <= upper_bound):
                    print(acc)
                    print(seq)
            acc = line
            seq = ""
        else:
            seq += line

    if(len(seq) > int(sys.argv[2])):
        print(acc)
        print(seq)
