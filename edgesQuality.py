#coding =utf-8

# Read tagged edges file and compute rand index by compraring to "ground truth"
# gene cluster read count.

import sys
import os
from collections import defaultdict as dd


def computeIsoQuality(edgeList):

    TP = 0
    TN = 0
    FP = 0
    FN = 0

    # current mapping
    for edge in edgeList:
        read1 = edge[0]
        l1 = int(edge[1])
        read2 = edge[2]
        l2 = int(edge[3])
        # orientation = edge[4]
        pos = [tuple(int(a) for a in el.split(",")) for el in edge[6:]]

        ref_gene = read1.split("_")[-1]
        tgt_gene = read2.split("_")[-1]
        same_iso = int(edge[5]) >= 2

        # print(ref_gene,tgt_gene)
        if(same_iso):
            if(ref_gene == tgt_gene):
                TP += 1
            else:
                FP += 1
        else:
            if(ref_gene == tgt_gene):
                FN += 1
            else:
                TN += 1
    return(TP, FP, TN, FN)


def computeClustQuality(edgeList):

    TP = 0
    TN = 0
    FP = 0
    FN = 0

    # current mapping
    for edge in edgeList:
        read1 = edge[0]
        l1 = int(edge[1])
        read2 = edge[2]
        l2 = int(edge[3])
        # orientation = edge[4]
        pos = [tuple(int(a) for a in el.split(",")) for el in edge[6:]]

        ref_gene = read1.split("_")[-1]
        tgt_gene = read2.split("_")[-1]

        # True positive if edge is right
        if(ref_gene == tgt_gene):
            TP += 1
        # False positive if edge is wrong
        else:
            FP += 1

    return(TP, FP, TN, FN)


def parse_edge(edgeFile):
    with open(edgeFile) as f:
        edgeList = []
        for i, line in enumerate(f):
            if(i >= 2):
                line = line.rstrip("\n")
                edgeList.append(line.split("\t"))
    return(edgeList)


def compute_stats(edgeList):

    TP, FP, TN, FN = computeClustQuality(edgeList)
    try:
        precision = round(float(100 * TP) / (TP + FP), 2)
        recall = round(float(100 * TP) / (TP + FN), 2)
        fmeasure = round((2 * precision * recall) / (precision + recall), 2)
        oddratio = round((TP / FP) / (FN / TN), 2)

    except ZeroDivisionError:
        print("One of the value is null.")

    else:
        print("Precision: ", precision)
        print("Recall   : ", recall)
        print("fmeasure : ", fmeasure)
        print("DOG      : ", oddratio)

    finally:

        print("TP", "FP", "TN", "FN", sep="\t")
        print(TP, FP, TN, FN, sep="\t")


current_path = sys.argv[1]
edge_files = []
# if we have a single file work on this one only
if(os.path.isfile(current_path)):
    edge_files.append(current_path)
# if we get a path, work on all edge files
elif(os.path.isdir(current_path)):
    for element in os.listdir(current_path):
        if(".edge" in element[-6:]):
            edge_files.append(os.path.join(current_path, element))

for edge_file in edge_files:
    print(os.path.basename(edge_file))
    el = parse_edge(edge_file)
    print("Parsed " + str(len(el)) + " edges")
    compute_stats(el)
