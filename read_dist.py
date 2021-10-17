# coding=utf-8
import sys
from collections import defaultdict as dd
import matplotlib.pyplot as plt

def dist_fasta(fasta_file):
    dist = dd(int)
    seq = ""
    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.rstrip("\n")
            if(line[0] == ">"):
                if(seq != ""):
                    dist[len(seq)] += 1
                    seq = ""
            else:
                seq += line
        dist[len(seq)] += 1
    return(dist)


dist = dist_fasta(sys.argv[1])

s = []
n = []
for k in sorted(dist.keys()):
	s.append(k)
	n.append(dist[k])


fig, ax = plt.subplots()
ax.bar(s,n)

ax.set(xlabel='size', ylabel='number',
       title='Size distribution of read length')
ax.grid()

plt.show()