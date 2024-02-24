#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for dou

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
        responseDICT = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "reply/reply_dou.json"), encoding="utf-8"))
    except Exception as e:
        print("[ERROR] responseDICT => {}".format(str(e)))

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG:
        print("[dou] {} ===> {}".format(inputSTR, utterance))

def getResponse(utterance, args):
    resultSTR = ""
    if utterance in responseDICT:
        if len(responseDICT[utterance]):
            resultSTR = sample(responseDICT[utterance], 1)[0].format(*args)

    return resultSTR

def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern=""):
    debugInfo(inputSTR, utterance)
    if utterance == "[兩個][房子][都]":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if args[0][:-1] not in "一1" and set("一二兩三四五六七八九十百千萬億").intersection(args[0][:-1]):
                resultDICT = {"status": True,
                              "msg": "",
                              "check": {"都":[inputSTR]},
                              "proofread": ""
                              }

    if utterance == "[兩個][都]":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if set("一二兩三四五六七八九十百千萬億").intersection(args[0][:-1]):
                resultDICT = {"status": True,
                              "msg": "",
                              "check": {"都":[inputSTR]},
                              "proofread": ""
                              }

    if utterance == "[我們][都]":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"都":[inputSTR]},
                          "proofread": ""
                         }
            if args[0].endswith("們"):
                pass
            elif args[0][-2:] in ("父母", "兄弟", "姐妹", "姐弟", "姊弟", "姊妹", "兄妹"):
                pass
            else:
                resultDICT = {}

    if utterance == "[我們]不[都]":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"都":[inputSTR]},
                          "proofread": ""
                         }
            if args[0].endswith("們"):
                pass
            elif args[0][-2:] in ("父母", "兄弟", "姐妹", "姐弟", "姊弟", "姊妹", "兄妹"):
                pass
            else:
                resultDICT = {}

    if utterance == "[都]幾":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"都":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "[都]給[你]":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"都":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "每次都":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"都":[inputSTR]},
                          "proofread": ""
                         }

    return resultDICT