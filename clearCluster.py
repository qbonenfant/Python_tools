# coding=utf-8
# Remove unassigned reads from a tagged cluster file
import sys


with open(sys.argv[1]) as f:
    for line in f:
        data = line.rstrip("\n").split("\t")
        out = []
        for read in data:
            if(read.split("_")[-1] != "UNASSIGNED"):
                out.append(read)
        print("\t".join(out))
