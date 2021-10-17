# coding=utf-8

import sys

with open(sys.argv[1]) as f:
    for line in f:
        line = line.rstrip("\n")
        data = line.split("\t")
        if(len(data) > 2):
            buff = "\t".join(data[0:6])
            last = ("", "")
            for el in data[6:]:
                a, b = el.split(",")
                c, d = last
                if(a != c and b != d):
                    buff += "\t" + el
                last = (a, b)
            print(buff)
        else:
            print(line)
