# coding=utf-8
# Remove unassigned reads from a tagged edge file
import sys


with open(sys.argv[1]) as f:
    for line in f:
        data = line.rstrip("\n").split("\t")
        fRead = data.pop(0)
        if(fRead.split("_")[-1] != "UNASSIGNED"):
            out = []
            for i in range(0, len(data), 2):
                read, nk = data[i], data[i + 1]
                if(read.split("_")[-1] != "UNASSIGNED"):
                    out.append(read)
                    out.append(nk)
            print(fRead + "\t" + "\t".join(out))
