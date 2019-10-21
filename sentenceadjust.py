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
#xmldoc=urlxml[0]

import re

paragraphstr=re.compile('<passage>.+?<infon key="section_type">.+?<\/infon><infon key="type">paragraph<\/infon><offset>[0-9]+<\/offset><text>.+?<\/text>')
paragraphs=re.findall(paragraphstr,xmldoc)
paragraphs2=[None]*len(paragraphs)
for i in range(len(paragraphs)):
    holder=re.findall('>.*?<',paragraphs[i])
    paragraphs2[i]=holder[-1][1:(len(holder[-1])-1)]

for i in xmldoc:
    