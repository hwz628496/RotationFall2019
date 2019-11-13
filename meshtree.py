# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 14:27:05 2019

@author: hwz62
"""

import json
import sys
import time
import pandas as pd
meshtree = "mtrees2020.bin" 

csvTree = []
id2name = {}
name2id = {}

with open(meshtree, "r") as ftree:
    for line in ftree:
        term_tree = line.strip().split(";")
        cur_term = term_tree[0]
        cur_tree = term_tree[1]
        
        
        csvTree.append({'id':cur_tree ,\
                        'name':cur_term})
        
        id2name.update({cur_tree:cur_term})
                        
        name2id.update({cur_term:cur_tree})
        
DF = pd.DataFrame(csvTree)
DF = DF.sort_values( ['id'],axis =0,ascending =True)
DF = DF.set_index('id')
DF.to_csv('csvTree.csv')
with open('id2name.json', 'w')as df:
    json.dump(id2name,df)