# coding=utf-8

import sys
import re
from collections import defaultdict


adapters = {}
DNARULE = re.compile(r'^[ATCG]+$')
seq_type = ""
with open(sys.argv[1]) as f:

    while True:
        try:
            seq_type =  next(f).rstrip("\n")
            forward  =  next(f).rstrip("\n")
            reverse  =  next(f).rstrip("\n")
        except StopIteration:
            break
        else:
            if(seq_type not in adapters):
                adapters[seq_type] = {}
                adapters[seq_type]["start"] = defaultdict(int)
                adapters[seq_type]["end"] = defaultdict(int)

            adapters[seq_type]["start"][forward] += 1
            adapters[seq_type]["end"][reverse] += 1

for st in adapters:
    for extremite in ["start", "end"]:
        print(st, ", ", extremite)
        for adapter, count in sorted(adapters[st][extremite].items(), reverse=True, key= lambda x: x[1]):
            print(adapter, count)
