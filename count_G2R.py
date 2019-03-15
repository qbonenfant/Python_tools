#coding=utf-8

# Count and sort the number of reads for genes and transcripts from a "gene to read list" output.
# (see nanotools transcript2meta.py code)

import sys
import os

g2r_dict={}
g2r_file = sys.argv[1]
out_path = os.path.dirname(g2r_file)
out_file = os.path.join(out_path, os.path.basename(g2r_file) + "_count.txt")

with open(g2r_file,'r') as f:
	current_gene = ""
	current_transcript = ""
	for line in f:
		tag, value = line.rstrip("\n").split("\t")
		if(tag == "G"):
			current_gene = value
			g2r_dict[value] = {}
		elif(tag == "T"):
			current_transcript = value
			g2r_dict[current_gene][value] = 0
		elif(tag == "R"):
			g2r_dict[current_gene][current_transcript]+=1
		else:
			raise ValueError("Wrong format")


with open(out_file,"w") as out:
	for gene in sorted(g2r_dict, key = lambda x: sum(el for el in g2r_dict[x].values)):
		out.write(gene + "\t" + str(sum(el for el in g2r_dict[gene].values)) + "\n")
		for tran,value in g2r_dict[gene].items():
			out.write(tran + "\t" + str(value) + "\n")