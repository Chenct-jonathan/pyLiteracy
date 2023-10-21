#!/user/bin/env python
# -*- coding: utf-8 -*-

import logging
import discord
import json
import re
from datetime import datetime
from pprint import pprint

from Gua_Zai.Gua_Zai import runLoki, execLoki
from ArticutAPI import Articut

accountDICT = json.load(open("../account.info",encoding="utf-8"))
articut = Articut(username=accountDICT["username"],apikey=accountDICT["apikey"])

logging.basicConfig(level=logging.DEBUG)

punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
def getLokiResult(inputSTR):
    punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
    inputLIST = punctuationPat.sub("\n", inputSTR).split("\n")
    filterLIST = []
    resultDICT = runLoki(inputLIST, filterLIST)
    logging.debug("Loki Result => {}".format(resultDICT))
    return resultDICT

class BotClient(discord.Client):

    def resetMSCwith(self, messageAuthorID):
        '''
        清空與 messageAuthorID 之間的對話記錄
        '''
        templateDICT = self.templateDICT
        templateDICT["updatetime"] = datetime.now()
        return templateDICT

    async def on_ready(self):
        # ################### Multi-Session Conversation :設定多輪對話資訊 ###################
        self.templateDICT = {"updatetime" : None,
                             "latestQuest": ""
        }
        self.mscDICT = { #userid:templateDICT
        }
        # ####################################################################################
        print('Logged on as {} with id {}'.format(self.user, self.user.id))

    async def on_message(self, message):
        # Don't respond to bot itself. Or it would create a non-stop loop.
        # 如果訊息來自 bot 自己，就不要處理，直接回覆 None。不然會 Bot 會自問自答個不停。
        if message.author == self.user:
            return None
        logging.debug("收到來自 {} 的訊息".format(message.author))
        logging.debug("訊息內容是 {}。".format(message.content))
        if self.user.mentioned_in(message):
            replySTR = "我是預設的回應字串…你會看到我這串字，肯定是出了什麼錯！"
            logging.debug("本 bot 被叫到了！")
            msgSTR = message.content.replace("<@{}> ".format(self.user.id), "").strip()
            logging.debug("人類說：{}".format(msgSTR))
            if msgSTR == "ping":
                replySTR = "pong"
            elif msgSTR == "ping ping":
                replySTR = "pong pong"

# ##########初次對話：這裡是 keyword trigger 的。
            elif msgSTR.lower() in ["哈囉","嗨","你好","您好","hi","hello"]:
                #有講過話(判斷對話時間差)
                if message.author.id in self.mscDICT.keys():
                    timeDIFF = datetime.now() - self.mscDICT[message.author.id]["updatetime"]
                    #有講過話，但與上次差超過 5 分鐘(視為沒有講過話，刷新template)
                    if timeDIFF.total_seconds() >= 300:
                        self.mscDICT[message.author.id] = self.resetMSCwith(message.author.id)
                        replySTR = "嗨嗨，我們好像見過面，但卓騰的隱私政策不允許我記得你的資料，抱歉！"
                    #有講過話，而且還沒超過5分鐘就又跟我 hello (就繼續上次的對話)
                    else:
                        replySTR = self.mscDICT[message.author.id]["latestQuest"]
                #沒有講過話(給他一個新的template)
                else:
                    self.mscDICT[message.author.id] = self.resetMSCwith(message.author.id)
                    replySTR = "{}！我是 pyLiteracy！讓我來檢查你的中文吧！".format(msgSTR.title())

# ##########非初次對話：這裡用 Loki 計算語意
            else: #開始處理正式對話
                #從這裡開始接上 NLU 模型
                sentenceLIST = []
                #rmPat = re.compile("[^<a-zA-Z/_>]")
                pat = re.compile("</?\w+?_?\w*?>")
                if msgSTR.strip() == "<@1096713732983357510>": #檢查一下，如果送空白字串上來，就回覆空字串。
                    replySTR = "How can I help you?"
                else:
                    #print("msgSTR：{}".format(msgSTR))
                    articutDICT = articut.parse(msgSTR)
                    if articutDICT["status"] == True:
                        #print(" Articut 處理結果：{}".format(articutDICT["result_pos"]))
                        for i in articutDICT["result_pos"]: #將 Articut 處理後的每一句，送入 Loki 模型中處理。
                            #print("正在檢查下列文字：「{}」。".format(i))
                            if len(i) <= 1:
                                sentenceLIST.append(i)
                                #print("{} 不是句子。".format(i))
                            elif "<FUNC_inner>在</FUNC_inner>" in i or "<ASPECT>在</ASPECT>" in i:
                                checkSTR = re.sub(pat, "", i)
                                #print("「{}」裡面有「在」。".format(checkSTR))
                                checkResultDICT = execLoki(checkSTR)
                                if checkResultDICT["Zai"] != []:
                                    #print("這句沒有錯誤。")
                                    sentenceLIST.append(checkSTR)
                                else:
                                    if "<FUNC_inner>在</FUNC_inner>" in i:
                                        checkSTR = checkSTR.replace("在", " `在>再` ")
                                        #print("修正為：「{}」。".format(checkSTR))
                                    else: #"<ASPECT>在</ASPECT>"
                                        checkSTR = checkSTR.replace("在", " `在>再` ")
                                        #print("修正為：「{}」。".format(checkSTR))
                                    sentenceLIST.append(checkSTR)
                            else:
                                checkSTR =  ''.join(re.sub(pat, "", i))
                                sentenceLIST.append(checkSTR)                        
                        replySTR = "檢查結果如下：「{}」".format(''.join(sentenceLIST))        
                    
                    else:
                        replySTR = "Somethine must be wrong with your message！"
        await message.reply(replySTR)


if __name__ == "__main__":
    with open("../account.info", encoding="utf-8") as f: #讀取account.info
        accountDICT = json.loads(f.read())
    client = BotClient(intents=discord.Intents.default())
    client.run(accountDICT["discord_token"])