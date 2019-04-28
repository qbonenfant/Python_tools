# coding=utf-8

import sys
import os

edgeFile = sys.argv[1]
outFile = sys.argv[2]

outPath = os.path.dirname(outFile)
filename = os.path.basename(outFile)

headFile = open(os.path.join(outPath, "head_" + filename), 'w')  # file containing nodes
graphFile = open(os.path.join(outPath, "edges_" + filename), 'w')  # file containging edges

edgeFormat = '<edge source="{}" target="{}">\n\
<data key="e_nk">{}</data>\n\
</edge>\n'

nodeFormat = '<node id="n{}">\n\
<data key="v_id">{}</data>\n\
</node>\n'


# Printing header
graphmlHeader = '''<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
<key id="v_id" for="node" attr.name="id" attr.type="string"/>
<key id="e_nk" for="edge" attr.name="nk" attr.type="double"/>
<graph id="G" edgedefault="undirected">\n'''

headFile.write(graphmlHeader)

nodes = {}
counter = 0
with open(edgeFile) as f:
    for i, line in enumerate(f):
        if(i >= 2):  # Skipping the first two line of .edge file, they contains informations about the run.
            data = line.rstrip("\n").split("\t")
            fRead = data.pop(0)
            if(fRead not in nodes):
                nodes[fRead] = str(counter)
                counter += 1
            fReadId = nodes[fRead]
            for i in range(0, len(data) - 1, 2):
                read = data[i]
                weight = data[i + 1]
                if(read not in nodes):
                    nodes[read] = str(counter)
                    counter += 1
                graphFile.write(edgeFormat.format('n' + fReadId, 'n' + nodes[read], weight))
graphFile.write('</graph></graphml>\n')
graphFile.close()

graphFile.close()

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
