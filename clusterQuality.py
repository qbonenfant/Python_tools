# coding =utf-8

# Read tagged edges file and compute rand index by compraring to "ground truth"
# gene cluster read count.

import sys
from sklearn import metrics

# Disabling warning for this code
import warnings
warnings.filterwarnings("ignore")

clusterFile = sys.argv[1]  # tabbed cluster file

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
            # prediction label = my clustering
            labels_pred.append(nbCluster)
            # "truth"
            tag = el.split("_")[-1]
            nodes.add("_".join(el.split("_")[:-1]))
            try:
                labels_true.append(genes.index(tag))
            except ValueError:
                genes.append(tag)
                labels_true.append(len(genes) - 1)
            cl_size+=1
        if(cl_size == 1):
            single +=1
        nbCluster += 1
        nbElem += len(elements)


print("Number of clusters:"     ,nbCluster  , sep = "\t")
print("Singletons: "            ,single     , sep = "\t")
print("Total number of elements",nbElem     , sep = "\t")


# Metrics
ari = metrics.adjusted_rand_score(labels_true, labels_pred)
print("Adjusted Rand Index :", ari, sep = "\t")

# compute homogeneity,completeness and vmeasuer all at once
h,c,vm = metrics.homogeneity_completeness_v_measure(labels_true, labels_pred)

print("Homogeneity :" , h , sep = "\t")
print("Completeness :" , c, sep = "\t")
print("V-measure :", vm, sep = "\t")

#F1 score, or F-Measure
f1 = (metrics.f1_score(labels_true, labels_pred)
print("F1-Score : ", f1, sep = "\t")
