#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from Gua_Zai import execLoki

import json

with open("../../purged corpus/loc_zai_purged.json", encoding="utf-8") as jFILE:
    corpusLIST = list(json.load(jFILE).keys())

missingLIST = []

for c in corpusLIST[1301:2301]:
    resultDICT = execLoki(c)
    if resultDICT["Zai"] == []:
        print("Missing pattern: {}".format(c))
        missingLIST.append(c)

with open("missing_zai_1301-2300_revised.json", "w", encoding="utf-8") as jFILE:
    json.dump(missingLIST, jFILE, ensure_ascii=False, indent=4)
