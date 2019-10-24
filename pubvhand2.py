# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 21:48:53 2019

@author: Henry

Compiled code from both handscrape.py and sentenceadjust2.py
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
    return pmcid_fail,urlxml,pmcid2pmid,pmidh2

pmcid_fail,urlxml,pmcid2pmid,pmid_list=buildlist()

#chop off non-annotated chunks from pubtator docs
import re
urlxml_original=urlxml.copy();
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

def find_lists(xmldoc):
    import re
    #get PMID
    pmcidre=re.compile('<id>[0-9]+<\/id>')
    pmcidraw=re.findall(pmcidre,xmldoc)
    disease_regex=re.compile('<infon key="type">Disease<\/infon><location length="[0-9]+" offset="[0-9]+"\/><text>')
    #disease_regex=re.compile('<infon key="type">Disease<\/infon><location length="[0-9]+" offset="[0-9]+"\/><text>')
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
    handlistloc=[]
    for i in handfile:
        holder=i.split('\t')
        handlist.append(holder[len(holder)-1])
        holder2=holder[1].split()
        handlistloc.append([holder2[1],holder2[2]])
    return pubtator_list,handlist,handlistloc

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
pubtator_group=[None]*52
hand_master=[None]*52
for i in range(52):
    pubtator_list,handlist,handlistloc=find_lists(urlxml[i])
    pubtator_list=clean(pubtator_list)
    handlist=clean(handlist)
    pubtator_group[i]=pubtator_list
    fone_list[i]=fone(pubtator_list,handlist)
    for j in range(len(handlistloc)):
        handlistloc[j].append(handlist[j])
    hand_master[i]=handlistloc


def xmllocs(xmldoc,publist):
    import re
    disease_regex=re.compile('<infon key="type">Disease<\/infon><location length="[0-9]+" offset="[0-9]+"\/><text>')
    re.findall(disease_regex,xmldoc)
    locationstr=re.findall(disease_regex,xmldoc)
    
    locations=[None]*len(locationstr)
    for i in range(len(locationstr)):
        locations[i]=re.findall('\d+',locationstr[i])
    
    parastartre=re.compile('<infon key="type">paragraph<\/infon><offset>(\d+?)<\/offset><text>')
    parastart=int(re.findall(parastartre,xmldoc)[0])
    startgap=int(locations[0][1])-parastart
    
    locations2=[None]*len(locations)
    for i in range(len(locations)):
        locations2[i]=[None]*3
        locations2[i][0]=int(locations[i][1])-int(locations[0][1])+startgap
        locations2[i][1]=int(locations[i][0])+int(locations2[i][0])
        locations2[i][2]=publist[i]
    return locations2

pub_master=[None]*52
for i in range(52):
    pub_master[i]=xmllocs(urlxml[i],pubtator_group[i])
    
    
"""
Start of sentenceadjust2.
"""

