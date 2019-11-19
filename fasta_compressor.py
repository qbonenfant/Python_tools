# coding=utf-8
import sys

# Compression "ratio" setting
cmp = 1
if(len(sys.argv) > 2):
    cmp = int(sys.argv[2])

# Keeping track of how many
# nucleotides have been removed
printed_nuc = 0
deleted_nuc = 0

with open(sys.argv[1]) as f:
    for line in f:
        line = line.rstrip("\n")
        if(line[0] == ">"):
            print(line)
        else:
            prev = ""
            count = 0
            for nc in line:
                if(nc == prev):
                    count += 1
                else:
                    prev = nc
                    count = 1
                if(count <= cmp):
                    printed_nuc += 1
                    print(nc, end="")
                else:
                    deleted_nuc += 1
            print("")

cmp_ratio = round(float(printed_nuc) / (printed_nuc + deleted_nuc), 2)
print("Deleted nucleotides: ", deleted_nuc, file=sys.stderr)
print("Printed nucleotides: ", printed_nuc, file=sys.stderr)
print("Compression ratio  : ", cmp_ratio , file=sys.stderr)
