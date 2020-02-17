# coding=utf-8
import sys


def count_sources(edgeFile):
    sources = set()
    prec = ""
    with open(edgeFile) as f:
        for line in f:
            data = line.rstrip("\n").split()
            if(len(data) > 2):
                if(line[0] != prec):
                    sources.add(data[0])
                    prec = data[0]
    print("Number of source node:")
    print(len(sources))


count_sources(sys.argv[1])
