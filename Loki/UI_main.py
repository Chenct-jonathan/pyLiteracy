#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from flask import Flask
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
def test():
    return render_template("homepage.html")

@app.route("/gua", methods=["POST", "GET"])
def zaiChecker():
    if request.method == "POST" or request.method == "GET":
        sentenceLIST = []
        inputSTR = request.values["inputSTR"]
        articutDICT = articut.parse(inputSTR)
        for i in articutDICT["result_pos"]:
            if len(i) <= 1:
                sentenceLIST.append(i)
            elif "<FUNC_inner>在</FUNC_inner>" in i or "<ASPECT>在</ASPECT>" in i:
                checkResultDICT = execLoki(inputSTR)
                if checkResultDICT["Zai"] == "":
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
        return "".join(sentenceLIST)

if __name__ == "__main__":
    app.run(debug=True)