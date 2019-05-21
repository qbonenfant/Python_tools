#coding = utf-8
#count the number of sequences which length is lower than the required threshold.
import sys

lim = int(sys.argv[2])
seq = ""
nb = -1 # init value, will be set to 0 when reading first line
tot = 0
acc = ""
with open(sys.argv[1]) as f:
	for line in f:
		if(line[0]==">"):
			tot+=1
			if(len(seq)<=lim):
				nb+=1
				#print(acc)
			seq = ""
			acc = line
		else:
			seq += line.rstrip("\n")
print(nb,tot,sep = "/")