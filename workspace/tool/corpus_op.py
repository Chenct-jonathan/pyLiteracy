#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import json

def extractFromFile(targetSTR):
    corpusLIST = []
    with open(f"../../raw_data/Corpus/raw/sketch_engine_{targetSTR}.txt", "r", encoding = "UTF-8") as f:
        rawLIST = f.readlines()
    for i in range(len(rawLIST)):
        rawSTR = re.search("<s>([^<]*?)</s>", rawLIST[i])
        if rawSTR != None and rawSTR not in corpusLIST:
            corpusLIST.append(rawSTR.group(1).replace(" ", ""))
            
    return corpusLIST
    
def dataPurge(corpusLIST, targetSTR):
    dataLIST = []
    for j in range(len(corpusLIST)):
        corpusSTR = re.search(f"[-（）()「」%、0-9a-zA-Z\u4E00-\u9FFF]*{targetSTR}[-（）()「」%、0-9a-zA-Z\u4E00-\u9FFF]*", corpusLIST[j])
        if corpusSTR != None and corpusSTR.group() not in dataLIST:
            dataLIST.append(corpusSTR.group())
    for k in dataLIST:
        print(k)
    print(len(dataLIST))    
    
    return dataLIST

def list2Json(dataLIST, filename):
    with open(f"../../raw_data/Corpus/purged/{filename}_purged.json", "w", encoding = "UTF-8") as jFILE:
        pass
    with open(f"../../raw_data/Corpus/purged/{filename}_purged.json", "w", encoding = "UTF-8") as jFILE:
        json.dump(dataLIST, jFILE, ensure_ascii=False)
        
def list2Txt(dataLIST, filename):
    with open(f"../../raw_data/Corpus/purged/{filename}_purged.txt", "w", encoding = "UTF-8") as textFILE:
        pass
    with open(f"../../raw_data/Corpus/purged/{filename}_purged.txt", "w", encoding = "UTF-8") as textFILE:
        for a in dataLIST:
            textFILE.write(a)
            textFILE.write("\n")
    
if __name__ == '__main__':
    targetSTR = "再"
    filename = "rep_zai"
    corpusLIST = extractFromFile(targetSTR)
    dataLIST = dataPurge(corpusLIST, targetSTR)
    list2Json(dataLIST, filename)
    list2Txt(dataLIST, filename)