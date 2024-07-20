#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for zai_vrep

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict,
        refDICT       dict,
        pattern       str

    Output:
        resultDICT    dict
"""

from random import sample
import json
import os

DEBUG = True
CHATBOT_MODE = False

userDefinedDICT = {}
try:
    userDefinedDICT = json.load(open(os.path.join(os.path.dirname(__file__), "USER_DEFINED.json"), encoding="utf-8"))
except Exception as e:
    print("[ERROR] userDefinedDICT => {}".format(str(e)))

responseDICT = {}
if CHATBOT_MODE:
    try:
        responseDICT = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "reply/reply_zai_vrep.json"), encoding="utf-8"))
    except Exception as e:
        print("[ERROR] responseDICT => {}".format(str(e)))

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG:
        print("[zai_vrep] {} ===> {}".format(inputSTR, utterance))
        #pass

def getResponse(utterance, args):
    resultSTR = ""
    if utterance in responseDICT:
        if len(responseDICT[utterance]):
            resultSTR = sample(responseDICT[utterance], 1)[0].format(*args)

    return resultSTR

def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern=""):
    debugInfo(inputSTR, utterance)
    #print("got the sentence")
    if utterance == "1983年再向虎山行飾紀青雲":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if "<UserDefined>" in args[8]:
                if args[9] in userDefinedDICT["as_Verb"] or args[9] in userDefinedDICT["as_Mod"]:
                    resultDICT["rep"].append("rep")
                else:
                    pass
            else:
                resultDICT["rep"].append("rep")
                
    if utterance == "2013再戰明天飾懲教人員":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "不再如此":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if "<UserDefined>" in args[0]:
                if args[5] in userDefinedDICT["as_Mod"]:
                    resultDICT["rep"].append("rep")
                else:
                    pass
            else:
                resultDICT["rep"].append("rep")

    if utterance == "再不簽核就會來不及":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再也不怕忘記":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再前行150公尺":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再多帶幾包":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再強悍的防毒軟體也會有失靈的一天":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再把這些要素融會整理":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再接再厲":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再於課堂中提問":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再查查":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再與冷熱進水彎頭連接鎖緊":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再處其負責人新臺幣十萬元以上五十萬元以下罰鍰":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再見":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if "<UserDefined>" in args[0]:
                if args[2] in userDefinedDICT["as_Verb"] or args[2] in userDefinedDICT["as_Noun"]:  
                    resultDICT["rep"].append("rep")
                else:
                    pass
            else:
                resultDICT["rep"].append("rep")

    if utterance == "到國光路後右轉再前行":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "包妥好再一根一根的結合起來":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "又再一次的超越自己了":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "希望時間可以再長一點":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "臺中支局葉菸草再乾燥場建築群":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "請再慎重考量":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "再一家家比較高低":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if args[0] == args[1]:
                resultDICT["rep"].append("rep")
            else:
                pass
            
    if utterance == "若於5年內再違反者":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "再上一層":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "再怎麼不喜歡":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "再發率":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "北門遊客中心再一新作":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "結帳再84折":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "再保險":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "再低5-10度":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "室內不再濕答答":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "要小心再小心":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if args[5] == args[8]:
                resultDICT["rep"].append("rep")
            else:
                pass
            
    if utterance == "再則屋主不必承受自營旅宿的種種風險":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "再這樣下去會得老年痴呆症":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "無論煮得再大鍋也不能改變事實":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")        

    return resultDICT