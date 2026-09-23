import csv
import json
from pprint import pprint


file_path = "raw_data.csv"
testLIST = []

with open(file_path, mode="r", encoding="utf-8") as csvFILE:
    raw_data = csv.reader(csvFILE)
    for i in raw_data:
        testLIST.extend(i)

pprint(testLIST)

with open("test_data.json", mode="w", encoding="utf-8") as jsonFILE:
    json.dump(testLIST, jsonFILE, ensure_ascii=False, indent=4)
    
    