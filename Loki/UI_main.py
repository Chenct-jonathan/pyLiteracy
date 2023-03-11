#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
import json
import os
import re

from ArticutAPI import Articut
from Gua_Zai.Gua_Zai import execLoki

BASEPATH = os.path.dirname(os.path.abspath(__file__))
try:
    with open("{}/account.info".format(BASEPATH), encoding="utf-8") as f:
        accountDICT = json.load(f)
except:
    print("提示！！目前使用 Articut 每小時公用字數中！！")
    accountDICT = {"username":"", "apikey":""}
pat = re.compile("</?\w+?_?\w*?>")
articut = Articut(username=accountDICT["username"], apikey=accountDICT["apikey"])
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/gua", methods=["POST"])
def zaiChecker():
    if request.method == "POST":# or request.method == "GET":
        sentenceLIST = []
        inputDICT = request.json
        inputSTR = inputDICT["inputSTR"]          #此行對應 .js 中的：payload["inputSTR"] = $("#inputSTR").val(); //將輸入區內的字串值載入 payload 中，給定 key 為 "inputSTR"
        if inputSTR.strip() == "":                #檢查一下，如果送空白字串上來，就回覆空字串。
            return jsonify({"returnData":""})

        articutDICT = articut.parse(inputSTR)     #如果不是空字串，就把字串送給 Articut 處理以便斷句。
        if articutDICT["status"] == True:         #若斷句結果正常結束，就繼續往下走。否則就回覆 jsonify() 後的結果。
            pass
        else:
            return jsonify({"returnData": articutDICT["msg"]})

        for i in articutDICT["result_pos"]:       #將 Articut 處理後的每一句，送入 Loki 模型中處理。
            if len(i) <= 1:
                sentenceLIST.append(i)
            elif "<FUNC_inner>在</FUNC_inner>" in i or "<ASPECT>在</ASPECT>" in i:
                checkResultDICT = execLoki(inputSTR)
                if checkResultDICT["Zai"] != []:
                    sentenceLIST.append(re.sub(pat, "", i))
                else:
                    if "<FUNC_inner>在</FUNC_inner>" in i:
                        i = re.sub(pat, "", i.replace("<FUNC_inner>在</FUNC_inner>", "<FUNC_inner>在</FUNC_inner>[sub][再]啦！[/sub]".format(i))).replace("[sub]", "<sub>").replace("[/sub]", "</sub>")
                    else: #"<ASPECT>在</ASPECT>"
                        i = re.sub(pat, "", i.replace("<ASPECT>在</ASPECT>" , "<ASPECT>在</ASPECT>[sub][再]啦！[/sub]".format(i))).replace("[sub]", "<sub>").replace("[/sub]", "</sub>")
                    sentenceLIST.append(i)
                    app.logger.info("變成{}".format("".join(sentenceLIST)))
            else:
                sentenceLIST.append(re.sub(pat, "", i))
        response = jsonify({"checkResult":"<br>".join(sentenceLIST)})    #將最終結果以 jsonify() 包裝後回傳到前端 .js
        return response

if __name__ == "__main__":
    app.run(debug=True)