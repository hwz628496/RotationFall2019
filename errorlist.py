# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 13:03:49 2019

@author: Henry
"""

def handformat(index):
    import copy
    misslist=copy.deepcopy(missmaster[index][:])
    fplist=copy.deepcopy(fpmaster[index][:])
    successlist=copy.deepcopy(successmaster[index][:])
    handlist=copy.deepcopy(handmaster2[index][:])
    
    grouplist=[["","","","","","","","",""] for i in range(50000)]
    
    for i in range(len(misslist)):
        grouplist[misslist[i][0]][0]=misslist[i][0]
        grouplist[misslist[i][0]][1]=misslist[i][1]
        grouplist[misslist[i][0]][2]=misslist[i][2]
    
    for i in range(len(fplist)):
        grouplist[fplist[i][0]][3]=fplist[i][0]
        grouplist[fplist[i][0]][4]=fplist[i][1]
        grouplist[fplist[i][0]][5]=fplist[i][2]
    
    for i in range(len(handlist)):
        grouplist[handlist[i][0]][6]=handlist[i][0]
        grouplist[handlist[i][0]][7]=handlist[i][1]
        grouplist[handlist[i][0]][8]=handlist[i][2]
        
    for i in range(len(grouplist)-1,-1,-1):
        if grouplist[i]==[""]*9:
            del grouplist[i]
    return grouplist

grouplistgroup=[None]*52
for i in range(52):
    grouplistgroup[i]=handformat(i)