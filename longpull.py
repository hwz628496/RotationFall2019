# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 12:31:52 2019

@author: hwz62
"""

def buildlist(handle):
    #pull PMCID's from PMID's
    from Bio import Medline 
    pmcidh=[]
    pmidh2=[]
    #handle=open("hfall.txt")
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
    pmclen=len(pmcidh)
    urlxml=[[""] for i in range(pmclen)]
    for i in range(pmclen):
        url="https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmcids="+pmcidh[i]
        try:
            response=requests.get(url, timeout=3)
            if response.status_code==200:
                urlxml[i]=response.text
        except:
            print(pmcidh[i])
            pmcid_fail.append(pmcidh[i])
            continue
    
    global pmcid2pmid
    pmcid2pmid = dict(zip(pmcidh, pmidh2))
    return pmcid_fail,urlxml,pmcid2pmid,pmidh2

pmcid_fail,urlxml,pmcid2pmid,pmid_list=buildlist()

import re

#disease_regex=re.compile('<infon key="type">Disease<\/infon><location length="[0-9]+" offset="[0-9]+"\/><text>(.+?)<\/text>')

mesh_regex=re.compile('MESH:(D\d+)')
meshterms=[]
for i in range(len(urlxml)):
    mesh=mesh_regex.findall(urlxml[i])
    for j in mesh:
        meshterms.append(j)

disease_regex=re.compile('<infon key="type">Disease<\/infon><location length="[0-9]+" offset="[0-9]+"\/><text>(.+?)<\/text>')
diseaseterms=[]
for i in range(len(urlxml)):
    mesh=disease_regex.findall(urlxml[i])
    for j in mesh:
        diseaseterms.append(j)

from collections import Counter
outkeys=Counter(meshterms).keys()
outvalues=Counter(meshterms).values()
Counter(meshterms).most_common(20)

meshFile = 'd2020.bin'
with open(meshFile, mode='rb') as file:
    mesh = file.readlines()