import sys
import os
import sqlite3
import fnmatch

def build_db(vcf,db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    A="CREATE TABLE SVDB (chr TEXT, pos INT,alt TEXT)"
    c.execute(A)

    exac_db=[]
    for line in open(vcf):
        if line[0] == "#":
            continue
        content=line.strip().split()

        chr=content[0]
        pos=content[1]
        ref=content[3]
        alt=content[4]

        exac_db.append([ chr, pos , alt ])

        if len(exac_db) > 100000:
            c.executemany('INSERT INTO SVDB VALUES (?,?,?)',exac_db)          
            exac_db=[]

    if exac_db:
        c.executemany('INSERT INTO SVDB VALUES (?,?,?)',exac_db)
                    
    A="CREATE INDEX SNP ON SVDB (chr, pos)"
    c.execute(A)
    conn.commit()

vcf_files=[]
for root, dirnames, filenames in os.walk(sys.argv[1]):
    for filename in fnmatch.filter(filenames, '*.vcf'):
        build_db( os.path.join(sys.argv[1],filename), os.path.join(sys.argv[1], filename.replace(".vcf",".db")  ) )
