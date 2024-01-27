from pyLiteracy import PyLiteracy
from pprint import pprint

pylite = PyLiteracy()

inputSTR = "你在做一次試看看。你在幹嘛?"
resultDICT = pylite.check(inputSTR)

pprint(resultDICT)