# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 14:51:15 2019

@author: Henry
"""

import timeit
import requests

urlstr1="https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmids=31490396"
urlstr="31490396"
for i in range(1,100):
    urlstr=urlstr+","+pmid[i]
urlstr2="https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmids="+urlstr

import timeit
import requests

start = timeit.timeit()
for i in range(100):
    print(pmid[i])
    response=requests.get("https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmids="+pmid[i], timeout=0.1)
end = timeit.timeit()
print(end - start)


start = timeit.timeit()
urlstr="31490396"
for i in range(1,100):
    print(pmid[i])
    urlstr=urlstr+","+pmid[i]
urlstr2="https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmids="+urlstr
response=requests.get(urlstr2, timeout=0.1)
end = timeit.timeit()
print(end - start)