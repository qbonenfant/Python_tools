# coding = utf-8
##################################################################
# Script used to concatenate resultes from Porechop_ABI benchmarks
# using multi run mode.
#
#
# author: Quentin Bonenfant
# contact: quentin.bonenfant@gmail.com
##################################################################

import sys
import os
import re
from collections import defaultdict as dd

ENDS = ["Start", "End"]
DNA_Rule = re.compile(r"^[ATCG]+$")

FREQ_THRESHOLD = 10.0  # 10% frequency threshold.

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


class consensus_freq:
    """ Collect and count the "supporting frequency" for an consensus adapter.
    The supporting frequency represent how many inferred sequences were used
    to make this consensus.
    Ex: 98.3% support for a 30 sequence consensus mean 29 /30 sequences
    were used to make the consensus.
    """
    def __init__(self, freq):
        self.freq = dd(int)
        if(freq):
            self.freq[freq] = 1
        self.count = 1

    # string representation
    def __repr__(self):
        return(f"{self.count} ({self.get_freq()}%)")

    def __str__(self):
        return(self.__repr__())

    def increment(self, freq):
        self.count += 1
        self.freq[freq] += 1

    def get_mean_freq(self):
        assert(len(self.freq.keys()) != 0)
        mean_freq = sum(self.freq)/len(self.freq)
        return(round(mean_freq, 2))

    def get_count(self):
        return(self.count)

    def get_filtered_count(self, threshold):
        f_count = sum(v for k, v in self.freq.items() if k >= threshold)
        return(f_count)

    def freq_stat(self):
        """ Return count for individual frequencies.
        """
        fs = []
        ordered_f = sorted(self.freq.keys(),
                           key=lambda x: self.freq[x],
                           reverse=True)
        just_f = sorted(self.freq.keys())
        # for k in ordered_f:
        for k in just_f:
            fs.append((k, self.freq[k]))
        return(fs)

    def filtered_freq_stat(self, threshold):
        """Filter the frequency statistics by discarding consensus
        with too low supporting frequency.
        """
        fs = []
        valid_k = [k for k in self.freq.keys() if k >= threshold]
        ordered_f = sorted(valid_k)  # ,
        # key=lambda x: self.freq[x],
        # reverse=True)
        for k in ordered_f:
            fs.append((k, self.freq[k]))
        return(fs)


# MAIN PARSER
adapters = {end: {} for end in ENDS}
run_stat = {end: [] for end in ENDS}
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
                run_stat[end].append(consensus_freq(None))
            # Sequence found
            elif(DNA_Rule.match(line)):
                if(line in adapters[end].keys()):
                    adapters[end][line].increment(current_frequency)
                else:
                    adapters[end][line] = consensus_freq(current_frequency)
                # if we added a stat to the adapter, we can keep it for run
                # statisitics
                run_stat[end][-1].increment(current_frequency)

            # If not a blank line, it is a sequence name.
            elif(line):
                current_frequency = float(line.split("_")[2][1:-2])


def detailed_frequency_stats(adapters):
    """ Print the detailed frequency statistics per consensus
    """
    for end in ENDS:
        print(end)
        adp_k = sorted(adapters[end].keys(),
                       key=lambda x:
                       adapters[end][x].get_filtered_count(FREQ_THRESHOLD),
                       # adapters[end][x].get_count(),
                       reverse=True)
        for key in adp_k:
            fs = adapters[end][key].filtered_freq_stat(FREQ_THRESHOLD)
            # fs = adapters[end][key].freq_stat()
            if(fs):
                fs_msg = ", ".join(f"{k}%: {v}" for k, v in fs)
                print(key + "\t" + fs_msg)
        print("")


def per_run_statistics(run_stat):
    """Compute simple "per run" statistics on frequencies
    """
    for end in ENDS:
        print(end)
        no_valid = 0
        for i, run in enumerate(run_stat[end]):
            f_stat = run.filtered_freq_stat(FREQ_THRESHOLD)
            # f_stat = run.freq_stat()
            if(f_stat):
                fs_msg = ", ".join(f"{k}%: {v}" for k, v in f_stat)
                print(f"Run {i}: {fs_msg}")
            else:
                no_valid += 1
        print(f"Runs with no valid consensus: {no_valid}/{len(run_stat[end])}")
        print("")


def plot_allrun_stats(run_stat):
    """Plot general distribution of consensus frequencies
    """
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2)
    for i, end in enumerate(ENDS):
        print(end)
        # retrieving for all runs.
        all_run_stat = dd(list)
        for run in run_stat[end]:
            f_stat = run.filtered_freq_stat(FREQ_THRESHOLD)
            # f_stat = run.freq_stat()
            if(f_stat):
                for k, v in f_stat:
                    all_run_stat[k].append(v)

        # Converting to list
        l, v = zip(*[(str(k)+"%", len(all_run_stat[k]))
                     for k
                     in sorted(all_run_stat.keys())])
        x = range(len(l))
        ax[i].set_xticks(x)
        print(l)
        print(v)
        # ploting for this end
        ax[i].bar(x, v)
        ax[i].set_xticklabels(l)
        ax[i].set_ylim([0, max(v) + 10])
        ax[i].set_title(f"{end} consensus frequency distribution")

    plt.show()


def plot_per_run_statistics(run_stat):
    """Compute simple "per run" statistics on frequencies
    """
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2)
    mx_y = 0
    for i, end in enumerate(ENDS):
        print(end)
        for run in run_stat[end]:
            f_stat = run.filtered_freq_stat(FREQ_THRESHOLD)
            # f_stat = run.freq_stat()
            if(f_stat):
                x, y = zip(*f_stat)
                print(x, y)
                mx_y = max(mx_y, max(y))
                # ploting for this run
                ax[i].scatter(x, y)

        ax[i].set_xlim([0, 100])
        ax[i].set_xlabel(r"% of support")
        ax[i].set_ylim([0, mx_y + 10])
        ax[i].set_ylabel(r"# of consensus")
        ax[i].set_title(f"{end} consensus frequency distribution")
    plt.show()


# detailed_frequency_stats(adapters)
per_run_statistics(run_stat)
# plot_allrun_stats(run_stat)
