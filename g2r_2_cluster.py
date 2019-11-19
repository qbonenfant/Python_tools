#coding=utf-8

import sys
from collections import defaultdict as dd

tagfile = sys.argv[1]
tagflag = sys.argv[2]
clusters = dd(list)
with open(tagfile) as f:
	current_commu = ""
	for line in f:
		data = line.rstrip("\n").split()
		if(data[0] == tagflag):
			current_commu = data[1]
		elif(data[0] == "R"):
			clusters[current_commu].append(data[1])

for commu in clusters.values():
	print("\t".join(commu))