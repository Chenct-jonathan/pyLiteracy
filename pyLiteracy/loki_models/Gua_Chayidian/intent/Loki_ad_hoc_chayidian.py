#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for ad_hoc_chayidian

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

DEBUG_ad_hoc_chayidian = True
try:
    userDefinedDICT = json.load(open(os.path.join(os.path.dirname(__file__), "USER_DEFINED.json"), encoding="utf-8"))
except:
    userDefinedDICT = {"_asNoun":["卡子","婦女支援組織","意念","艾柏格","身心","隨從"],"_asVerb":["打轉","抽腳筋","見上面","車畚斗","陰溝裡翻船"],"_tmpToken":["畢業生","盛況","質素"],"_extractFromPunc":["仇人席","保守","大智若愚","平分秋色","拉一把","晚晴協會","活古蹟","眼淚歌后","選秀狀元","鄉土"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_ad_hoc_chayidian:
        print("[ad_hoc_chayidian] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "即使差一點":
        resultDICT["reason"] = "這個 [差一點] 是 predicate(worse) 而非 approximative adverb 的 [差一點]，不在討論範圍內。"
        

    if utterance == "若是評估質素差一點的":
        resultDICT["reason"] = "這個 [差一點] 是 predicate(worse) 而非 approximative adverb 的 [差一點]，不在討論範圍內。"
        

    if utterance == "這些胎生的小苗萬一在第一次落下運氣差一點":
        resultDICT["reason"] = "這個 [差一點] 是 predicate(worse) 而非 approximative adverb 的 [差一點]，不在討論範圍內。"
        

    if utterance == "還差一點旅行社才開門辦公":#差一點所指意義待確認
        resultDICT["reason"] = "這個 [差一點] 是 predicate(less than) 而非 approximative adverb 的 [差一點]，不在討論範圍內。"
        
        
    if utterance == "照片內容也和原先想的大概差一點":
        resultDICT["reason"] = "這個 [差一點] 是 predicate (less than) 而非 approximative adverb 的 [差一點]，不在討論範圍內。"

    return resultDICT