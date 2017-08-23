import sys
import numpy
import sqlite3
import fnmatch
import os
import random
#
def load_fasta(fafile):
    sequence={}
    chromosome_order=[]
    #read the fast file 
    with open(fafile, 'r+') as f:
        reference = f.read()
    split_reference=reference.split(">")
    del reference
    del split_reference[0]
    #store the reference as a dictionary
    chromosome_len={}
    chromosomes=[]
    simulated_bases=0
    for chromosome in split_reference:
        content=chromosome.split("\n",1)
        sequence[content[0].split()[0]]=content[1].replace("\n","")
        chromosome_order.append(content[0].split()[0])
    del split_reference
    return(sequence,chromosome_order)

def compute_homology_len(ref_seq,posA,posB):
    hom_len = 0
    direction_A=random.randint(0, 1)
    direction_B=random.randint(0, 1)
    while True:
        base_A=ref_seq[posA]
        base_B=ref_seq[posB]
        if base_A == "N" or base_B == "N":
            hom_len = -1
            break

        elif base_A == base_B:
            hom_len += 1
            if direction_A:
                posA +=1
            else:
                posA +=-1
            if direction_B:
                posB += 1 
            else:
                posB +=-1
        else:
            break

    return hom_len

conn=sqlite3.connect(sys.argv[1])
c=conn.cursor()

chromosomes=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","X"]
reference,order=load_fasta(sys.argv[1])
contig_sizes={}
for contig in reference:
	contig_sizes[contig.replace("chr","")]=len(reference[contig])

n=100000

first=True
for line in open(sys.argv[2]):
	content=line.split("\t")
	pval=0
	if first:
		print line.strip()
		first=False
		continue

	junctions=int(content[8])
	total_hom=int(content[4])*int(content[5])

		
	selected_chr=numpy.random.choice(chromosomes,n)
	for chromosome in selected_chr:
		dist=[]
		maxima=contig_sizes[chromosome]
		minima=1
		while True:
			pos_list=numpy.random.randint(low=minima,high=maxima,size=2)
			d=compute_homology_len(reference[chromosome],pos_list[0],pos_list[1])
			if d > -1:
				dist.append(d)
			if len(dist) == junctions:
				break
		if sum(dist) >= total_hom:
			pval+=1
	pval=float(pval)/n
	print line.strip()+"\t"+str(pval)


