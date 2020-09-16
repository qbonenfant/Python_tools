# coding=utf-8
# Convert G2Rl files to tabbed asociation file
# Classes marker are given by the tagFlag value
# and element by elemFlag
import sys

if(len(sys.argv) < 2 or len(sys.argv) > 4):
    print("USAGE: g2r_2_assoc.py <g2r_file> [tag_flag] [elem_flag]")

tagfile = sys.argv[1]
tagflag = sys.argv[2] if len(sys.argv) > 2 else "G"
elemflag = sys.argv[3] if len(sys.argv) > 3 else "R"

with open(tagfile) as f:
    current_commu = ""
    for line in f:
        data = line.rstrip("\n").split()
        if(data[0] == tagflag):
            current_commu = data[1]
        elif(data[0] == elemflag):
            print(data[1] + "\t" + current_commu)
