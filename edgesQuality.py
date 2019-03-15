#coding =utf-8

# Read tagged edges file and compute rand index by compraring to "ground truth"
# gene cluster read count.

import sys
from collections import defaultdict as dd

edgeFile = sys.argv[1]
countFile = sys.argv[2]
fields = ["Read Number ", "Read Name",
          "Nb Reads", "Precision", "Recall", "FP", "FN"]
print("\t".join(fields))


def computeClustQuality(initialRead, edgeList, geneCount, clNb):
    initialGene = initialRead.split("_")[-1]
    geneSet = dd(int)
    geneSet[initialGene] += 1
    data = []
    nbReads = 1
    for read in edgeList[::2]:
        g = read.split("_")[-1]
        geneSet[g] += 1
        nbReads += 1
    if(initialGene != "UNASSIGNED"):
        # CLuster nb
        data.append("N° " + str(clNb))
        # Firstread
        data.append(initialRead)
        # nbReads
        data.append(nbReads)
        # Precision
        data.append(round(float(geneSet[initialGene] / nbReads), 2))
        # Recall
        data.append(
            round(float(geneSet[initialGene] / geneCount[initialGene]), 2))
        # % False Positive
        data.append(
            round(float((nbReads - geneSet[initialGene]) / nbReads), 2))
        # % False Negative
        data.append(round(float(
            (geneCount[initialGene] - geneSet[initialGene]) / geneCount[initialGene]), 2))
    else:
        data = ["N° " + str(clNb), initialRead, nbReads,
                "None", "None", "None", "None"]

    # Print first line (clustering information about first read associated gene)
    print("\t".join([str(el) for el in data]))

    # Computing data for all genes in this line ( proportion only)
    for i, g in enumerate(geneSet.keys()):
        if(g != "UNASSIGNED"):
            print("  " + str(i + 1) + "\t" + g + "\t" + str(geneSet[g]) + "\t" + str(round(float(
                geneSet[g] / nbReads), 2)) + "\t" + str(round(float(geneSet[g] / geneCount[g]), 2)))
        else:
            print("  " + str(i + 1) + "\t" + g + "\t" + str(geneSet[g]) + "\t" + str(
                round(float(geneSet[g] / nbReads), 2)) + "\t" + "None" + "\t" + "None")
    print("")


geneCount = {}
with open(countFile) as f:
    for line in f:
        geneName, c = line.rstrip("\n").split("\t")
        geneCount[geneName] = int(c)


with open(edgeFile) as f:
    end = False
    clusterNb = 0
    while(not end):
        try:
            direct = next(f).rstrip("\n").split("\t")
            reverse = next(f).rstrip("\n").split("\t")
        except StopIteration:
            end = True
        else:
            initialRead = direct.pop(0)
            reverse.pop(0)
            ri = computeClustQuality(
                initialRead, direct + reverse, geneCount, clusterNb)
            clusterNb += 1
