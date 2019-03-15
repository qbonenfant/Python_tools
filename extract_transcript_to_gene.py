#coding=utf-8
import sys
import re
from collections import defaultdict as dd
gene_rule = re.compile(r">(ENSMUST\d+\.?\d+).*gene\:(ENSMUSG\d+\.?\d+).*\n")

gene_dict = dd(list)

with open(sys.argv[1]) as f:
	for line in f:
		if(line[0] == ">"):
			elements = gene_rule.match(line)
			gene_dict[elements.group(1)].append(elements.group(2))

for gene, transcripts in gene_dict.items():
	print("G\t" + gene)
	for t in transcripts:
		print("T\t" + t)
