# coding=utf-8

import sys

from collections import defaultdict as dd

import matplotlib.pyplot as plt
import matplotlib.colors as colors


class color_mix:

    def __init__(self, value):
        self.R = value[0]
        self.G = value[1]
        self.B = value[2]
        self.nb = 1

    def mix(self, col):
        weight = self.nb + 1
        newR = (self.R * self.nb + col.R) / weight
        newG = (self.G * self.nb + col.G) / weight
        newB = (self.B * self.nb + col.B) / weight
        self.R = newR
        self.G = newG
        self.B = newB
        self.nb += 1

    def get_col(self):
        return((self.R, self.G, self.B))


def get_coverage(pos_list, l1, l2, k=15):
    coverage_ref = dd(int)
    coverage_tgt = dd(int)
    for p in pos_list:
        # computing coverage
        for j in range(k):
            coverage_ref[p[0] + j] += 1
            coverage_tgt[p[1] + j] += 1
    return(coverage_ref, coverage_tgt)


def get_coherence(pos_list):
    """Testing seed coherence"""

    # keeping relative differences, this is out observation set.
    diff_vec = []
    last_ref = pos_list[0][0]
    last_tgt = pos_list[0][1]
    for p in pos_list:
        # how much did we advanced on reference and target ?
        dif_ref = abs(p[0] - last_ref)
        dif_tgt = abs(p[1] - last_tgt)

        # offset difference  between the two read
        relative_diff = abs(dif_ref - dif_tgt)
        diff_vec.append(relative_diff)

        last_ref = p[0]
        last_tgt = p[1]
    return(diff_vec)

# Compute a similarity score between two reads using coverage and
# a seed gap coherence score


def checksum(elem):
    csum = 0
    for c in elem:
        csum ^= (ord(c)**2 + 2*csum)//3 % 256
    return((csum % 256))


def edge_score(l1, l2, pos_list, k=15):

    # init the coverage vectors
    coverage_ref, coverage_tgt = get_coverage(pos_list, l1, l2)

    # COmputing each cover
    # cover_ref = cover(l1, coverage_ref)
    # cover_tgt = cover(l2, coverage_tgt)
    cover_ref = float(sum(coverage_ref) / len(coverage_ref))
    cover_tgt = float(sum(coverage_tgt) / len(coverage_tgt))

    # coverage score is the smallest coverage between ref and target
    # coverage_score = max(cover_tgt, cover_ref)

    # Testing coherence
    diff_vec = get_coherence(pos_list)
    try:
        coherence_score = 1 - 1 / max(diff_vec)
    except ZeroDivisionError:
        coherence_score = 1.0

    # Computing edge score as the harmonic mean between coverage and coherence
    # edge_score = 2 * coherence_score * coverage_score / \
    #     float(coverage_score + coherence_score)

    # return(edge_score)
    return(cover_ref, cover_tgt, coherence_score)


##############################################################################
# Main start
# fasta = parse_fasta(sys.argv[2])

# parsing edge file


node_pileup = {}
node_support = {}
coverage_list = []

ef = sys.argv[1]
the_node = sys.argv[2]

with open(ef) as edge_file:
    for line in edge_file:
        line = line.rstrip("\n")
        data = line.split("\t")
        if(len(data) > 2):
            read1 = data[0]
            l1 = int(data[1])
            read2 = data[2]
            l2 = int(data[3])

            if(read1 == the_node or read2 == the_node):

                # orientation = data[4]
                pos = [tuple(int(a) for a in el.split(",")) for el in data[6:]]

                # checking if reads are the same isoforms or not.
                ref_gene = read1.split("_")[-1]
                tgt_gene = read2.split("_")[-1]

                coverage_ref, coverage_tgt = get_coverage(pos, l1, l2)

                if(read1 == the_node):
                    the_coverage = coverage_ref
                    csum = checksum(read2.split("_")[-1])
                    print("Coloring pos for ", read2)
                elif(read2 == the_node):
                    the_coverage = coverage_tgt
                    csum = checksum(read1.split("_")[-1])
                    print("Coloring pos for ", read1)

                rgb_col = colors.hsv_to_rgb((float(csum / 256), .8, .8))
                the_col = color_mix(rgb_col)

                coverage_list.append(the_coverage)

                for p, sup in the_coverage.items():
                    if(p not in node_pileup.keys()):
                        node_pileup[p] = the_col
                        node_support[p] = 0
                    else:
                        node_pileup[p].mix(the_col)
                    node_support[p] += sup


x = sorted(list(node_pileup.keys()))
y = [node_support[el] for el in x]
c = [node_pileup[el].get_col() for el in x]
data = {'x': x,
        'y': y,
        'c': c}

plt.scatter('x', 'y', c='c', marker= "+", data=data)

# for i, cv in enumerate(coverage_list):
#     x = sorted(cv.keys())
#     y = [cv[el] for el in x]
#     plt.plot(x,y)

plt.ylabel('support')
plt.xlabel('position')
plt.legend()
plt.show()
