#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for adv_sinica_chayidian

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

import json
import os
import re
from ArticutAPI import Articut

accountDICT = json.load(open("account.info",encoding="utf-8"))
articut = Articut(username=accountDICT["username"],apikey=accountDICT["apikey"], version="v258")
userDefinedDictFILE = "./intent/USER_DEFINED.json"

DEBUG_adv_sinica_chayidian = True
try:
    userDefinedDICT = json.load(open(os.path.join(os.path.dirname(__file__), "USER_DEFINED.json"), encoding="utf-8"))
except:
    userDefinedDICT = {"_asNoun":["卡子","婦女支援組織","意念","艾柏格","身心","隨從"],"_asVerb":["打轉","抽腳筋","見上面","車畚斗","陰溝裡翻船"],"_tmpToken":["畢業生","盛況","質素"],"_extractFromPunc":["仇人席","保守","大智若愚","平分秋色","拉一把","晚晴協會","活古蹟","眼淚歌后","選秀狀元","鄉土"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_adv_sinica_chayidian:
        print("[adv_sinica_chayidian] {} ===> {}".format(inputSTR, utterance))

def inputSTRSpliter(inputSTR, spliterSTR="差一點"):
    tmpInputSTR = inputSTR.split(spliterSTR)[-1]
    return "差一點"+tmpInputSTR

def formMSG(tmpInputSTR, pat):
    '''
    input: 我差一點跌倒ㄟ
    output : <MODIFIER>差一點</MODIFIER><ACTION_verb>跌倒</ACTION_verb><ENTITY_nouny>ㄟ</ENTITY_nouny>
    把 inputSTR 轉成 Articut 結果
    '''
    tmpResultDICT = articut.parse(tmpInputSTR, userDefinedDictFILE=userDefinedDictFILE)
    if tmpResultDICT["status"] == True:
        posSTR = ''.join(tmpResultDICT["result_pos"])
        return posSTR
    else:
        raise Exception("Invalid Articut result:{}".format(tmpResultDICT["message"]))

def getResult(inputSTR, utterance, pat, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "只差一點沒和那漂亮女人做成一回好事":
        if "inputSTR" in resultDICT.keys():
            pass
        else:
            tmpInputSTR = inputSTRSpliter(inputSTR)
            tmpPosSTR = formMSG(tmpInputSTR, pat)
            #print(re.findall(pat,tmpPosSTR))
            resultDICT["FirstVerb"] = re.search(pat,tmpPosSTR).group(2)
            if resultDICT["FirstVerb"] == None:
                resultDICT["FirstVerb"] = re.search(pat,tmpPosSTR).group(5)
            else:
                resultDICT["FirstVerb"] = re.search(pat,tmpPosSTR).group(2)
            resultDICT["reason"] = "[差一點] 後的第一個動詞 [{}] 為一結束體事件(accomplishment)語意，故可使用 [差一點]。".format(resultDICT["FirstVerb"])
            resultDICT["key"] = "結束體(accomplishment)"

    if utterance == "否則差一點看不到新中國":
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        #print(re.findall(pat,tmpPosSTR))
        resultDICT["FirstVerb"] = re.search(pat,tmpPosSTR).group(5)
        resultDICT["reason"] = "[差一點] 後的第一個動詞 [{}] 符合 [{}] 詞彙結構，為一結束體事件(accomplishment)語意，故可使用 [差一點]。".format(resultDICT["FirstVerb"],"V "+resultDICT["FirstVerb"][1:])
        resultDICT["key"] = "結束體(accomplishment)"

    if utterance == "差一點他那神父爸爸便不能認這個孩子":
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        resultDICT["negation"] = re.search(pat,tmpPosSTR).group(14)
        resultDICT["modal"] = re.search(pat,tmpPosSTR).group(16)
        resultDICT["FirstVerb"] = re.search(pat,tmpPosSTR).group(18)
        #print(re.findall(pat,tmpPosSTR ))
        if resultDICT["negation"] != None:
            if resultDICT["modal"] != None:
                resultDICT["reason"] = "[差一點] 後的第一個動詞 [{}] 前有否定詞 [{}]，故 [{}] 為一經驗貌事件(experiencial)語意，故可使用 [差一點]。".format(resultDICT["FirstVerb"],resultDICT["negation"]+resultDICT["modal"], resultDICT["negation"]+resultDICT["modal"]+resultDICT["FirstVerb"])
                resultDICT["key"] = "經驗貌(experiencial)"
            else:
                resultDICT["reason"] = "[差一點] 後的第一個動詞 [{}] 前有否定詞 [{}]，故 [{}] 為一經驗貌事件(experiencial)語意，故可使用 [差一點]。".format(resultDICT["FirstVerb"],resultDICT["negation"], resultDICT["negation"]+resultDICT["FirstVerb"])
                resultDICT["key"] = "經驗貌(experiencial)"
        else:
            if resultDICT["modal"] != None:
                resultDICT["reason"] = "[差一點] 後的第一個動詞 [{}] 前有 modality [{}]，故 [{}] 為一經驗貌事件(experiencial)語意，故可使用 [差一點]。".format(resultDICT["FirstVerb"],resultDICT["modal"], resultDICT["modal"]+resultDICT["FirstVerb"])
                resultDICT["key"] = "經驗貌(experiencial)"
            else:
                pass

    if utterance == "差一點就沒命了":
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        resultDICT["modifier"] = re.search(pat,tmpPosSTR).group(5)#待更改
        resultDICT["aspect"] = re.search(pat,tmpPosSTR).group(7)
        #print(re.findall(pat,tmpPosSTR ))
        resultDICT["reason"] = "[差一點] 後的 [{}] 為一完成貌事件(perfective)語意，故可使用 [差一點]".format(resultDICT["modifier"]+resultDICT["aspect"])
        resultDICT["key"] = "完成貌(perfective)"

    if utterance == "差一點就讓這種傳統工藝走不回來":
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        resultDICT["FirstVerb"] = re.search(pat,tmpPosSTR).group(5)
        #print(re.findall(pat,tmpPosSTR ))
        resultDICT["reason"] = "[差一點] 後的子句 [{}] 為一完成貌事件(perfective)語意，故可使用 [差一點]。".format("讓"+"".join(tmpInputSTR.split("讓")[1:]))
        resultDICT["key"] = "完成貌 (perfective)"

    if utterance == "差一點把爸爸心愛的上等酒給打翻了":
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        resultDICT["FirstVerb"] = re.search(pat,tmpPosSTR).group(7)
        #print(re.findall(pat,tmpPosSTR ))
        resultDICT["reason"] = "[差一點] 後的 [把...] 字句 [{}] 為一完成貌事件(perfective)語意，故可使用 [差一點]".format("把"+"".join(tmpInputSTR.split("把")[1:]))
        resultDICT["key"] = "完成貌 (perfective)"

    if utterance == "差一點提前引爆華隆跳票的引信":#re problem
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        resultDICT["FirstVerb"] = re.search(pat,tmpPosSTR).group(5)
        resultDICT["range"] = re.search(pat,tmpPosSTR).group(8)
        #print(re.findall(pat,tmpPosSTR ))
        resultDICT["reason"] = "[差一點] 後的第一個動詞 [{}] 為一結束體事件(accomplishment)語意，故可使用 [差一點]".format(resultDICT["FirstVerb"]+resultDICT["range"])
        resultDICT["key"] = "結束體(accomplishment)"

    if utterance == "差一點昏倒": # 只有符合此 pattern 的句子會進此 code block 處理
        tmpInputSTR = inputSTRSpliter(inputSTR) # 只取 input 字串中從 [差一點] 開始的字
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        if re.search(pat,tmpPosSTR).group(5) == None:# 以位置為依據找尋第一個動詞
            resultDICT["First Verb"] = re.search(pat,tmpPosSTR).group(6)
            if re.search(pat,tmpPosSTR).group(8) == None:
                pass
            else:
                resultDICT["First Verb"] = resultDICT["First Verb"] + re.search(pat,tmpPosSTR).group(8)
        elif re.search(pat,tmpPosSTR).group(6) == None:
            resultDICT["First Verb"] = re.search(pat,tmpPosSTR).group(5)
        if resultDICT["First Verb"][-1] in  ["了","昏"]:
            resultDICT["reason"] = "因為 [差一點] 後面的第一個動詞 [{}] 為完成貌事件(perfective)語意，故可使用 [差一點]。 ".format(resultDICT["First Verb"])
            resultDICT["key"] = "完成貌(perfective)"
        else:
            resultDICT["reason"] = "因為 [差一點] 後面的第一個動詞 [{}] 為結束體事件(accomplishment)語意，故可使用 [差一點]。 ".format(resultDICT["First Verb"])
            resultDICT["key"] = "結束體(accomplishment)"

    if utterance == "差一點沒把手指頭當菜切了":#差一點把手指頭當菜切了
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        resultDICT["FirstVerb"] = re.search(pat,tmpPosSTR).group(13)
        #print(re.findall(pat,tmpPosSTR ))
        resultDICT["reason"] = "[差一點] 後的 [把...] 字句 [{}] 為一完成貌事件(perfective)語意，故可使用 [差一點]".format("把"+"".join(tmpInputSTR.split("把")[1:]))
        resultDICT["key"] = "完成貌 (perfective)"

    if utterance == "差一點遭到截肢":
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        resultDICT["passive"] = re.search(pat,tmpPosSTR).group(5)
        #print(re.findall(pat,tmpPosSTR ))
        resultDICT["reason"] = "[差一點] 後的被動式子句 [{}] 為一完成貌事件(perfective)語意，故可使用 [差一點]。".format(resultDICT["passive"]+tmpInputSTR.split(resultDICT["passive"])[-1])
        resultDICT["key"] = "完成貌(perfective)"

    if utterance == "差一點陰溝裡翻船":
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        #print(tmpPosSTR)
        resultDICT["idiom"] = re.search(pat,tmpPosSTR).group(7)
        if resultDICT["idiom"] in userDefinedDICT["_asVerb"]:
            resultDICT["reason"] = "[差一點] 後的 idiom [{}] 若為一完成貌事件(perfective)或經驗貌事件(experiantial)語意，則可使用 [差一點]。".format(resultDICT["idiom"])
            resultDICT["key"] = "完成貌(perfective)或經驗貌(experiantial)均"
        else:
            pass
        #print(re.findall(pat,tmpPosSTR ))

    if utterance == "最後還差一點就當選高雄區的立法委員":
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        resultDICT["FirstVerb"] = re.search(pat,tmpPosSTR).group(5)
        #print(re.findall(pat,tmpPosSTR ))
        resultDICT["reason"] = "[差一點] 後的第一個動詞 [{}] 若為一達成體事件(achievement)語意，則可使用 [差一點]。".format(resultDICT["FirstVerb"])
        resultDICT["key"] = "達成體事件(achievement)"

    if utterance == "爭三連霸的瑞典名將艾柏格則差一點落馬":
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        resultDICT["FirstVerb"] = re.search(pat,tmpPosSTR).group(5)
        #print(re.findall(pat,tmpPosSTR ))
        resultDICT["reason"] = "[差一點] 後的第一個動詞 [{}] 為一結束體事件(accomplishment)語意，故可使用 [差一點]。".format(resultDICT["FirstVerb"])
        resultDICT["key"] = "結束體(accomplishment)"

    if utterance == "謝長亨差一點就是中華職棒第一個「選秀狀元」":
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        resultDICT["auxiliary"] = re.search(pat,tmpPosSTR).group(1)
        #print(re.findall(pat,tmpPosSTR ))
        resultDICT["reason"] = "[差一點] 後的助動詞 [{}] 為一達成體事件(achievement)語意，故可使用 [差一點]".format(resultDICT["auxiliary"])
        resultDICT["key"] = "達成體(achievement)"

    if utterance == "雖然差一點而沒挑戰成功":#待改
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        resultDICT["FirstVerbP"] = re.search(pat,tmpPosSTR).group(5) + re.search(pat,tmpPosSTR).group(7)
        #print(re.findall(pat,tmpPosSTR ))
        resultDICT["reason"] = "[差一點] 後的第一個動詞 [{}] 為一完成貌事件(perfective)語意，故可使用 [差一點]".format(resultDICT["FirstVerbP"])
        resultDICT["key"] = "完成貌(perfective)"
        
    if utterance == "她差一點栽在印度芭娜姬的手中":
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        resultDICT["FirstVerb"] = re.search(pat,tmpPosSTR).group(5)
        #print(re.findall(pat,tmpPosSTR ))
        resultDICT["reason"] = "[差一點] 後的子句 [{}] 為一結束體事件(accomplishment)語意，故可使用 [差一點]".format(resultDICT["FirstVerb"] + tmpInputSTR.split(resultDICT["FirstVerb"])[-1])
        resultDICT["key"] = "結束體(accomplishment)"
        
    if utterance == "三個年輕人差一點就要去大鬧天宮":
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        resultDICT["FirstVerb"] = re.search(pat,tmpPosSTR).group(6)
        #print(re.findall(pat,tmpPosSTR ))
        resultDICT["reason"] = "[差一點] 後的第一個動詞 [{}] 為一經驗貌事件(experiential)語意，故可使用 [差一點]".format(resultDICT["FirstVerb"])
        resultDICT["key"] = "經驗貌(experiential)"
        
    if utterance == "差一點沒到九十分":
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        resultDICT["FirstVerb"] = re.search(pat,tmpPosSTR).group(3)
        resultDICT["number"] = re.search(pat,tmpPosSTR).group(7)
        #print(re.findall(pat,tmpPosSTR ))
        resultDICT["reason"] = "[差一點] 後的子句 [{}] 為一完成貌事件(perfective)語意，故可使用 [差一點]".format(resultDICT["FirstVerb"] + resultDICT["number"])
        resultDICT["key"] = "完成貌(perfective)"
        
    if utterance == "我差一點認不出她來":
        tmpInputSTR = inputSTRSpliter(inputSTR)
        tmpPosSTR = formMSG(tmpInputSTR, pat)
        #print(re.findall(pat,tmpPosSTR))
        resultDICT["FirstVerb"] = re.search(pat,tmpPosSTR).group(2)
        resultDICT["reason"] = "[差一點] 後的第一個動詞 [{}] 符合 [{}] 詞彙結構，為一結束體事件(accomplishment)語意，故可使用 [差一點]。".format(resultDICT["FirstVerb"],"V " + re.search(pat,tmpPosSTR).group(4) + re.search(pat,tmpPosSTR).group(7))
        resultDICT["key"] = "結束體(accomplishment)"        

    return resultDICT