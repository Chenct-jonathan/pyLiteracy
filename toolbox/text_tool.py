#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def textPurger(tagInputSTR):
    '''
    Input:str (e.g. "<s> 碰到 無法 用 字面 解釋 的 句子 ， 你 真的 能 了解 美國人 在 說什麼嗎 ？ </s>" )
    Output:str (e.g. "碰到無法用字面解釋的句子，你真的能了解美國人在說什麼嗎 ？" )
    '''
    rawInputSTR = tagInputSTR.replace(" ", "").replace("&gt","").replace("&lt","").replace("<s>","").replace("</s>","")
    return rawInputSTR

def mergePurgedJson(jsonLIST,filename):
    '''
    Input:list (e.g. ["loc_zai_purged-10005.json","loc_zai_purged.json"]), str ("loc_zai_purged-all.json")
    Output: json file
    '''
    resultJsonDICT = {}
    for i in jsonLIST:
        jFILE = json.load(open(i, encoding="utf-8"))
        resultJsonDICT.update(jFILE)
        print(jFILE)
        mergedJson = json.JSONEncoder().encode(resultJsonDICT)
        mergedJsonFile = open(filename, "w")
        mergedJsonFile.write(mergedJson)
    return mergedJsonFile
