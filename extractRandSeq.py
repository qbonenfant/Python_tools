# coding=utf-8

import random
import sys


fileName = sys.argv[1]
nbSeq = int(sys.argv[2])

f = open(fileName, 'r')
nbLines = 0  # offset to simplify further operation
for l in f:
    nbLines += 1

seqIndex = set()
while len(seqIndex) < nbSeq*2:
    rndPos = random.randint(0, nbLines)
    seqIndex.add(rndPos - rndPos % 2)  # only getting even  line number
    seqIndex.add((rndPos - rndPos % 2) + 1)  # followed by uneven line number
# getting back to the begining of the file
f.seek(0)
for i, line in enumerate(f):
    if(i in seqIndex):
        print(line.rstrip("\n"))
f.close()
