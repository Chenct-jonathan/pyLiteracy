#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for zai_loc

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
        responseDICT = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "reply/reply_zai_loc.json"), encoding="utf-8"))
    except Exception as e:
        print("[ERROR] responseDICT => {}".format(str(e)))

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG:
        print("[zai_loc] {} ===> {}".format(inputSTR, utterance))

def getResponse(utterance, args):
    resultSTR = ""
    if utterance in responseDICT:
        if len(responseDICT[utterance]):
            resultSTR = sample(responseDICT[utterance], 1)[0].format(*args)

    return resultSTR

def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern=""):
    debugInfo(inputSTR, utterance)
    if utterance == "在90.6公里處":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["loc_msg"] = args[0]
            resultDICT["clar_msg"] = "句中 {} 為一測量詞組，與名詞「處」組成之詞組 {}處 為一表示地點的詞組，而「在」引介某人或某事地點，故此處應使用「在」。".format(resultDICT["loc_msg"], resultDICT["loc_msg"])

    if utterance == "在彰化縣員林鎮山腳路5段312巷160號":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["loc_msg"] = args[0]
            resultDICT["clar_msg"] = "句中 {} 為一地址，為一表示地點的詞組，而「在」引介某人或某事地點，故此處應使用「在」。".format(resultDICT["loc_msg"])

    if utterance == "在臺灣":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["loc_msg"] = args[0]
            resultDICT["clar_msg"] = "句中 {} 為一表示地點的詞組，而「在」引介某人或某事地點，故此處應使用「在」。".format(resultDICT["loc_msg"])
    


    return resultDICT