#coding=utf-8
from random import randint
import sys


def genSeq(size,alphabet):
	seq = ""
	max_range = len(alphabet)-1
	for i in range(size):
		seq+=alphabet[randint(0,max_range)]
	return(seq)


if(len(sys.argv<3)):
	print("Usage: gen_rand_seq size alphabet [nb sequence]")
	exit()

size = int(sys.argv[1])
alpha = sys.argv[2]
nb = sys.argv[3] if len(sys.argv)>=4 else 1
for i in range(nb):
	print(">Sequence_" + str(i))
	print(genSeq(size,alpha))

## older version calculated kmer occurence esperance
# k = 10
# seqSize = 2000
# totNbK = seqSize - k + 1
# print("Kmer Esperance = " + str(totNbK * ( 1- (4**k - 1)**totNbK / ((4**k)**totNbK)  )))
