# coding = utf-8
# count adapters from an adapter stability benchmark

import sys
from collections import defaultdict as dd


adapters = dd(lambda: dd(lambda: dd(int)))

with open(sys.argv[1]) as f:
    loop = 1
    lc = 0
    data = []
    while loop:
        try:

            line = next(f).rstrip("\n")
            if (lc % 7 != 6):
                data.append(line)
            else:
                for i in range(0, len(data), 3):
                    method = data[i]
                    start = data[i + 1]
                    end = data[i + 2]
                    adapters[method]["start"][start] += 1
                    adapters[method]["end"][end] += 1
                data = []
        except StopIteration:
            loop = 0
        lc += 1

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
