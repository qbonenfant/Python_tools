# coding=utf-8
# Convert G2Rl files to tabbed cluster.
# Classes marker are given by the tagFlag value
import sys
from collections import defaultdict as dd

if(len(sys.argv) < 2 or len(sys.argv) > 4):
    print("USAGE: g2r_2_cluster.py <g2r_file> [tag_flag] [elem_flag]")

tagfile = sys.argv[1]
tagflag = sys.argv[2] if len(sys.argv) > 2 else "G"
elemflag = sys.argv[3] if len(sys.argv) > 3 else "R"

# sotring cluster in dicts, class as key
clusters = dd(list)


with open(tagfile) as f:
    current_commu = ""
    for line in f:
        data = line.rstrip("\n").split()
        if(data[0] == tagflag):
            # try to convert to int, if possible
            try:
                current_commu = int(data[1])
            except TypeError:
                current_commu = data[1]
        elif(data[0] == elemflag):
            clusters[current_commu].append(data[1])

for commu in sorted(clusters.keys()):
    print("\t".join(clusters[commu]))
