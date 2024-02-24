#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import json
from ArticutAPI import Articut

with open("jo_account.info", "r", encoding = "UTF-8") as p:
    accountDICT = json.load(p)

articut = Articut(username=accountDICT["username"],apikey=accountDICT["apikey"])


if __name__ == '__main__':
    corpusLIST = []
    with open("../../raw_data/Corpus/raw/sketch_engine_再.txt", "r", encoding = "UTF-8") as f:
        rawLIST = f.readlines()
    for i in range(len(rawLIST)):
        rawSTR = re.search("<s>([^<]*?)</s>", rawLIST[i])
        if rawSTR != None:
            corpusLIST.append(rawSTR.group(1).replace(" ", "").replace("&gt","").replace("&lt",""))
    for j in range(len(corpusLIST)):
        corpusSTR = re.search("[-（）()「」%、0-9a-zA-Z\u4E00-\u9FFF]*再[-（）()「」%、0-9a-zA-Z\u4E00-\u9FFF]*", corpusLIST[j])
        if corpusSTR != None and corpusSTR.group() not in corpusLIST:
            corpusLIST.append(corpusSTR.group())    
            #print(corpusSTR.group())
            
    for k in range(len(corpusLIST)):
        extDICT = articut.parse(corpusLIST[k])
        extSTR = articut.getVerbStemLIST(extDICT)
        print(extSTR)
    

