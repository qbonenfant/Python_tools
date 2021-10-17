# coding=utf-8

# Compute average occurence of seed per line and std dev

import sys
from math import sqrt

edgeFile = sys.argv[1]


def mean_std_dev(elements):
    mean = float(sum(elements) / len(elements))
    std_dev = 0.0
    for el in elements:
        std_dev += (el - mean)**2
    return(mean, sqrt(std_dev / len(elements)))


elements = []
with open(edgeFile, "r") as f:
    for line in f:
        data = line.rstrip("\n").split("\t")
        if(len(data) > 2):
            elements.append(len(data[6:]))

print(mean_std_dev(elements))
