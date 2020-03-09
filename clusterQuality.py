# coding =utf-8

# Read tagged edges file and compute rand index by compraring to "ground truth"
# gene cluster read count.

import sys
from sklearn import metrics

# Disabling warning for this code
import warnings
warnings.filterwarnings("ignore")

clusterFile = sys.argv[1]  # tabbed cluster file
read_name_file = ""
if(len(sys.argv) > 2):
    read_name_file = sys.argv[2]

read_name_assoc = []
if(read_name_file != ""):
    with open(read_name_file) as f:
        for line in f:
            line = line.rstrip("\n")
            read_name_assoc.append(line)


nbCluster = 0
nbElem = 0
single = 0
labels_pred = []
labels_true = []
genes = []
nodes = set()
print("Generating labels...")
with open(clusterFile) as f:
    for cluster in f:
        elements = cluster.rstrip("\n").split("\t")
        cl_size = 0
        for el in elements:

            # Should check for name type...
            if(read_name_assoc):
                read_name = read_name_assoc[int(el)]
            else:
                read_name = el

            # "truth"
            tag = read_name.split("_")[-1]
            nodes.add("_".join(read_name.split("_")[:-1]))
            if(tag not in genes):
                genes.append(tag)

            # adding "thruth" label
            labels_true.append(genes.index(tag))
            # prediction label = my clustering
            labels_pred.append(nbCluster)

            cl_size += 1
        if(cl_size == 1):
            single += 1
        nbCluster += 1
        nbElem += len(elements)



print("Number of clusters:", nbCluster, sep="\t")
print("Singletons: ", single, sep="\t")
print("Total number of elements", nbElem, sep="\t")


##############################################################################
# Metrics
#
#  print(genes)
print(metrics.classification_report(labels_true, labels_pred))#, labels=genes))

# # Adjusted Rand Index
ari = metrics.adjusted_rand_score(labels_true, labels_pred)
print("Adjusted Rand Index :", ari, sep="\t")


# # Homogeneity, completeness and V-measure
h, c, vm = metrics.homogeneity_completeness_v_measure(labels_true, labels_pred)
print("Homogeneity :", h, sep="\t")
print("Completeness :", c, sep="\t")
print("V-measure :", vm, sep="\t")

# acc = metrics.accuracy_score(labels_true, labels_pred)
# print("Accuracy :", acc, sep="\t")


# Precision, recall, fscore
# pr, rc, f_score, support = metrics.precision_recall_fscore_support(labels_true, labels_pred)
# print("Precison :", pr, sep="\t")
# print("Recall :", rc, sep="\t")
# print("F1-Score :", f_score, sep="\t")
