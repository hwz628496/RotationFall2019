# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 14:20:38 2019

@author: Henry

Using regex: format of text is thus:
    
<annotation id="1">
<infon key="Identifier">
MESH:D006391</infon>
<infon key="type">
Disease</infon>
<location length="17" offset="0"/>
<text>
Atrial Hemangioma</text>
</annotation>

First, we get the string from urlxml, find the PMCID.
Then convert from PMCID to PMID: https://www.ncbi.nlm.nih.gov/pmc/tools/id-converter-api/
Then open filename PMID.ann and read my hand annotations
Then compare?????

"""

import re

#get PMID
pmidre=re.compile('<id>[0-9]+<\/id>')
pmid=re.findall(pmidre,urlxml[0])

urlstr='https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email=my_email@example.com&ids=PMC'+pmid[0][4:11]

re.compile('<infon key="type">Disease<\/infon>')