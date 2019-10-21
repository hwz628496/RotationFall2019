# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 12:55:53 2019

@author: Henry

PMChand_medline.txt was made by c/p list of PMID's into PubMed and downloading
it as the MEDLINE file.
"""

"""
#Read in hand-curated PMID's
PMhand=['']*52
f=open('PMChand.txt','r')
for i in range(52):
    PMhand[i]=f.readline()
f.close()
"""

#pull PMCID's from PMID's
from Bio import Medline 
pmcidh=[]
pmidh2=[]
handle=open("PMChand_medline.txt")
records = Medline.parse(handle)
for rec2 in records:
    try:
        pmci=rec2['PMC']
        pmcidh.append(pmci)
        pmidh2.append(rec2["PMID"])
    except:
        continue
handle.close()

#Query PubTator
import requests
pmcid_fail=[]

urlxml=[""]*52
for i in range(52):
    url="https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmcids="+pmcidh[i]
    try:
        response=requests.get(url, timeout=3)
        if response.status_code==200:
            urlxml[i]=response.text
    except:
        print(pmcidh[i])
        pmcid_fail.append(pmcidh[i])
        continue
    
pmcid2pmid = dict(zip(pmcidh, pmidh2))