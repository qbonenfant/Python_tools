#coding=utf-8
#############################################################################
#                                                                           #
# Associate reads to genes from a mapping on reference transcriptome        #
# Works only for ENSEMBL formated cDNA database                             #
#                                                                           #
#                                                                           #
#                                                                           #
#                                                                           #
#       Version: 0.3                                                        #
#       Author: Quentin Bonenfant                                           #
#               quentin.bonenfant@gmail.com                                 #
#############################################################################

import pysam
import sys
import os
from collections import defaultdict as dd

SEP = "\t"  # separator


def sam2graph(sam):
    """ Use BAM/SAM file to convert mapping into a ref / read dictionnary"""

    # storing gene/reads in default dictionnary, using set as factory.
    mapping_dict = dd(set)
    # using pysam to go through sam/bam files
    with pysam.AlignmentFile(sam) as samfile:
        for read in samfile.fetch():

            if(not read.flag & 4  ):
                # Fetching read and reference names
                targetName = read.query_name
                refName = read.reference_name
                mapping_dict[refName].add(targetName)

    return(mapping_dict)


def parseFasta(fastaFile):
    """Go through an ENSEMBL transcriptome fasta file
    and associate transcript accession to gene accession"""
    fasta = dd(set) # associate a gene to a set of transcripts
    with open(fastaFile, 'r') as f:
        for line in f:
            if ">" == line[0]:
                data = line[1:].split()
                transcript_acc = data[0]
                gene_acc = data[3].split(":")[1]
                fasta[gene_acc].add(transcript_acc)
                # not storing sequences
    return(fasta)

if(len(sys.argv) != 3 ):
    print("USAGE: sam2G2R FASTAFILE(ref) SAMFILE(mapping)" )
    print("OUTFILE ARE GENERATED IN THE SAME PATH AS SAMFILE")
    exit()


fastaFile = sys.argv[1]
samFile = sys.argv[2]

# parsing fasta
print("PARSING FASTA")
fasta = parseFasta(fastaFile)
# parsing sam
print("PARSING SAM/BAM")
mapping_dict = sam2graph(samFile)
#risky way to remove ".sam" extension
filePath = os.path.basename(samFile)[:-4] 
# appending our own extension
filePath += "_gene2readlist.txt"

out = open( filePath , "w")
print("OUTPUT FILE:")
print(filePath)
print("PROCESSING")
for gene in fasta.keys():    
    gene_block = "G" + SEP + gene + "\n"
    trans_block = ""
    print_gene = False # should we print the gene ? be printed ?
    for trans in fasta[gene]:
        try:
            # try to fetch reads mapped to this transcript
            reads = mapping_dict[trans]
            if(len(reads)<1):
                raise KeyError
        except KeyError:
            # this will often not be the case, so pass if nothing is associated
            pass
        else:
            trans_block += "T" + SEP + trans + "\n"
            print_gene = True #Yes, reads are associated
            for read in reads:
                trans_block += "R" + SEP + read + "\n"
    if(print_gene):
        out.write(gene_block)
        out.write(trans_block)

out.close()
