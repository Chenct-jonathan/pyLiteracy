#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from text_tool import textPurger
from ArticutAPI import Articut
import json
import re

accountDICT = json.load(open("account.info",encoding="utf-8"))
articut = Articut(username=accountDICT["username"],apikey=accountDICT["apikey"])

def purge_pos_loc_zai(startLine, lastLine):
    '''
    input : raw corpus.txt
    output : purged corpus + cws result.txt
    startline : int
    lastline : int 
    '''
    purgedDICT = {}
    with open("../corpus/Sketch Engine 在.txt", encoding="utf-8") as f:
        lines = ''.join(f.readlines())
        rawLIST = textPurger(lines).split("\n")
        purgedLIST = []
        [purgedLIST.append(x) for x in rawLIST if x not in purgedLIST]
    with open("../purged corpus/loc_zai_purged.txt", 'w', encoding = "utf-8") as g:
        for j in range(startLine, lastLine):#4539
            result_pos = articut.parse(purgedLIST[j],userDefinedDictFILE = "./USER_DEFINED.json")['result_pos']
            for s in result_pos:
                if "<FUNC_inner>在</FUNC_inner>" in s:
                    #g.write(purgedLIST[j]+"\n"+''.join(articut.parse(purgedLIST[j])['result_pos'])+"\n")
                    g.write("{}".format(re.sub('</?[a-zA-Z_]+>','',s))+"\n"+s+"\n")
            print(j)

def to_json(txtfile):
    zai_txtfile = open(txtfile, 'r', encoding='utf-8')
    count=0
    keys=[]
    values=[]
    for line in zai_txtfile:
        if count%2 == 0:
            keys.append(line.replace("\n", ""))
        else:
            values.append(line)
        count+=1
    dictionary = dict(zip(keys, values))

    with open("../purged corpus/loc_zai_purged.json", "w", encoding='UTF-8') as f:
        json.dump(dictionary, f, indent = 4, ensure_ascii=False)


if __name__ == "__main__":
    #purge_pos_loc_zai(5,9222)
    to_json("../purged corpus/loc_zai_purged.txt")