# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:50:17 2019

@author: Henry

Regex for finding location and offset

Regex used to find disease:
    <infon key="type">Disease<\/infon><location length="[0-9]+" offset="[0-9]+"\/><text>
"""
#xmldoc=urlxml[0]

def xmllocs(xmldoc,publist):
    import re
    disease_regex=re.compile('<infon key="type">Disease<\/infon><location length="[0-9]+" offset="[0-9]+"\/><text>')
    re.findall(disease_regex,xmldoc)
    locationstr=re.findall(disease_regex,xmldoc)
    
    locations=[None]*len(locationstr)
    for i in range(len(locationstr)):
        locations[i]=re.findall('\d+',locationstr[i])
    
    locations2=[None]*len(locations)
    for i in range(len(locations)):
        locations2[i]=[None]*3
        locations2[i][0]=int(locations[i][1])-int(locations[0][1])
        locations2[i][1]=int(locations[i][0])+int(locations2[i][0])
        locations2[i][2]=publist[i]
    return locations2

pub_master=[None]*52
for i in range(52):
    pub_master[i]=xmllocs(urlxml[i],pubtator_group[i])