# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 13:33:41 2019

@author: Henry

Compiled code from both handscrape.py and xmlparse2.py
"""

def buildlist():
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
    
    global pmcid2pmid
    pmcid2pmid = dict(zip(pmcidh, pmidh2))
    return pmcid_fail,urlxml,pmcid2pmid

pmcid_fail,urlxml,pmcid2pmid=buildlist()

#chop off non-annotated chunks from pubtator docs
import re
urlxml_original=urlxml;
abstract=re.compile('<passage>.+?<infon key="section_type">.+?<\/infon><infon key="type">abstract<\/infon><offset>[0-9]+<\/offset><text>.+?<\/passage>')
for i, xmldoc in enumerate(urlxml):
    urlxml[i]=re.sub(abstract,'',xmldoc);

title=re.compile('<passage>.+?<infon key="section_type">TITLE<\/infon>.+?<\/passage>')
for i, xmldoc in enumerate(urlxml):
    urlxml[i]=re.sub(title,'',xmldoc);

ref=re.compile('<infon key="section_type">REF<\/infon>.+?<\/passage>')
for i, xmldoc in enumerate(urlxml):
    urlxml[i]=re.sub(ref,'',xmldoc);

table=re.compile('<passage><infon key="section_type">TABLE</infon>.+?<\/passage>')
for i, xmldoc in enumerate(urlxml):
    urlxml[i]=re.sub(table,'',xmldoc);

#ref2=re.compile('<passage>*+?<infon key="section_type">REF<\/infon>.+?<\/passage>')
#for i, xmldoc in enumerate(urlxml):
#    urlxml[i]=re.sub(ref2,'',xmldoc);

#xmldoc=urlxml[0]


def find_lists(xmldoc):
    import re
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
    return pubtator_list,handlist

#pubtator_list,handlist=find_lists(urlxml[0])

def fone(pubtator_list,handlist):
    from collections import Counter
    c1 = Counter(pubtator_list)
    c2 = Counter(handlist)
    intersect=c1&c2
    precision=(sum(intersect.values()))/sum(c1.values())
    recall=(sum(intersect.values()))/sum(c2.values())
    try:
        f_one=(2*precision*recall)/(precision+recall)
    except:
        f_one=0
    return f_one

def clean(diseaselist):
    cleanlist=[""]*len(diseaselist)
    for i in range(len(diseaselist)):
        diseaselist[i]=diseaselist[i].rstrip('\n')
        cleanlist[i]=diseaselist[i].lower()
    return cleanlist

fone_list=[None]*52
for i in range(52):
    pubtator_list,handlist=find_lists(urlxml[i])
    pubtator_list=clean(pubtator_list)
    handlist=clean(handlist)
    fone_list[i]=fone(pubtator_list,handlist)