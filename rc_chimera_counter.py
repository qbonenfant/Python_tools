# coding=utf-8
# This script will count the number of double occurences of edges between
# two reads. This case should only happend if a read map both on reverse
# and forward on the same read. Such mappping could be an indicator of
# self-chimeric reads (read chimeric with a RC copy of itself).


import sys
from collections import defaultdict as dd
with open(sys.argv[1]) as f:
    mapping = dd(set)
    total = 0
    nb_edge = 0
    for line in f:
        data = line.rstrip("\n").split("\t")
        # if we are looking at data and not header
        if(len(data) > 2):
            nb_edge += 1
            read1 = data[0]
            read2 = data[2]
            # read orientation: 0 forward, 1 reverse
            rc = data[4] == "1"
            if(read1 in mapping.keys()):
                if(read2 in mapping[read1]):
                    print(read1, read2)
                    total += 1
                else:
                    mapping[read1].add(read2)
            else:
                mapping[read1].add(read2)
    print("\n#########################################################\n")
    print(total, nb_edge, round(100 * total / nb_edge))
