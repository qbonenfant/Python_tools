# coding=utf-8
# Search for edges in an edge file
# that are not in the same community according to a partition
# format are .edge for edge input and g2rl for partition.
import sys
from collections import defaultdict

g2rfile = sys.argv[1]
edge_file = sys.argv[2]
THRESHOLD = int(sys.argv[3]) if len(sys.argv) > 3 else 1

# Fetching communityfrom G2R file
community = {}
with open(g2rfile) as f:
    current_community = ""
    for line in f:
        line = line.rstrip("\n")
        tag, element = line.split("\t")

        if(tag == "R"):
            community[element] = current_community
        else:
            current_community = element


# count the number of rejected edges for each node
rejected_node_count = defaultdict(int)
# Count the number of edges for each node
edge_count = defaultdict(int)

# going through the edge file, testing edges
with open(edge_file) as f:
    current_source = ""
    current_community = ""
    for line in f:
        line = line.rstrip("\n")
        data = line.split("\t")
        if(len(data) > 2):
            read1 = data[0]
            read2 = data[2]

            # limit the number of check in community dict
            if(read1 != current_source):
                current_source = read1
                current_community = community[read1]
            tgt_community = community[read2]

            # printing only line were edges are not in the same community.
            # this mean our clustering decided to cut those edges.
            if(current_community != tgt_community):
                rejected_node_count[read1] += 1
                rejected_node_count[read2] += 1
            # Increase edge count for each node
            edge_count[read1] += 1
            edge_count[read2] += 1


# Printing results
for node in sorted(rejected_node_count.keys(), key=lambda x: rejected_node_count[x], reverse=True):
    count = rejected_node_count[node]
    if(count > THRESHOLD):
        # print(node, rejected_node_count[node], edge_count[node], sep="\t")
        print(node)
