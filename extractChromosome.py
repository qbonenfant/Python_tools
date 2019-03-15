#coding = utf-8 
# Extract the Id and sequences from an ENSEMBL TRANSCRIPTOME fasta file if the gene is on specific chromosome.
# Create a corresponding FASTA file in the same directory
import sys
import re

file = sys.argv[1]
ch   = sys.argv[2]

ensembleRule = re.compile(r'>ENSMUST\d+\.\d.+chromosome:\w+:(\d+):.*\n')
out = open(".".join(file.split(".")[:-1])+"_ch" + ch +".fasta","w")

with open(file,"r") as f:

	line = f.next()
	while(line != ""):
		ident = line
		found=(ensembleRule.search(ident))
		seq =""
		try:
			line = f.next()
			while(re.search(r"[ATCGUXN]+\n",line)):
				seq+=line
				line = f.next()
			if found and found.group(1) == ch:
				out.write(ident)
				out.write(seq)
		except StopIteration:
			line = ""
out.close()