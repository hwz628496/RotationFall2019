# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 13:46:50 2019

@author: Henry

All XML files start with <'collection'><'document'> and thus should start with
foo['collection']['document']. Texts are structured in <passage>'s, where each 
passage has a single <text> tag sub-dictionary. <passage> also contains 
<annotation>'s, which inside contains an <id>, <infon> which contains what type 
of text (we care about [#text]=='Disease'), as well as the text string itself. 
Examples:
    foo['collection']['document']['passage'][0]['annotation']['infon'][1]['#text']=='Disease'
    foo['collection']['document']['passage'][0]['annotation']['text']=='Atrial Hemangioma'
    foo['collection']['document']['passage'][0]['text']==''Atrial Hemangioma: A Case Report and Review of the Literature'
    foo['collection']['document']['passage'][1]['annotation'][2]['text']=='cardiac tumor'
        >Note: if there are multiple OrderedDict in one level, a numerical indicator is needed,
        but if there's only one OrderedDict then no number is needed and you jump right to ['infon']
    
After <passage> should follow a number indicating which paragraph, with [0] being the title

To do: search through each index, look for disease terms and draw up a list for 
each PMID, one of handmade annotations, one from PubTator
"""

import xmltodict
foo=xmltodict.parse(urlxml[0])