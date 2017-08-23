import sys
import numpy
import sqlite3
import fnmatch
import os
import random
#
repeat_distances={}
first=True
for line in open(sys.argv[1]):
	if first:
		first=False
		continue
	content=line.strip().split()
	if not content[0] in repeat_distances:
		repeat_distances[content[0]]=[]
	repeat_distances[content[0]].append(int(content[-1]))

chromosomes=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","X"]

n=10000
first=True
for line in open(sys.argv[2]):
	content=line.split("\t")
	pval=0
	if first:
		print line.strip()
		first=False
		continue

	junctions=int(content[3])
	avg=float(content[1])

		
	selected_chr=numpy.random.choice(chromosomes,n)
	for chromosome in selected_chr:
		dist=selected_chr=numpy.random.choice(repeat_distances[chromosome],junctions)
		if numpy.average(dist) <= avg:
			pval+=1
	pval=float(pval)/n
	print line.strip()+"\t"+str(pval)
