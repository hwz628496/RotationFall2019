# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 15:56:48 2019

@author: Henry

Scrapes MEDLINE citations from pubmed_result2.txt 
"""

from Bio import Medline 

handle=open("pubmed_result2.txt")
records = Medline.parse(handle)
pmid = [rec['PMID'] for rec in records]

handle.close()

for r in records:
    print(r['TI'])
    if r['PMID']=="31411269":
        print(r['PMC'])