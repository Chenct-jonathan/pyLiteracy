#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Zai_State

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

DEBUG_Zai_State = True
try:
    userDefinedDICT = json.load(open(os.path.join(os.path.dirname(__file__), "USER_DEFINED.json"), encoding="utf-8"))
except:
    userDefinedDICT = {"_asNoun":["@","《","》","「","」","『","』","【","】","（","）"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_Zai_State:
        print("[Zai_State] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "在90%中":
        resultDICT["Zai"].append("State")

    if utterance == "在內":
        resultDICT["Zai"].append("State")

    if utterance == "在前後文":
        resultDICT["Zai"].append("State")

    if utterance == "在於":
        resultDICT["Zai"].append("State")

    if utterance == "在桌上":
        resultDICT["Zai"].append("State")

    if utterance == "在軟體方面":
        resultDICT["Zai"].append("State")

    if utterance == "收錄在第三頁":
        resultDICT["Zai"].append("State")

    return resultDICT