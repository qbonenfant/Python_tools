import sys
from collections import defaultdict as dd

distri = dd(int)

with open(sys.argv[1]) as f:
    for line in f:
        distri[len(line.rstrip("\n").split("\t"))] += 1
for k in sorted(list(distri.keys())):
    print(k, distri[k], sep="\t")
