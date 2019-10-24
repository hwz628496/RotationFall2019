# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 21:44:06 2019

@author: Henry
"""


#xmldoc=urlxml[0]

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

test1,test2=sentenceadjust(urlxml[3],3,pmid_list,hand_master,pub_master)