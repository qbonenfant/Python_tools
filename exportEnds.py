# coding=utf-8
# Export the ends of the sequences from a FASTA file.
# The middle is also exported to generate a negativ control
# Short sequences (< 500) will not ne exported
import sys

fileName = ".".join(sys.argv[1].split("/")[-1].split(".")[:-1] + ["fasta"])
path = "/".join(sys.argv[1].split("/")[:-1])
path = "./"
size = int(sys.argv[2])

nbExported = 0
nbRejected = 0

with open(sys.argv[1], "r") as f:

    # Preparing out file
    st = open(path + "/start_" + fileName, "w")
    md = open(path + "/middle_" + fileName, "w")
    ed = open(path + "/end_" + fileName, "w")
    ident = ""
    sequence = ""
    # Starting to read
    for line in f:
        if(line[0] == ">"):
            if(sequence != ""):
                lSeq = len(sequence)
                if(lSeq >= 500):
                    nbExported += 1
                    mid = lSeq // 2
                    start = sequence[:size]
                    middle = sequence[mid - (size // 2):mid + (size // 2)]
                    end = sequence[-(size + 1):]
                    st.write(ident + "_start\n" + start + "\n")
                    md.write(ident + "_middle\n" + middle + "\n")
                    ed.write(ident + "_end\n" + end + "\n")
                else:
                    nbRejected += 1
                sequence = ""
            ident = ">" + "_".join(line[1:].split("_")[0:2])
        else:
            sequence += line.rstrip('\n')
    lSeq = len(sequence)
    if(lSeq >= 500):
        nbExported += 1
        mid = lSeq // 2
        start = sequence[:size]
        middle = sequence[mid - (size // 2):mid + (size // 2)]
        end = sequence[-(size + 1):]
        st.write(ident + "_start\n" + start + "\n")
        md.write(ident + "_middle\n" + middle + "\n")
        ed.write(ident + "_end\n" + end + "\n")
    else:
        nbRejected += 1
    st.close()
    md.close()
    ed.close()
print("Number of accepted sequences (>=500): " + str(nbExported))
print("Number of rejected sequences (<500) : " + str(nbRejected))
