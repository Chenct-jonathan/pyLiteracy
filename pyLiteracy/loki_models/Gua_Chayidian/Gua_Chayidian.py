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
                    "msg": "No Match Intent!"
                }
            ]
        }
"""


from requests import post
from requests import codes
import math
import json
import re
try:
    from intent import Loki_adv_sinica_chayidian
    from intent import Loki_ad_hoc_chayidian
    from intent import Loki_adv_extend_chayidian
except:
    from .intent import Loki_adv_sinica_chayidian
    from .intent import Loki_ad_hoc_chayidian
    from .intent import Loki_adv_extend_chayidian


with open("account.info", "r", encoding="utf-8") as f:
    accountDICT = json.load(f)
            
LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
USERNAME = accountDICT["username"]
LOKI_KEY = accountDICT["lokikey"]
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
       #"key": []
    }
    lokiRst = LokiResult(inputLIST, filterLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # adv_sinica_chayidian
                if lokiRst.getIntent(index, resultIndex) == "adv_sinica_chayidian":
                    resultDICT = Loki_adv_sinica_chayidian.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getPattern(index, resultIndex), resultDICT)

                # ad_hoc_chayidian
                if lokiRst.getIntent(index, resultIndex) == "ad_hoc_chayidian":
                    resultDICT = Loki_ad_hoc_chayidian.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getPattern(index, resultIndex), resultDICT)

                # adv_extend_chayidian
                if lokiRst.getIntent(index, resultIndex) == "adv_extend_chayidian":
                    resultDICT = Loki_adv_extend_chayidian.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getPattern(index, resultIndex), resultDICT)

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
    # adv_sinica_chayidian
    print("[TEST] adv_sinica_chayidian")
    inputLIST = ['差一點昏倒','差一點就沒命了','差一點遭到截肢','差一點陰溝裡翻船','否則差一點看不到新中國','雖然差一點而沒挑戰成功','差一點沒把手指頭當菜切了','她差一點栽在印度芭娜姬的手中','差一點提前引爆華隆跳票的引信','差一點就讓這種傳統工藝走不回來','差一點把爸爸心愛的上等酒給打翻了','只差一點沒和那漂亮女人做成一回好事','差一點他那神父爸爸便不能認這個孩子','最後還差一點就當選高雄區的立法委員','爭三連霸的瑞典名將艾柏格則差一點落馬','謝長亨差一點就是中華職棒第一個「選秀狀元」']
    testLoki(inputLIST, ['adv_sinica_chayidian'])
    print("")

    # ad_hoc_chayidian
    print("[TEST] ad_hoc_chayidian")
    inputLIST = ['即使差一點','若是評估質素差一點的','還差一點旅行社才開門辦公','這些胎生的小苗萬一在第一次落下運氣差一點']
    testLoki(inputLIST, ['ad_hoc_chayidian'])
    print("")

    # adv_extend_chayidian
    print("[TEST] adv_extend_chayidian")
    inputLIST = ['差一點站不穩','差一點被截肢','差一點跑不動','差一點就沒時間了','差一點就使這種傳統工藝走不回來','差一點沒和那漂亮女人看一部電影','差一點他那神父爸爸便看到這個孩子']
    testLoki(inputLIST, ['adv_extend_chayidian'])
    print("")


if __name__ == "__main__":
    inputSTR = input("input utterance : \n (按下 enter 查看 Sinica Corpus 分析結果)")
    if inputSTR == "":
        with open("test_data.txt", encoding="utf-8") as k:
            lines = ''.join(k.readlines()).split("\n")
            for i in range(len(lines)):
                inputSTR = lines[i]
                print("{}:".format(i+1))
                resultDICT = runLoki([inputSTR])#,filter = ["ad_hoc_chayidian"])
                print("說明：")
                if "reason" in resultDICT.keys():
                    print("\t{}".format(resultDICT["reason"]))
                    if "key" in resultDICT.keys():
                        print("\t註：{}帶有一語意錨點。".format(resultDICT["key"]))
                    else:
                        pass
                else:
                    print("根據 sinica corpus 平衡與料庫，此語句似乎不能和 [差一點] 連用")
                    print("若與您的語感判斷結果不相符，請聯繫 chenjonathan901210@gmail.com")
    else:
        resultDICT = runLoki([inputSTR])#,filter = ["ad_hoc_chayidian"])
        print("說明：")
        if "reason" in resultDICT.keys():
            print("\t{}".format(resultDICT["reason"]))
            if "key" in resultDICT.keys():
                print("\t註：{}帶有一終點。".format(resultDICT["key"]))
            else:
                pass
        else:
            print("根據 sinica corpus 平衡與料庫，此語句似乎不能和 [差一點] 連用")
            print("若與您的語感判斷結果不相符，請聯繫 chenjonathan901210@gmail.com")
    '''
    
    inputSTR = "差一點吃掉了"
    resultDICT = runLoki([inputSTR])#,filter = ["ad_hoc_chayidian"])
    print("說明：")
    if "reason" in resultDICT.keys():
        print("\t{}".format(resultDICT["reason"]))
        if "key" in resultDICT.keys():
            print("\t註：{}帶有一終點。".format(resultDICT["key"]))
        else:
            pass
    else:
        print("根據 sinica corpus 平衡與料庫，此語句似乎不能和 [差一點] 連用")
        print("若與您的語感判斷結果不相符，請聯繫 chenjonathan901210@gmail.com")
        print(resultDICT)    
        
    '''