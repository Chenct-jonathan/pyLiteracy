#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for mei

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

DEBUG = False
CHATBOT_MODE = False

userDefinedDICT = {}
try:
    userDefinedDICT = json.load(open(os.path.join(os.path.dirname(__file__), "USER_DEFINED.json"), encoding="utf-8"))
except Exception as e:
    print("[ERROR] userDefinedDICT => {}".format(str(e)))

responseDICT = {}
if CHATBOT_MODE:
    try:
        responseDICT = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "reply/reply_mei.json"), encoding="utf-8"))
    except Exception as e:
        print("[ERROR] responseDICT => {}".format(str(e)))

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG:
        print("[mei] {} ===> {}".format(inputSTR, utterance))

def getResponse(utterance, args):
    resultSTR = ""
    if utterance in responseDICT:
        if len(responseDICT[utterance]):
            resultSTR = sample(responseDICT[utterance], 1)[0].format(*args)

    return resultSTR

def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern=""):
    debugInfo(inputSTR, utterance)
    if utterance == "各一顆":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"各":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "各三公尺":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"各":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "各人":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"各":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "各個":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"各":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "各所":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"各":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "各買一各":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"各":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "各買一次":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"各":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "每一顆":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"每":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "每三公尺":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"每":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "每人":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"每":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "每天":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"每":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "每次":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"每":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "每買一個":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"每":[inputSTR]},
                          "proofread": ""
                         }

    if utterance == "每買一次":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT = {"status": True,
                          "msg": "",
                          "check": {"每":[inputSTR]},
                          "proofread": ""
                         }

    return resultDICT