import sys
import numpy
import sqlite3
import fnmatch
import os
import random
#
def distance(chromosome,pos,c):
    d=[]
    delta=10000
    i =0
    while True:
        i +=1
        A='SELECT start,end FROM SVDB WHERE chr == \'{}\' AND start < {} AND end > {}'.format(chromosome,int(pos)+delta,int(pos)-delta)
        #print A
        d=[]
        for hit in c.execute(A):
            d.append( abs(pos- int( hit[0] )) )
            d.append( abs(pos- int( hit[1] )) )
            if pos >= int( hit[0]) and pos <= int( hit[1] ):
                d.append(0)
        if d:
            return( min(d) )
        delta = delta*10


conn=sqlite3.connect(sys.argv[1])
c=conn.cursor()

chromosomes=[]
for hit in c.execute("SELECT DISTINCT chr FROM SVDB"):
	if hit[0] in ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","X"]:
		chromosomes.append(hit[0])

positions={}
for chromosome in chromosomes:
	for hit in c.execute("SELECT MIN(start) FROM SVDB WHERE chr ==  \'{}\'".format(chromosome)):
		minima=int(hit[0])+1000
	for hit in c.execute("SELECT MAX(end) FROM SVDB WHERE chr ==  \'{}\'".format(chromosome)):
		maxima=int(hit[0])-1000
	positions[chromosome]=[minima,maxima]

n=1000000
print "chromosome pos dist"
first=True

selected_chr=numpy.random.choice(chromosomes,n)
for chromosome in selected_chr:
	dist=[]
	maxima=positions[chromosome][1]
	minima=positions[chromosome][0]
	pos=numpy.random.randint(low=minima,high=maxima)
	dist=distance(chromosome,pos,c)
	print "{} {} {}".format(chromosome,pos,dist)
