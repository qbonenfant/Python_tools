# coding=utf8
# Filter ENSEMBL fasta using metadata, rejecting reads fitting the filter


import sys
import os


def parse_ensembl_fasta(fasta_file):
    fasta = {}
    with open(fasta_file) as f:
        current_element = {}
        sequence = ""
        for line in f:
            if(line[0] == ">"):
                current_element["sequence"] = sequence
                sequence = ""
                data = line[1:].rstrip("\n").split()
                fasta[data[0]] = {}
                current_element = fasta[data[0]]
                # data[7] = " ".join(data[7:])

                for element in data[2:7]:
                    sub_elements = element.split(":")
                    current_element[sub_elements[0]] = ":".join(
                        sub_elements[1:])

            else:
                sequence += line.rstrip("\n")
        current_element["sequence"] = sequence
    return(fasta)
