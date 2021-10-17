# coding=utf-8
# Remove read from assoc file if they are not part of a cluster


import sys

if(len(sys.argv) < 3):
    print("USAGE: filter_assoc.py <cluster_file> <assoc_file>")
    exit()

cluster_file = sys.argv[1]
assoc_file = sys.argv[2]

reads = set()

with open(cluster_file) as f:
    for line in f:
        reads.update(line.rstrip("\n").split("\t"))

with open(assoc_file) as f:
    for line in f:
        read, cl = line.rstrip("\n").split("\t")
        if(read in reads):
            print(line.rstrip("\n"))
