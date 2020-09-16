# coding=utf-8

import sys
from collections import defaultdict as dd

filename = sys.argv[1]
k = int(sys.argv[2]) if len(sys.argv) > 2 else 16
sample_len = int(sys.argv[3]) if len(sys.argv) > 3 else 100
sample_size = int(sys.argv[4]) if len(sys.argv) > 4 else 40000


kmer_count = dd(int)
sampled = 0
with open(filename) as f:
    seq = ""
    for line in f:
        if(line[0] != ">"):
            seq += line.rstrip("\n")
        elif(seq != "" and len(seq) > 3*sample_len):
            pos = (len(seq) - sample_len) // 2
            for i in range(sample_len - k + 1):
                kmer_count[seq[pos:pos + k]] += 1
                pos += 1

            sampled += 1
        if(sampled >= sample_size):
            break

for k in sorted(kmer_count.keys(), key=lambda x: kmer_count[x], reverse = True):
    print(k, kmer_count[k], sep="\t")
