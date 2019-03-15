#coding = UTF-8
# print out the gene ids from a fasta / fastq file

import sys


fileName = sys.argv[1]
form = fileName.split(".")[-1]

with open(fileName, 'r') as f:

	symbol = "$"
	if(form == "fasta" or form == "fa"):
		symbol = ">"
	elif(form == "fastq" or form == "fq"):
		symbol = "@"
	for line in f:
		if symbol == line[0]:
			#print(line[1:].rstrip("\n"))
			print(line[1:].split(" ")[0])