# coding=utf-8
import sys


def trimm_fasta(fasta_file, nb_bases):
    fasta = {}
    seq = ""
    acc = ""
    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.rstrip("\n")
            if(line[0] == ">"):
                if(seq != ""):
                    if(len(seq) > nb_bases * 3):
                        print(acc)
                        print(seq[nb_bases:-nb_bases])
                    seq = ""
                acc = line
            else:
                seq += line
        if(len(seq) > nb_bases * 3):
            print(acc)
            print(seq[nb_bases:-nb_bases])
    return(fasta)


fasta = trimm_fasta(sys.argv[1], int(sys.argv[2]))
