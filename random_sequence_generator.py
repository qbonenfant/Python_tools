# coding=utf-8
from random import randint
import sys


max_var = 0.10
min_len = 300
nb_seq = int(sys.argv[1])
size = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
alpha = sys.argv[3] if len(sys.argv) > 3 else "ATCG"


def genSeq(size, alphabet):
    seq = ""
    a_len = len(alphabet) - 1
    for i in range(size):
        seq += alphabet[randint(0, a_len)]
    return(seq)


if(len(sys.argv) < 2):
    print("Usage: gen_rand_seq nb_sequence [size] [alphabet]")
    exit()

offset = round(max_var * size / 2.0)

for i in range(nb_seq):
    r_size = randint(size - offset, size + offset)
    r_size = max(r_size, min_len)
    print(">Sequence_" + str(i))
    print(genSeq(r_size, alpha))
