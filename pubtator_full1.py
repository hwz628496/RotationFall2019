# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 13:06:14 2019

@author: Henry

A list of pmcid's has been built. Send these through pubtator and scrape
annotated fulltexts.

url example: 
    https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmcids=PMC6690576
"""

import requests
pmcid_fail=[""]

urlxml=[""]*150
for i in range(150):
    url="https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmcids="+pmcid[i]
    try:
        response=requests.get(url, timeout=1)
        if response.status_code==200:
            urlxml[i]=response.text
    except:
        print(pmcid[i])
        pmcid_fail.append(pmcid[i])
        continue

for f in range(150):
    filename=pmid2[f]+'.txt'
    with open(filename,'w', encoding="utf-8") as fo:
        fo.write(urlxml[f])