def sentenceadjust(xmldoc,xmldoccnt,pmid_list,hand_master,pub_master):
    import re
    
    paragraphre=re.compile('<passage>.+?<infon key="section_type">.+?<\/infon><infon key="type">paragraph<\/infon><offset>[0-9]+<\/offset><text>.+?<\/text>')
    paragraphs=re.findall(paragraphre,xmldoc)
    paragraphs2=[None]*len(paragraphs)
    for i in range(len(paragraphs)):
        holder=re.findall('>.*?<',paragraphs[i])
        paragraphs2[i]=holder[-1][1:(len(holder[-1])-1)]
        
    brattxt=[]
    fo=open('./PMC_sentences/'+pmid_list[xmldoccnt]+'.txt')
    for i in fo:
        brattxt.append(i[:-1])
    fo.close()
       
    bratstr=""
    for i in brattxt:
        bratstr=bratstr+'|'+i
    bratstr=bratstr[1:]
    
    handext=[None]*len(hand_master[xmldoccnt])
    for i in range(len(hand_master[xmldoccnt])):
        holder=[int(hand_master[xmldoccnt][i][0]), int(hand_master[xmldoccnt][i][1]), hand_master[xmldoccnt][i][2]]
        handext[i]=holder
    
    from operator import itemgetter
    handext=sorted(handext, key=itemgetter(0))
    
    adjust=bratstr.count('|',0,int(handext[0][0]))
    for j in range(len(handext)):
        handext[j][0]=int(handext[j][0])-adjust
        handext[j][1]=int(handext[j][1])-adjust
    for i in range(1,len(handext)):
        adjust=bratstr.count('|',int(handext[i-1][0]),int(handext[i][0]))
        for j in range(i,len(handext)):
            handext[j][0]=int(handext[j][0])-adjust
            handext[j][1]=int(handext[j][1])-adjust
    
    titlere=re.compile('<infon key="section_type">.+?<infon key="type">(.+?)<\/infon><offset>(\d+?)<\/offset><text>(.+?)<\/text>')
    titles=re.findall(titlere,xmldoc)
    
    paragraph_list=[]
    for i in range(len(titles)):
        if titles[i][0]=='paragraph':
            paragraph_list.append(i)
    
    difflist=[]
    for i in range(1,len(paragraph_list)):
        difference=int(titles[paragraph_list[i]][1])-int(titles[(paragraph_list[i-1]+1)][1])
        difflist.append(difference)
    
    firstparagraphflag=paragraph_list[0]
    
    difflist2=[]
    for i in range(len(difflist)):
        firstoffset=int(titles[firstparagraphflag][1])
        ticks=int(titles[paragraph_list[i+1]][1])-firstoffset
        diffhold=[ticks,difflist[i]]
        difflist2.append(diffhold)
    
    for i in difflist2[1:]:
        i[1]=i[1]+0
    
    difflist3=[]
    
    for i in range(len(difflist2)):
        totals=0
        for j in range(i+1):
            totals=totals+difflist2[j][1]
        holder=[difflist2[i][0], totals]
        difflist3.append(holder)
    
    difflist3firsts=[i[0] for i in difflist3]
    
    realoffsets=[]
    for i in range(1,len(paragraph_list)):
        realoffsets.append(int(titles[paragraph_list[i]][1])-int(titles[paragraph_list[i-1]][1])-len(titles[paragraph_list[i-1]][2])-1)
    
    realoffsets2=[]
    tally=0
    for i in range(len(realoffsets)):
        tally=tally+realoffsets[i]
        realoffsets2.append(tally)
    difflistdict2=dict(zip(difflist3firsts,realoffsets2))
    
    publistadjust=pub_master[xmldoccnt][:]
    publistadjust2=publistadjust
    for i in range(len(publistadjust)):
        pos=publistadjust[i][0]
        if pos>=difflist3firsts[0]:
            diffdictlookup=max(k for k in difflist3firsts if k<=pos)
            offsetpos=difflistdict2[diffdictlookup]
        else:
            offsetpos=0
        holder=[int(publistadjust[i][0])-offsetpos, int(publistadjust[i][1])-offsetpos, publistadjust[i][2]]
        publistadjust2[i]=holder
    return handext, publistadjust2

handmaster2=[]
pubmaster2=[]
for i in range(len(urlxml)):
    handhold,pubhold=sentenceadjust(urlxml[i],i,pmid_list,hand_master,pub_master)
    handmaster2.append(handhold)
    pubmaster2.append(pubhold)

def fonetwo(publist,handlist):
    pubprobe=[]
    for i in range(len(publist)):
        pubprobe.append(publist[i][0])
    
    handfirst=[]
    for i in range(len(handlist)):
        handfirst.append(handlist[i][0])
    
    fp=0
    success=0
    
    for i in range(len(pubprobe)):
        if pubprobe[i] in handfirst:
            success=success+1
        elif pubprobe[i] not in handfirst:
            fp=fp+1
        else:
            print("Comparison error at ",i)
            break
    allpositive=len(handfirst)
    selected=len(pubprobe)
    try:
        precision=success/selected
        recall=success/allpositive
        score=(2*precision*recall)/(precision+recall)
    except:
        score=0
    return score

fonemaster=[None]*52
for i in range(52):
    fonemaster[i]=fonetwo(pubmaster2[i],handmaster2[i])