#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from Gua_zai import execLoki

import json

with open("../../purged corpus/loc_zai_purged.json", encoding="utf-8") as jFILE:
    corpusLIST = list(json.load(jFILE).keys())

missingLIST = []

"""
c = "111 終於在8月26日發出「中字第十二號」備忘錄"
resultDICT = execLoki(c)
if resultDICT["Zai"] == []:
    print("hi")
    print("Missing pattern: {}".format(c))
    missingLIST.append(c)
"""

for c in corpusLIST[0:301]:
    resultDICT = execLoki(c)
    if resultDICT["Zai"] == []:
        print("Missing pattern: {}".format(c))
        missingLIST.append(c)

with open("missing_zai_0-300_revised.json", "w", encoding="utf-8") as jFILE:
    json.dump(missingLIST, jFILE, ensure_ascii=False, indent=4)
