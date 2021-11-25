#coding = utf-8
import sys
import os
import re
from collections import defaultdict as dd

ENDS = ["Start", "End"]
DNA_Rule = re.compile(r"^[ATCG]+$")

"""
Start
Consensus_1_(50.0%)
CTGTTGTACTTCGTTCAGTTACGTATTGCTCTTGCCTGTCGCTCTATCTTCGGCGTCTGCTTGGGTGTTTAACCTTTT

Consensus_2_(50.0%)
ATGTACTTCGTTCAGTTACGTATTGCTTCTGTTGGTGCTGATATTGCGGCGTCTGCTTGGGTGTTTAACCTTTT

End
Consensus_1_(53.3%)
GGTTAAACACCCAAGCAGACGCCGAAGATAGAGCGACAGGCAAGTAGCAATACGTAACTGA

Consensus_2_(46.7%)
GGTTAAACACCCAAGCAGACGCCGCAATATCAGCACCAACAGAAAGCA


Start
Consensus_1_(50.0%)
"""

class consensus_adp:
    def __init__(self, freq):
        self.freq = [freq]
        self.count = 1

    # string representation
    def __repr__(self):
        return(f"{self.count} ({self.get_freq()}%)")

    def __str__(self):
        return(self.__repr__())

    def increment(self, freq):
        self.count += 1
        self.freq.append(freq)

    def get_freq(self):
        assert(len(self.freq) != 0)
        mean_freq = sum(self.freq)/len(self.freq)
        return(round(mean_freq,2))

    def freq_stat(self):
        freq_dic = {}
        keys = set(self.freq)
        for k in keys:
            freq_dic[k] = self.freq.count(k)
        fs = []
        for k in sorted(freq_dic, key=lambda x: freq_dic[x], reverse=True):
            fs.append( (k,freq_dic[k]))
        return(fs)


    def get_count(self):
        return(self.count)


adapters = {end:{} for end in ENDS}
# adapters["Start"][adp_seq] = 
with open(sys.argv[1]) as f:
    loop = True
    end = ""
    current_frequency = 0
    sequence = ""
    while loop:
        try:
            line = next(f).rstrip("\n")
        except StopIteration:
            loop = 0
        else:
            # Start or End section begins
            if(line in ENDS):
                end = line
            # Sequence found
            elif(DNA_Rule.match(line)):
                if(line in adapters[end].keys()):
                    adapters[end][line].increment(current_frequency)
                else:
                    adapters[end][line] = consensus_adp(current_frequency)

            # If not a blank line, it is a sequence name.
            elif(line):
                current_frequency = float(line.split("_")[2][1:-2])

for end in ENDS:
    print(end)
    for key in sorted(adapters[end].keys(),
                      key=lambda x: adapters[end][x].get_count(),
                      reverse=True):
        fs = adapters[end][key].freq_stat()
        fs_msg = ", ".join(f"{k}%: {v}" for k,v in fs)
        print(key + "\t" + fs_msg)
    print("")