# coding=utf-8

import sys
import os

edgeFile = sys.argv[1]
outFile = sys.argv[2]

outPath = os.path.dirname(outFile)
filename = os.path.basename(outFile)

headFile = open(os.path.join(outPath, "head_" + filename),
                'w')  # file containing nodes
graphFile = open(os.path.join(outPath, "edges_" + filename),
                 'w')  # file containging edges

edgeFormat = '<edge source="{}" target="{}">\n\
<data key="e_nk">{}</data>\n\
<data key="e_dir">{}</data>\n\
<data key="e_iso">{}</data>\n\
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
<key id="e_dir" for="edge" attr.name="dir" attr.type="boolean"/>
<key id="e_iso" for="edge" attr.name="is_iso" attr.type="double"/>
<graph id="G" edgedefault="undirected">\n'''

headFile.write(graphmlHeader)

nodes = {}
counter = 0
with open(edgeFile) as f:
    for i, line in enumerate(f):
        # Skipping the first two line of .edge file,
        # they contains informations about the run.
        if(i >= 2):

            data = line.rstrip("\n").split("\t")
            fRead = data[0]
            l1 = int(data[1])
            read = data[2]
            l2 = int(data[3])
            orientation = data[4]
            is_iso = data[5]
            pos = [tuple(int(a) for a in el.split(",")) for el in data[6:]]
            weight = len(pos)

            for r in [fRead, read]:
                if(r not in nodes):
                    nodes[r] = str(counter)
                    counter += 1

            graphFile.write(edgeFormat.format(
                'n' + nodes[fRead], 'n' + nodes[read], weight, orientation, is_iso))


graphFile.write('</graph></graphml>\n')
graphFile.close()

graphFile.close()

for node, nb in nodes.items():
    headFile.write(nodeFormat.format(nb, node))

headFile.close()

print("CONCATENING FILES AND CLEANING")
filenames = [os.path.join(outPath, "head_" + filename),
             os.path.join(outPath, "edges_" + filename)]
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
