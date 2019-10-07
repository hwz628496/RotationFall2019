# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 16:24:04 2019

@author: Henry

https://www.ncbi.nlm.nih.gov/research/pubtator/api.html

Send PMID through PubTator Central and find annotated texts

Structure of API query:
https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/[Format]?[Type]=[Identifiers]&concepts=[Bioconcepts]

Example: https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmids=31411269
"""

from Bio import Medline 

handle=open("pubmed_result2.txt")
records = Medline.parse(handle)
pmid = [rec['PMID'] for rec in records]
handle.close()

pmcid=[""]
pmid2=[""]
handle=open("pubmed_result2.txt")
records = Medline.parse(handle)
for rec2 in records:
    try:
        pmci=rec2['PMC']
        pmcid.append(pmci)
        pmid2.append(rec2["PMID"])
    except:
        continue
handle.close()


#for r in records:
#    print(r['TI'])
#    if r['PMID']=="31411269":
#        print(r['PMC'])
        
        

urlstrs=[""]*len(pmid)

for i, urls in enumerate(pmid):
    urlstrs[i]="https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmids="+urls



import requests
pmid_fail=[""]

urlxml=[""]*len(urlstrs)
for i, url in enumerate(urlstrs):
    try:
        response=requests.get(url, timeout=0.5)
        if response.status_code==200:
            urlxml[i]=response.text
    except:
        print(pmid[i])
        pmid_fail.append(pmid[i])
        continue

fo=open('pmcodepairs.txt','w')
for i in range(15687):
    fo.write(pmid2[i]+' '+pmcid[i])
    fo.write('\n')
fo.close()