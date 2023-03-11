#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki 3.0 Template For Python3

    [URL] https://api.droidtown.co/Loki/BulkAPI/

    Request:
        {
            "username": "your_username",
            "input_list": ["your_input_1", "your_input_2"],
            "loki_key": "your_loki_key",
            "filter_list": ["intent_filter_list"] # optional
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v223",
            "word_count_balance": 2000,
            "result_list": [
                {
                    "status": True,
                    "msg": "Success!",
                    "results": [
                        {
                            "intent": "intentName",
                            "pattern": "matchPattern",
                            "utterance": "matchUtterance",
                            "argument": ["arg1", "arg2", ... "argN"]
                        },
                        ...
                    ]
                },
                {
                    "status": False,
                    "msg": "No matching Intent."
                }
            ]
        }
"""

import json
from requests import post
from requests import codes
import math
import re
try:
    from intent import Loki_Zai_verbP
    from intent import Loki_Zai_Aspect
    from intent import Loki_Zai_Range
    from intent import Loki_Zai_State
    from intent import Loki_Zai_Loc
except:
    from .intent import Loki_Zai_verbP
    from .intent import Loki_Zai_Aspect
    from .intent import Loki_Zai_Range
    from .intent import Loki_Zai_State
    from .intent import Loki_Zai_Loc

import os

with open("{}/../../account.info".format(BASEPATH), encoding="utf-8") as f:
    accountDICT = json.load(f)

LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
USERNAME = accountDICT["username"]
LOKI_KEY = accountDICT["loki-key"]
# 意圖過濾器說明
# INTENT_FILTER = []        => 比對全部的意圖 (預設)
# INTENT_FILTER = [intentN] => 僅比對 INTENT_FILTER 內的意圖
INTENT_FILTER = []
INPUT_LIMIT = 20

class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = []

    def __init__(self, inputLIST, filterLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []
        # filterLIST 空的就採用預設的 INTENT_FILTER
        if filterLIST == []:
            filterLIST = INTENT_FILTER

        try:
            result = post(LOKI_URL, json={
                "username": USERNAME,
                "input_list": inputLIST,
                "loki_key": LOKI_KEY,
                "filter_list": filterLIST
            })

            if result.status_code == codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "{} Connection failed.".format(result.status_code)
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLokiStatus(self, index):
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

def runLoki(inputLIST, filterLIST=[]):
    # 將 intent 會使用到的 key 預先設爲空列表
    resultDICT = {
       "Zai": [],
       "RepZai":[]
    }
    lokiRst = LokiResult(inputLIST, filterLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # Zai_Loc
                if lokiRst.getIntent(index, resultIndex) == "Zai_Loc":
                    resultDICT = Loki_Zai_Loc.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Zai_State
                if lokiRst.getIntent(index, resultIndex) == "Zai_State":
                    resultDICT = Loki_Zai_State.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Zai_verbP
                if lokiRst.getIntent(index, resultIndex) == "Zai_verbP":
                    resultDICT = Loki_Zai_verbP.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Zai_Aspect
                if lokiRst.getIntent(index, resultIndex) == "Zai_Aspect":
                    resultDICT = Loki_Zai_Aspect.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Zai_Range
                if lokiRst.getIntent(index, resultIndex) == "Zai_Range":
                    resultDICT = Loki_Zai_Range.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return resultDICT

def execLoki(content, filterLIST=[], splitLIST=[]):
    """
    input
        content       STR / STR[]    要執行 loki 分析的內容 (可以是字串或字串列表)
        filterLIST    STR[]          指定要比對的意圖 (空列表代表不指定)
        splitLIST     STR[]          指定要斷句的符號 (空列表代表不指定)
                                     * 如果一句 content 內包含同一意圖的多個 utterance，請使用 splitLIST 切割 content

    output
        resultDICT    DICT           合併 runLoki() 的結果，請先設定 runLoki() 的 resultDICT 初始值

    e.g.
        splitLIST = ["！", "，", "。", "？", "!", ",", "
", "；", "　", ";"]
        resultDICT = execLoki("今天天氣如何？後天氣象如何？")                      # output => ["今天天氣"]
        resultDICT = execLoki("今天天氣如何？後天氣象如何？", splitLIST=splitLIST) # output => ["今天天氣", "後天氣象"]
        resultDICT = execLoki(["今天天氣如何？", "後天氣象如何？"])                # output => ["今天天氣", "後天氣象"]
    """
    contentLIST = []
    if type(content) == str:
        contentLIST = [content]
    if type(content) == list:
        contentLIST = content

    resultDICT = {}
    if contentLIST:
        if splitLIST:
            # 依 splitLIST 做分句切割
            splitPAT = re.compile("[{}]".format("".join(splitLIST)))
            inputLIST = []
            for c in contentLIST:
                tmpLIST = splitPAT.split(c)
                inputLIST.extend(tmpLIST)
            # 去除空字串
            while "" in inputLIST:
                inputLIST.remove("")
        else:
            # 不做分句切割處理
            inputLIST = contentLIST

        # 依 INPUT_LIMIT 限制批次處理
        for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
            lokiResultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST)
            if "msg" in lokiResultDICT:
                return lokiResultDICT

            # 將 lokiResultDICT 結果儲存至 resultDICT
            for k in lokiResultDICT:
                if k not in resultDICT:
                    resultDICT[k] = []
                resultDICT[k].extend(lokiResultDICT[k])

    return resultDICT

def testLoki(inputLIST, filterLIST):
    INPUT_LIMIT = 20
    for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
        resultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST)

    if "msg" in resultDICT:
        print(resultDICT["msg"])

def testIntent():
    # Zai_Loc
    print("[TEST] Zai_Loc")
    inputLIST = ['在此','保持在','在其中','在台灣','在我國','在本款','在此處','在浴室','在90.6K處','在中文系','在別台電腦','在同一電腦','在福建省中','在科學機構','在許多角落','在國家音樂廳','在國外購買商品','在我國之申請案','在有限的預算中','在東方320公里外','在正式課程之外','在一般的營業場所','在金融和投資等方面','在「尚有庫存」內出貨','紅色木屋在綠樹中掩映']
    testLoki(inputLIST, ['Zai_Loc'])
    print("")

    # Zai_State
    print("[TEST] Zai_State")
    inputLIST = ['在內','在於','在2009','在90%中','在桌上','在800年前','在前後文','在該範圍內','在軟體方面','目前在第1頁','長度在0以上','在西元前800年','收錄在第三頁','在七期新光三越','在福智高級中學','在不確定的世界裡','在新台幣五千元以內','在古典與現代之間悠遊','在短期內較易收得成效','收錄在被行銷者之手機','長度在0以上的任意字串','目前情趣內衣多在數千元之譜','並在會後舉行年終尾牙聚餐活動','可用來保障您在線上傳輸的資料不會外流','可以讓你在不增加任何成本的狀況下接觸更多顧客']
    testLoki(inputLIST, ['Zai_State'])
    print("")

    # Zai_verbP
    print("[TEST] Zai_verbP")
    inputLIST = ['我目前在職']
    testLoki(inputLIST, ['Zai_verbP'])
    print("")

    # Zai_Aspect
    print("[TEST] Zai_Aspect")
    inputLIST = ['在跑步','在工作之餘','在輕輕的燒']
    testLoki(inputLIST, ['Zai_Aspect'])
    print("")

    # Zai_Range
    print("[TEST] Zai_Range")
    inputLIST = ['在昨天','在此時','在本社區','在此期間','收在胡適文存集','在國內七天猶豫期間']
    testLoki(inputLIST, ['Zai_Range'])
    print("")


if __name__ == "__main__":
    # 測試所有意圖
    #testIntent()

    # 測試其它句子
    #filterLIST = []
    #splitLIST = ["！", "，", "。", "？", "!", ",", "\n", "；", "\u3000", ";"]
    #resultDICT = execLoki("今天天氣如何？後天氣象如何？", filterLIST)            # output => ["今天天氣"]
    #resultDICT = execLoki("今天天氣如何？後天氣象如何？", filterLIST, splitLIST) # output => ["今天天氣", "後天氣象"]
    #resultDICT = execLoki(["今天天氣如何？", "後天氣象如何？"], filterLIST)      # output => ["今天天氣", "後天氣象"]

    inputSTR = "17曾道雄製作《台語創作歌曲之夜》在國家音樂廳演出"
    #inputSTR = input("請輸入要檢查的句子：")
    resultDICT = execLoki(inputSTR)

    """
    if resultDICT["Zai"] == []:
        print("\n再啦!為什麼不好好選字呢？")
    else:
        pass
    """

    print(resultDICT)