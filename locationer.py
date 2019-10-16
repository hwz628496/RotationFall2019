# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:50:17 2019

@author: Henry

Regex for finding location and offset

Regex used to find disease:
    <infon key="type">Disease<\/infon><location length="[0-9]+" offset="[0-9]+"\/><text>
"""

import re

xmldoc=urlxml[0]

disease_regex=re.compile('<infon key="type">Disease<\/infon><location length="[0-9]+" offset="[0-9]+"\/><text>')
re.findall(disease_regex,xmldoc)
locationstr=re.findall(disease_regex,xmldoc)

locations=[None]*len(locationstr)
for i in range(len(locationstr)):
    locations[i]=re.findall('\d+',locationstr[i])
    
