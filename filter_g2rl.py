# coding=utf-8
# Remove duplicate entry from G2RL files
import sys
tagFile = sys.argv[1]
tagflag = "G"

current_set = set()
current_cl = ""
with open(tagFile) as f:
    for line in f:
        data = line.rstrip("\n").split("\t")
        if(data[0] == tagflag):
            if(current_cl != ""):
                print("G " + current_cl)
                print("\n".join("R " + el for el in current_set))
                current_set = set()
            current_cl = data[1]
        elif(data[0] == "R"):
            current_set.add(data[1])
    print("G " + current_cl)
    print("\n".join("R " + el for el in current_set))
