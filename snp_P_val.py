import sys
import numpy
import sqlite3
import fnmatch
import os
import random
#vcf db, snps, reakpoints
def retrieve_sample_data(db,chr,start,end):
	snps=0
	A='SELECT pos FROM SVDB WHERE chr == \'{}\' AND pos <= {} AND pos >= {} '.format(chr,end,start)
	for hit in c.execute(A):
		snps+=1
	return(snps)

conn=sqlite3.connect(sys.argv[1])
c=conn.cursor()


chromosomes=[]
for hit in c.execute("SELECT DISTINCT chr FROM SVDB"):
	if hit[0] in ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","X"]:
		chromosomes.append(hit[0])

positions={}
for chromosome in chromosomes:
	for hit in c.execute("SELECT MIN(pos) FROM SVDB WHERE chr ==  \'{}\'".format(chromosome)):
		minima=int(hit[0])+1000
	for hit in c.execute("SELECT MAX(pos) FROM SVDB WHERE chr ==  \'{}\'".format(chromosome)):
		maxima=int(hit[0])-1000
	positions[chromosome]=[minima,maxima]
pval=0

n=50000

for i in range(0,n):
	snps=0
	for k in range(0,int(sys.argv[3])):
		chromosome=random.choice(chromosomes)
		maxima=positions[chromosome][1]
		minima=positions[chromosome][0]
		pos=random.randint(minima,maxima)
		snps += retrieve_sample_data(c,chromosome,pos-1000,pos+1000)	
	if snps >= int(sys.argv[2]):
		pval +=1
	p=float(pval)/n


print p
