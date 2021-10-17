# coding=utf-8
import sys
from collections import defaultdict as dd

"""
Compute and display basic statistics of len distribution in a fasta file.
Example in comments
"""

# #-------------------- GLOBAL STATISTICS -------------------#
# N50 size= 1885  number= 363907
# N80 size= 1238  number= 770249
# N90 size= 955  number= 959768
# Assembly size= 2074348139 number= 1256967 minSize= 5 maxSize= 135118 averageSize= 1650.28
# #----------------------------------------------------------#
# #-------------------- SIZE REPARTITION --------------------#
# Size= >= 100000   Number= 10         (0.00)   CumulativeSize= 1130965         (0.05)
# Size= >= 50000    Number= 41         (0.00)   CumulativeSize= 3288080         (0.16)
# Size= >= 10000    Number= 371        (0.03)   CumulativeSize= 9314883         (0.45)
# Size= >= 5000     Number= 9167       (0.73)   CumulativeSize= 60075681        (2.90)
# Size= >= 1500     Number= 605002     (48.13)  CumulativeSize= 1432438255      (69.05)
# Size= >= 1000     Number= 929372     (73.94)  CumulativeSize= 1837194539      (88.57)
# Size= >= 500      Number= 1207631    (96.07)  CumulativeSize= 2055774370      (99.10)
# Size= >= 0        Number= 1256967    (100.00) CumulativeSize= 2074348139      (100.00)
# #----------------------------------------------------------#
# #-------------------- BASE COMPOSITION --------------------#
# NumberOfN=  (0%) NumberOfGC= 981684747 (47.32%)
# #----------------------------------------------------------#

line_sep = "#----------------------------------------------------------#"
global_format = "Assembly size= {} number= {} minSize= {} maxSize= {} averageSize= {}"
nx_format = "N{} size= {} \t number= {}"
size_format = "Size= >= {}\tNumber= {}\t({})\tCumulativeSize= {}  \t({})"
basecompo_format = "# NumberOfN= {}\t({}%)\tNumberOfGC= {}\t({}%)"


number_of_bases = 0
number_of_gc = 0
number_of_n = 0
number_of_seq = 0
size_aray = []
size_classes = [100000, 50000, 10000, 5000, 1500, 1000, 500, 0]
size_distri = dd(list)


# Manually parsing fasta.... cause why not ?
with open(sys.argv[1]) as fastaFile:
    firstLine = True
    seq = ""  # current sequence
    for line in fastaFile:
        line = line.rstrip("\n")
        if(line[0] == ">"):
            number_of_seq += 1
            if(not firstLine):
                # global stats
                ln = len(seq)
                size_aray.append(ln)
                number_of_bases += ln
                # size distribution
                for classe in size_classes:
                    if(ln >= classe):
                        size_distri[classe].append(ln)
                # base composition
                number_of_n += seq.upper().count("N")
                # GC
                number_of_gc += seq.upper().count("G")
                number_of_gc += seq.upper().count("C")
                seq = ""
            else:
                firstLine = False

        else:
            seq += line
    ln = len(seq)
    size_aray.append(ln)
    number_of_bases += ln
    # size distribution
    for classe in size_classes:
        if(ln >= classe):
            size_distri[classe].append(ln)
    # base composition
    number_of_n += seq.upper().count("N")
    # GC
    number_of_gc += seq.upper().count("G")
    number_of_gc += seq.upper().count("C")


# print(len(size_aray))
# Computing N50,80,90
nxx = {50: 0, 80: 0, 90: 0}
nxxn = {50: 0, 80: 0, 90: 0}
rs_size_array = sorted(size_aray)[::-1]

n = 0
for i, l in enumerate(rs_size_array):
    for nx in nxx.keys():
        if(n >= number_of_bases * float(nx / 100) and nxx[nx] == 0):
            nxx[nx] = l
            nxxn[nx] = i
    n += l

# global stats
avg_size = round(float(number_of_bases / number_of_seq), 2)
max_size = max(size_aray)
min_size = min(size_aray)

# DISPLAY
print(sys.argv[1])
print("#-------------------- GLOBAL STATISTICS -------------------#")
for nx in nxx.keys():
    print(nx_format.format(nx, nxx[nx], nxxn[nx]))
print(global_format.format(number_of_bases, number_of_seq, min_size, max_size, avg_size))
print(line_sep)

print("#-------------------- SIZE REPARTITION --------------------#")
for size in reversed(sorted(size_distri.keys())):
    size_prop = round(len(size_distri[size]) / float(number_of_seq) * 100, 2)
    size_cumul_prop = round(sum(size_distri[size]) / float(number_of_bases) * 100, 2)
    print(size_format.format(size, len(size_distri[size]), size_prop, sum(size_distri[size]), size_cumul_prop))
print(line_sep)

print("#-------------------- BASE COMPOSITION --------------------#")
n_number_prop = round(number_of_n / float(number_of_bases) * 100, 2)
gc_number_prop = round(number_of_gc / float(number_of_bases) * 100, 2)

print(basecompo_format.format(number_of_n, n_number_prop, number_of_gc, gc_number_prop))
print(line_sep)
