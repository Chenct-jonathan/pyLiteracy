import json
import re
from pprint import pprint

with open("rep_zai.json", "r", encoding="utf-8") as f:
    uDICT = json.load(f)
    
#pprint(uDICT)
keyLIST = list(uDICT["utterance"].keys()) 

pprint(keyLIST)
pprint(len(keyLIST))


inputSTR = '''
def getResult(inputSTR, utterance, args, resultDICT, refDICT, pattern=""):
    debugInfo(inputSTR, utterance)
    if utterance == "1983年再向虎山行飾紀青雲":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if "<UserDefined>" in args[8]:
                if args[9] in userDefinedDICT["as_Verb"]:
                    resultDICT["rep"].append("rep")
                else:
                    pass
            else:
                resultDICT["rep"].append("rep")
                
    if utterance == "2013再戰明天飾懲教人員":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "不再如此":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if "<UserDefined>" in args[0]:
                if args[1] in userDefinedDICT["as_Mod"]:
                    resultDICT["rep"].append("rep")
                else:
                    pass
            else:
                resultDICT["rep"].append("rep")

    if utterance == "再不簽核就會來不及":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再也不怕忘記":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再前行150公尺":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再多帶幾包":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再將同學行李擺放至寢室內":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再強悍的防毒軟體也會有失靈的一天":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再把這些要素融會整理":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再接再厲":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再於課堂中提問":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再查查":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再與冷熱進水彎頭連接鎖緊":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再處其負責人新臺幣十萬元以上五十萬元以下罰鍰":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再行長期出租予企業客戶使用":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "再見":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "到國光路後右轉再前行":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "包妥好再一根一根的結合起來":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "又再一次的超越自己了":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "可享住宿再優惠9折2來店泡湯贈送養生茶乙壺":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "希望時間可以再長一點":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "臺中支局葉菸草再乾燥場建築群":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")

    if utterance == "請再慎重考量":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "再一家家比較高低":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            if args[0] == args[1]:
                resultDICT["rep"].append("rep")
            else:
                pass
            
    if utterance == "若於5年內再違反者":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "再上一層":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "再怎麼不喜歡":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "再發率":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "北門遊客中心再一新作":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "恕不再一一徵求同意":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "再因急降雨造成聚落淹水":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "結帳再84折":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "再保險":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")
            
    if utterance == "再低5-10度":
        if CHATBOT_MODE:
            resultDICT["response"] = getResponse(utterance, args)
        else:
            resultDICT["rep"].append("rep")    
'''

pat = re.compile(r'if utterance == "([\u4E00-\u9FFF 0-9a-zA-Z]+)":')
utterenceLIST = re.findall(pat, inputSTR)
pprint(utterenceLIST)
pprint(len(utterenceLIST))


unique_to_list1 = [item for item in keyLIST if item not in utterenceLIST]

# 找到 list2 中有但 list1 中沒有的元素
unique_to_list2 = [item for item in utterenceLIST if item not in keyLIST]

# 找到兩個列表中不同的元素
different_elements = unique_to_list1 + unique_to_list2

print("List1 中獨有的元素:", unique_to_list1)
print("List2 中獨有的元素:", unique_to_list2)
print("兩個列表中不同的元素:", different_elements)

pprint(utterenceLIST == keyLIST)