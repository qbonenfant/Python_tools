# coding=utf-8
# Trimm the the ends of all sequences from a multi-fasta file
# usage: trimm_ends <fasta> <nb_base>
# The sequence need to ne at least nb_base * 3 long to be cut.
import sys
from Bio import SeqIO


def trimm_fasta(fasta_file, nb_bases, extension):
    for record in fasta_file:
        if(len(record) > nb_bases * 3):
            record = record[nb_bases:-nb_bases]
            print(record.format(extension), end="")


infile = sys.argv[1]
extension = infile.split(".")[-1]

records = SeqIO.parse(infile, extension)
trimm_fasta(records, int(sys.argv[2]), extension)
