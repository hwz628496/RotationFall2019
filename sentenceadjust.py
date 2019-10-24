# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 14:16:27 2019

@author: Henry

BRAT strips spaces from sentences, PubTator does not. This causes errors.

Plan:
    Divide document into paragraph chunks
    Search through every line in paragraph
    Add a pipe (|) after every newline, replacing the space after the break
    For each pubtator term, scan from beginning of paragraph to pubtator-stated
        location. Count number of pipes. Adjust using number of pipes.

The idea here is is to encode BRAT's line breaks into PubTator's information.
"""

#find id
xmldoc=urlxml[3]

import re

paragraphre=re.compile('<passage>.+?<infon key="section_type">.+?<\/infon><infon key="type">paragraph<\/infon><offset>[0-9]+<\/offset><text>.+?<\/text>')
paragraphs=re.findall(paragraphre,xmldoc)
paragraphs2=[None]*len(paragraphs)
for i in range(len(paragraphs)):
    holder=re.findall('>.*?<',paragraphs[i])
    paragraphs2[i]=holder[-1][1:(len(holder[-1])-1)]

#load brat sentence texts
brattxt=[]
fo=open('./PMC_sentences/'+pmid_list[0]+'.txt')
for i in fo:
    brattxt.append(i[:-1])
fo.close()

pubstr=""
for i in paragraphs2:
    pubstr=pubstr+'|'+i
pubstr=pubstr[1:]

bratstr=""
for i in brattxt:
    bratstr=bratstr+'|'+i
bratstr=bratstr[1:]

#adjust for sentences
handext=hand_master[0]
adjust=bratstr.count('|',0,int(handext[0][0]))
for j in range(len(handext)):
    handext[j][0]=int(handext[j][0])-adjust
    handext[j][1]=int(handext[j][1])-adjust
for i in range(1,len(handext)):
    adjust=bratstr.count('|',int(handext[i-1][0]),int(handext[i][0]))
    for j in range(i,len(handext)):
        handext[j][0]=int(handext[j][0])-adjust
        handext[j][1]=int(handext[j][1])-adjust

#adjust for PubMed section title offsets
#titlere=re.compile('<infon key="section_type">.+?<\/infon><offset>.*?<\/offset><text>.+?<\/text>')
#titles=re.findall(titlere,xmldoc)
#titles2=[None]*len(titles)
#for i in range(len(titles)):
#    holder=re.findall('>.*?<',titles[i])
#    titles2[i]=holder[-1][1:(len(holder[-1])-1)]
#
#offsetre=re.compile('<offset>(\d*?)<\/offset>')
#offsetnum=[None]*len(titles)
#for i in range(len(titles)):
#    offsety=re.search(offsetre,titles[i])
#    if offsety:
#        offsetnum[i]=offsety.group(1)

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
difflist3seconds=[i[1] for i in difflist3]

difflistdict=dict(zip(difflist3firsts,difflist3seconds))

publistadjust=pub_master[0][:]
publistadjust2=publistadjust
for i in range(len(publistadjust)):
    pos=publistadjust[i][0]
    if pos>=difflist3firsts[0]:
        diffdictlookup=max(k for k in difflist3firsts if k<=pos)
        offsetpos=difflistdict[diffdictlookup]
    else:
        offsetpos=0
    print(offsetpos)
    holder=[int(publistadjust[i][0])-offsetpos, int(publistadjust[i][1])-offsetpos, publistadjust[i][2]]
    publistadjust2[i]=holder



for i in range(1,len(titles)):
    print(int(titles[i][1])-int(titles[i-1][1])-len(titles[i-1][2]))

realoffsets=[]
for i in range(1,len(paragraph_list)):
    realoffsets.append(int(titles[paragraph_list[i]][1])-int(titles[paragraph_list[i-1]][1])-len(titles[paragraph_list[i-1]][2])-1)

realoffsets2=[]
tally=0
for i in range(len(realoffsets)):
    tally=tally+realoffsets[i]
    realoffsets2.append(tally)
difflistdict2=dict(zip(difflist3firsts,realoffsets2))