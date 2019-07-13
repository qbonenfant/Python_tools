#coding = utf-8
# display sequences id which length is lower than the required threshold.
import sys

lim = int(sys.argv[2])
seq = ""
acc = ""
with open(sys.argv[1]) as f:
    for line in f:
        if(line[0] == ">"):
            if(acc and len(seq) <= lim):
                print(acc)
            seq = ""
            acc = line[1:].rstrip("\n")
        else:
            seq += line.rstrip("\n")
    if(len(seq) <= lim):
        print(acc)
