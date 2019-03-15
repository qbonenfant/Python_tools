# coding=utf-8
# convert transcript tag to appropriate gene tag
import sys
import os
import re


transcript_rule = re.compile(r'ENSMUST\d+\.?\d*')

to_convert_file = sys.argv[1]
path = os.path.dirname(to_convert_file)
file_base = os.path.basename(to_convert_file)
converted_file = os.path.join(path, "gene_tag" + file_base)
g2t_file = sys.argv[2]

# associating a gene to a transcript
t2g = {}
current_gene = ""
with open(g2t_file, 'r') as f:
    for line in f:
        line = line.rstrip("\n")
        t, value = line.split("\t")
        if(t == "G"):
            current_gene = value
        else:
            t2g[value] = current_gene

# converting

out = open(converted_file, "w")
with open(to_convert_file, 'r') as f:
    for line in f:
        line = line.rstrip("\n")
        newLine = line
        for occ in transcript_rule.finditer(line):
            transcript = occ.group(0)
            shortened = transcript.split('.')[0]
            if(shortened in t2g.keys()):
                newLine = newLine.replace(transcript, t2g[transcript.split('.')[0]])
            else:
                print("TRANSCRIPT NOT IN TRANSCRIPTOM ?? ", transcript)
        out.write(newLine)
out.close
