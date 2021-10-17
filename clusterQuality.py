# coding =utf-8

# Read tagged edges file and compute rand index by compraring to "ground truth"
# gene cluster read count.

import sys
from sklearn import metrics
from collections import defaultdict as dd
# Disabling warning for this code
import warnings
warnings.filterwarnings("ignore")

clusterFile = sys.argv[1]  # tabbed cluster file
fasta_file = sys.argv[2]   # fasta file

# Clustering general info
nbCluster = 0
nbElem = 0
single = 0
classes = []

# SciKit label vectors
labels_pred = []
labels_true = []

# storing clusters
clusters = {}

# PARSING FASTA FILE
# Allows us to keep the real number of reads and
# associate read names to their id if required.
read_names = []
with open(fasta_file) as f:
    for line in f:
        if(line[0] == ">"):
            line = line.rstrip("\n").split()[0][1:]
            read_names.append(line)


# PARSING CLUSTER FILE
with open(clusterFile) as f:
    for cluster in f:
        data = cluster.rstrip("\n").split("\t")
        cl_size = 0
        for el in data:
            # if read names are number, we must use their id
            # to retreived their original name from the fasta
            try:
                read_name = read_names[int(el)]
            except ValueError:
                # if the read name is not a number
                # then just use it as is
                read_name = el

            # Associating read name to cluster number
            clusters[read_name] = nbCluster

            # cluster size
            cl_size += 1
        # updating singleton count
        if(cl_size == 1):
            single += 1

        # and updating cluster id / total sizes
        nbCluster += 1
        nbElem += cl_size


# LABELING
print("Generating labels...")
for read in read_names:

    # In the case not all singleton are included in the cluster file
    # we need to count them now

    # trying to fetch read cluster id
    try:
        cl_id = clusters[read]
    except KeyError:
        # If key not found, this read is not in a cluster, so a singleton
        single += 1
        # Using the current number of cluster as cluster id
        cl_id = nbCluster
        # And increasing the number of cluster available
        nbCluster += 1

    # "truth"
    tag = read.split("_")[-1]
    # Storing distinct classes
    if(tag not in classes):
        classes.append(tag)
    # "thruth" label
    labels_true.append(classes.index(tag))
    # prediction label
    labels_pred.append(cl_id)

print("Number of clusters:", nbCluster, sep="\t")
print("Number of classes:", len(set(labels_true)), sep="\t")
print("Singletons: ", single, sep="\t")
print("Total number of elements", nbElem, sep="\t")


##############################################################################
# Metrics
#
# print(metrics.classification_report(labels_true, labels_pred))#, labels=classes))

MI = metrics.mutual_info_score(labels_true, labels_pred)
print("Mutual information :", MI, sep="\t")

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
