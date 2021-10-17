# coding = utf-8
# count adapters from an adapter stability benchmark file

import sys
import re
from collections import defaultdict as dd

DNA_rule = re.compile(r'^[ATCG]+$')
adapters = dd(lambda: dd(lambda: dd(int)))


def store_adapter(adapter, method, data):
    try:
        assert(len(data) == 2)
    except AssertionError:
        print("Error on data length")
        print(data)

    start = data[0]
    end = data[1]
    if(start):
        adapters[method]["start"][start] += 1
    if(end):
        adapters[method]["end"][end] += 1


with open(sys.argv[1]) as f:
    method = ""
    data = []
    for line in f:
        line = line.rstrip("\n")
        dna_found = DNA_rule.match(line)

        # ####################################
        # # DEBUG
        # print("###########################")
        # print("Line:", line)
        # print("DNA found:", dna_found)
        # ####################################

        # if method
        if(line != "" and not dna_found):
            if(method):
                store_adapter(adapters, method, data)
            method = line
            data = []
        # if data:
        elif(len(data) < 2):
            data.append(line if line else "None")
        # else, separator
        else:
            store_adapter(adapters, method, data)
            method = ""
            data = []
    if(method and len(data) == 2):
        store_adapter(adapters, method, data)



for method in sorted(adapters.keys(), reverse=True):

    print(method)
    for which_end in ["start", "end"]:
        print(which_end)
        for key in sorted(adapters[method][which_end].keys(),
                          key=lambda x: adapters[method][which_end][x],
                          reverse=True):
            val = adapters[method][which_end][key]
            print("\t".join(str(el) for el in [val, key]))
        print("")
    print("")
