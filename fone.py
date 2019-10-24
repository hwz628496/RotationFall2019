# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 22:33:42 2019

@author: Henry
"""

publist=pubmaster2[0][:]
handlist=handmaster2[0][:]

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