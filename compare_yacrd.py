# coding=utf-8
# Compare the output from YACRD to a read list.


import sys

yacrd_file = sys.argv[1]
read_file = sys.argv[2]

# parsing yarcd file
chimeric_yarcd = set()
with open(yacrd_file) as f:
    for line in f:
        line = line.rstrip("\n")

        data = line.split("\t")
        if(data[0] == "Chimeric"):
            chimeric_yarcd.add(data[1])

# Parsing readlist
chimeric_reads = set()
with open(read_file) as f:
    for line in f:
        line = line.rstrip("\n")
        # one read per line, not fields to split
        chimeric_reads.add(line)


commons = chimeric_reads & chimeric_yarcd
only_list = chimeric_reads - commons
only_yacrd = chimeric_yarcd - commons
total = chimeric_yarcd | chimeric_reads

print("Total number of chimeric", len(total))
print("Common reads between yacrd and the readlist", len(commons))
print("Reads only in the readlist", len(only_list))
print("Reads only in the yarcd results", len(only_yacrd))
