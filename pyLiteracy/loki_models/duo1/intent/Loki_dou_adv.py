#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for dou_adv

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
        responseDICT = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "reply/reply_dou_adv.json"), encoding="utf-8"))
    except Exception as e:
        print("[ERROR] responseDICT => {}".format(str(e)))

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG:
        print("[dou_adv] {} ===> {}".format(inputSTR, utterance))

def getResponse(utterance, args):
    resultSTR = ""
    if utterance in responseDICT:
        if len(responseDICT[utterance]):
            resultSTR = sample(responseDICT[utterance], 1)[0].format(*args)

    return resultSTR

def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern=""):
    debugInfo(inputSTR, utterance)
    if utterance == "哥哥和姐姐都":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"都":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "都多了兩公分":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"都":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "都多了兩歲":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"都":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "都沒有":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"都":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "都用了一千多年":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"都":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "都看了兩部電影":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"都":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "都花了一千多塊":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"都":[inputSTR]},
                          "proofread": ""
                         }

    return resultDICT