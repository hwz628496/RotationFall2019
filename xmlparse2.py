# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 14:20:38 2019

@author: Henry

Using regex: format of text is thus:
    
<annotation id="1">
<infon key="Identifier">
MESH:D006391</infon>
<infon key="type">
Disease</infon>
<location length="17" offset="0"/>
<text>
Atrial Hemangioma</text>
</annotation>

First, we get the string from urlxml, find the PMCID.
Then convert from PMCID to PMID using pmcid2pmid dict from handscrape.py
Then open filename PMID.ann and read my hand annotations
Then compare?????

"""

import re

xmldoc=urlxml[0]

#get PMID
pmcidre=re.compile('<id>[0-9]+<\/id>')
pmcidraw=re.findall(pmcidre,xmldoc)

disease_regex=re.compile('<infon key="type">Disease<\/infon><location length="[0-9]+" offset="[0-9]+"\/><text>')

disease_regex=re.compile('<infon key="type">Disease<\/infon><location length="[0-9]+" offset="[0-9]+"\/><text>')
pubtator_list=[]
for disease in disease_regex.finditer(xmldoc):
    counter=0
    string=''
    letter=''
    while letter!='<':
        letter=xmldoc[disease.end()+counter:disease.end()+counter+1]
        string=string+letter
        counter+=1
    pubtator_list.append(string[0:len(string)-1])

#Open hand-annotated documents
pmid=pmcid2pmid['PMC'+pmcidraw[0][4:11]]
filename=pmid+'.ann'
handfile=[]
fo=open('./PMC_sentences/'+filename,'r')
count=0
for line in fo:
    count+=1
    if count%2==1:
        handfile.append(line)
fo.close()

handlist=[]
for i in handfile:
    holder=i.split('\t')
    handlist.append(holder[len(holder)-1])