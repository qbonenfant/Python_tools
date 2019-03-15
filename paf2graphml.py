########################################################################
# Convert a paf file to a graphml file in the most dirty way possible.
# It's ugly, but works on big dataset. 
# This script works on BIG datasets, and generate two temp files.
# Since RM command a used, do not use this script with high level perm, 
# to avoid potential accidental deletions.
########################################################################
# coding=utf-8

import sys
import os

pafFile = sys.argv[1]
outFile = sys.argv[2]

outPath = os.path.dirname(outFile)
filename = os.path.basename(outFile)


headFile = open(os.path.join(outPath, "head_" + filename), 'w')  # file containing nodes
graphFile = open(os.path.join(outPath, "edges_" + filename), 'w')  # file containging edges


edgeFormat = '    <edge source="{}" target="{}"/>\n'

nodeFormat = '    <node id="n{}">\n\
      <data key="v_id">{}</data>\n\
    </node>\n'


# Printing header
graphmlHeader = '''<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
         http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
<!-- Created by paf2graphml -->
  <key id="v_id" for="node" attr.name="id" attr.type="string"/>
  <graph id="G" edgedefault="undirected">\n'''

headFile.write(graphmlHeader)

nodes = {}
counter = 0
print("PARSING PAF FILE")
with open(pafFile) as f:
    print("EXPORTING EDGES")
    for line in f:
        data = line.rstrip("\n").split("\t")
        read1 = data[0]
        read2 = data[5]
        if(read1 != read2):
            if(read1 not in nodes):
                nodes[read1] = str(counter)
                counter += 1

            if(read2 not in nodes):
                nodes[read2] = str(counter)
                counter += 1
            graphFile.write(edgeFormat.format('n' + nodes[read1], 'n' + nodes[read2]))
graphFile.write('</graph></graphml>\n')
graphFile.close()

print("EXPORTING NODES")
for node, nb in nodes.items():
    headFile.write(nodeFormat.format(nb, node))

headFile.close()
print("CONCATENING FILES AND CLEANING")
filenames = [os.path.join(outPath, "head_" + filename), os.path.join(outPath, "edges_" + filename)]
with open(outFile, 'w') as outfile:
    for fname in filenames:
        print("cat " + fname + " >> " + outfile.name)
        infile = open(fname)
        for line in infile:
            outfile.write(line)
        infile.close()
        print("rm " + fname)
        os.system("rm " + fname)
print('DONE')
