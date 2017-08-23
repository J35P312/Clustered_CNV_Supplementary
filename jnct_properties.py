import sys
import numpy

data={}
for line in open(sys.argv[1]):
    content=line.split("\t")
    sample=content[0]
    repeat_dist_a=content[9]
    repeat_dist_b=content[11]
    micro_homology=content[12]
    insert=content[14]

    if not sample in data:
        data[sample]={}
        data[sample]["MH"]=[]
        data[sample]["INST"]=[]
        data[sample]["RD"]=[]
        data[sample]["junctions"]=0
        data[sample]["snps"]=0

    try:
        data[sample]["MH"].append(int(micro_homology))
    except:
        pass

    try:
        data[sample]["INST"].append(int(insert))
    except:
        pass

    try:
        data[sample]["RD"].append(int(repeat_dist_a))
    except:
		pass
    try:
        data[sample]["RD"].append(int(repeat_dist_b))
    except:
        pass
    data[sample]["junctions"]+=1

    snps=content[16].split("|")
    pos=int(content[3])
    for snp in snps:
        if "none" in snp:
            continue 
        distance=int(snp.split("-")[1])
        if abs(distance-pos) < 1000:
            data[sample]["snps"]+=1
    
    snps=content[18].split("|")
    if not content[4] == "NA":
        pos=int(content[4])
        for snp in snps:
            if "none" in snp:
                continue 
            distance=int(snp.split("-")[1])
            if abs(distance-pos) < 1000:
                data[sample]["snps"]+=1

print "sample\t#avg_repeat_distance\trepeats_within_1kb\tbps\tavg_MH_len\tMH_jnct\tavg_insert_len\tinsert_jnct\ttotal_jnct\tsnps_within_1kb"
for sample in data:
    AVG_RD=numpy.average(data[sample]["RD"])
    RDH=0
    for i in data[sample]["RD"]:
        if i <= 1000:
            RDH +=1
    bps=len(data[sample]["RD"])
    avgMH=0
    nMH=0
    MH_vector=[]
    for i in data[sample]["MH"]:
        if i > 0:
            avgMH+=i
            nMH+=1
    if nMH:
        avgMH=avgMH/nMH
    else:
        avgMH=0
        
    avgINS=0
    nINS=0
    for i in data[sample]["INST"]:
        if i > 0:
            avgINS+=i
            nINS+=1
    if nINS:
        avgINS=avgINS/nINS	
    else:
        avgINS=0
    print "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(sample,AVG_RD,RDH,bps,avgMH,nMH,avgINS,nINS,data[sample]["junctions"],data[sample]["snps"])
