#!/usr/bin/env python3
# -*- coding:utf-8 -*-

try:
    from loki_models.Gua_Zai import Gua_Zai
except:
    from .loki_models.Gua_Zai import Gua_Zai    
#try:
    #from loki_models.Gua_Zai import Gua_Zai
#except:
    #from .loki_models.Gua_Zai import Gua_Zai

from ArticutAPI import Articut
from pprint import pprint
import re
import json
import os

"""
from Pyl import PyL

x  = PyL(apikey,username)
x.check()

def check(str,apikey)
  articut(apikey)
  ...
  str....

class PyL:
  key:str
  def __init__(self,key):
    self.key = key

  def check(self,str):
    ....articut(self.key)
    ...

inst = PyL(key)
inst.check(str)

"""

BASEPATH = os.path.dirname(os.path.abspath(__file__))

class PyLiteracy:
    def __init__(self, username=None, apikey=None, lokiDICT=None, gaikey=""):
        if username == None or apikey == None or lokiDICT == None:
            try:
                with open("{}/account.info".format(BASEPATH), "r") as f:
                    userDICT = json.loads(f.read())
                self.username = userDICT["username"]
                self.apikey = userDICT["apikey"]
                self.lokikey = userDICT["lokiDICT"]
            except:
                self.username = "chenjonathan901210@gmail.com"
                self.apikey = "l#QmFaassWUs&p@vP#9RS^sfGQ*!qlW"
                self.lokiDICT = {
                    "Gua_zai":"&Srr55Ulq4BuEixXgcqyjpv6-ryrufN"
                }

        self.gaikey = ""

    def check(self, inputSTR):
        articut = Articut(self.username, self.apikey)
        articutDICT = articut.parse(inputSTR)
        sentenceLIST = []
        errorLIST = []
        pat = re.compile("</?\w+?_?\w*?>")
        if articutDICT["status"] == True:
            for i in articutDICT["result_pos"]:
                if len(i) <= 1:
                    sentenceLIST.append(i)
                elif "<FUNC_inner>在</FUNC_inner>" in i or "<ASPECT>在</ASPECT>" in i:
                    checkSTR = re.sub(pat, "", i)
                    checkResultDICT = Gua_Zai.execLoki(checkSTR)
                    if checkResultDICT["Zai"] != []:
                        sentenceLIST.append(checkSTR)
                    else:
                        errorLIST.append(checkSTR)
                        if "<FUNC_inner>在</FUNC_inner>" in i:
                            checkSTR = checkSTR.replace("在", "[在>再]")
                        else:
                            checkSTR = checkSTR.replace("在", "[在>再]")
                        sentenceLIST.append(checkSTR)
                else:
                    checkSTR =  ''.join(re.sub(pat, "", i))
                    sentenceLIST.append(checkSTR)
            resultSTR = "「{}」".format(''.join(sentenceLIST))
        else:
            resultSTR = "error"

        resultDICT = {
            "status": True,
            "msg": "",
            "check": {"error_sentence":errorLIST},
            "proofread": "",
            "result": resultSTR
        }

        return resultDICT

    def proofread(inputSTR, username, apikey, lokikey):
        pass

if __name__ == '__main__':
    pyLite =  PyLiteracy()
    resultDICT = pyLite.check(inputSTR="你在做一次試看看。你在幹嘛?")
    pprint(resultDICT)