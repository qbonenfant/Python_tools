# coding=utf-8
import sys
from collections import defaultdict as dd


# Testing if additional read name have been given.
read_name_file = ""
if(len(sys.argv) > 2):
    read_name_file = sys.argv[2]

# Parsing file if yes
read_name_assoc = []
if(read_name_file != ""):
    with open(read_name_file) as f:
        for line in f:
            line = line.rstrip("\n")
            read_name_assoc.append(line)


# keeping track of the number of the number of element in classes.
classes = dd(int)
# parsing cluster file
clusters = []
with open(sys.argv[1]) as f:
    for line in f:
        line = line.rstrip("\n")
        data = []
        for element in line.split("\t"):
            # associating read id to name if required
            if(read_name_assoc):
                read_name = read_name_assoc[int(element)]
            else:
                read_name = element
            data.append(read_name)
            tag = read_name.split("_")[-1]
            classes[tag] += 1
        clusters.append(data)
# print(classes)
for i, cl in enumerate(clusters):
    print("Cluster", i, "size: ", len(cl), "prec",
          "recall", "f1-score", "nb_seq", sep="\t")
    current_classes = list([el.split("_")[-1] for el in cl])
    for cc in set(current_classes):
        if("UNASSIGNED" not in cc):
            nb_elem_class = current_classes.count(cc)
            precision = round(float(nb_elem_class / len(cl)), 4)
            recall = round(float(nb_elem_class / classes[cc]), 4)
            try:
                f1_score = 2 * (precision * recall) / (precision + recall)
                f1_score = round(f1_score, 4)
            except ZeroDivisionError:
                f1_score = "-"

            print("Class", cc, "", "", precision, recall,
                  f1_score, nb_elem_class, sep="\t")
    print("\n")
