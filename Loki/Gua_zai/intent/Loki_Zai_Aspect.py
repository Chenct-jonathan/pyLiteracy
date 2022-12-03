#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Zai_Aspect

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

DEBUG_Zai_Aspect = True
try:
    userDefinedDICT = json.load(open(os.path.join(os.path.dirname(__file__), "USER_DEFINED.json"), encoding="utf-8"))
except:
    userDefinedDICT = {"_asNoun":["@","《","》","「","」","『","』","【","】","（","）"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_Zai_Aspect:
        print("[Zai_Aspect] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "在工作之餘":
        resultDICT["Zai"].append("Aspect")

    if utterance == "在跑步":
        resultDICT["Zai"].append("Aspect")

    return resultDICT