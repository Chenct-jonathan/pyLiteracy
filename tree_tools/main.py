from ArticutAPI import Articut
import json
import re
import pprint as pp
import parsy
from typing import Optional, TypeVar, Generic, Literal, Union
from itertools import chain, starmap,groupby
from functools import partial
from dataclasses import dataclass
from collections.abc import Sequence, Callable, Iterable

#from syntax_tree import *

username = ""
apikey   = ""

with open('DROIDTOWN.json') as f:
    try:
        r = json.load(f)
        username = r["username"]
        apikey = r["key"]
    except:
        raise Exception("Please fill the DROIDTOWN.json file (an object with \"username\" and \"key\" fields).)")

articut = Articut(username, apikey)

#inputSTR = "戴克斯的原始版本僅適用於找到兩個頂點之間的最短路徑"
inputSTR= '蓼葉堇菜（學名：）是堇菜科堇菜屬的植物。分布在朝鮮以及中國大陸的吉林等地，生長於海拔650米至900米的地區，一般生長在山地疏林中，目前尚未由人工引種栽培。'
# resultDICT = articut.parse(inputSTR, level="lv2")

# pp.pprint(articut.getVerbStemLIST(resultDICT))
# with open("sample.json", "w",encoding='utf-8') as outfile:
#     json.dump(resultDICT, outfile, ensure_ascii=False, indent=4)

# resultDICT = {}
# with open('sample.json','r+') as f:
#     resultDICT = json.load(f)

# # trying the groupby function
# things = [("animal", "bear"), ("animal", "duck"), ("plant", "cactus"), ("vehicle", "speed boat"), ("vehicle", "school bus")]
# groups = [list(group) for key,group in groupby(things, lambda x: x[0])]

class CC():
    def __class_getitem__()