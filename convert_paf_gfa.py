#coding=utf-8
import paf2gfa
import sys
file = open(sys.argv[1],'r')
out  = open(sys.argv[2],'w')



p = paf2gfa.Parser()

p.parse_lines("".join(file.readlines()).split("\n"))

file.close()
out.write(p.get_gfa())
out.close()