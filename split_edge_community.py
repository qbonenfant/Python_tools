# coding=utf-8
# Split an edge file in several files containing nodes
# that share the same community
# Format are .edge for edge input and g2rl for partition.
import sys
import os
import subprocess


g2rfile = sys.argv[1]
edge_file = sys.argv[2]

##############################################################################
# Before parsing edge file, we make a tmp folder
if(not os.path.isdir("./tmp")):
    print("Making a tmp folder. Communities will be stored there")
else:
    # If there is a tmp folder, erase it
    print("I need a tmp folder to store communities.")
    print("But there already is a TMP folder here.")
    print("Should I erase it ? (y/n)")
    inp = ""
    while(inp != "y" and inp != "n"):
        inp = input()
        if(inp != "y" and inp != "n"):
            print("Pleaser enter y or n .")
    if(inp == "y"):
        tmpDir = os.path.dirname("./tmp/")
        command = "rm -r " + tmpDir
        try:
            subprocess.check_call(command.split())
        except SystemError as e:
            print("SOMETHING WENT WRONG!", file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit("ERROR: approximate k-mer count failed")
        else:
            print("tmp folder emptied!")

    else:
        print("I need a tmp folder")
        print("Please rename or move current tmp folder")
        print("then relaunch.")
        exit(0)
os.mkdir("./tmp")

##############################################################################
# Fetching communities from G2R file
community = {}
with open(g2rfile) as f:
    current_community = ""
    for line in f:
        line = line.rstrip("\n")
        tag, element = line.split("\t")

        if(tag == "R"):
            community[element] = current_community
        else:
            current_community = element

##############################################################################
# Going through the edge file, testing edges
with open(edge_file) as f:
    current_source = ""
    current_community = ""
    # current output file
    current_file = None
    filepath = "./tmp/cluster_{}.edges"
    for line in f:
        line = line.rstrip("\n")
        data = line.split("\t")
        if(len(data) > 2):
            read1 = data[0]
            read2 = data[2]
            # Limit the number of check in community dict
            # and file I/O
            if(read1 != current_source):
                current_source = read1
                current_community = community[read1]
                # Closing, if required
                if(current_file is not None):
                    current_file.close()
                # Opening
                current_file = open(filepath.format(current_community), "a+")

            tgt_community = community[read2]
            # If the edge is in the same community as source,
            # then print the edge in the cluster file
            if(current_community == tgt_community):
                current_file.write(line+"\n")
