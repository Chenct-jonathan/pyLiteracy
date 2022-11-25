#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from argparse import ArgumentParser
from pprint import pprint
from requests import post
from time import sleep
import json


def addUtterance(payloadDICT):
    url = "https://api.droidtown.co/Loki/Command/"

    for i in range(0, len(payloadDICT["utterance"]), 20):
        payload = {
            "username" : payloadDICT["username"],
            "loki_key" : payloadDICT["loki_key"],
            "intent"   : payloadDICT["intent"],
            "utterance": payloadDICT["utterance"][i:i+20]
        }
        response = post(url, json=payload).json()
        
        if response["status"] == True:
            sleep(0.5)
        else:
            return response["msg"]
    
    return response


def listUtterance(payloadDICT):
    url = "https://api.droidtown.co/Loki/Utterance/"

    for i in range(0, len(payloadDICT["intent"]), 20):
        payload = {
            "username"    : payloadDICT["username"],
            "loki_key"    : payloadDICT["loki_key"],
            "intent_list" : payloadDICT["intent"][i:i+20]
        }
        response = post(url, json=payload).json()
        
        if response["status"] == True:
            sleep(0.5)
        else:
            return response["msg"]
    
    return response


# sub-command functions: au (Add Utterances)
def au(args):
    intent = args.intent
    jsonfile = args.jsonfile

    payloadDICT = json.load(open("account.info"))
    
    payloadDICT["intent"] = intent
    payloadDICT["utterance"] = []
    
    jsnLIST = json.loads(open(jsonfile, encoding = 'utf8').read())
    
    for u in jsnLIST:
        payloadDICT["utterance"].append(u)
    
    if payloadDICT["utterance"] == []:
        print("Well...I don't see any utterance.")
    else:
        pprint(payloadDICT)
        
        response = addUtterance(payloadDICT)
        
        if response["status"] == True:
            pprint(response)
        elif response["status"] == False:
            print(response["msg"])


# sub-command functions: lu (List Utterances)
def lu(args):
    intent = args.intent

    payloadDICT = json.load(open("account.info"))

    payloadDICT["intent"] = [intent]
    response = listUtterance(payloadDICT)
    pprint(response)


if __name__== "__main__":
    """
    Basic usage:
        - To add utterances listed in the corpus to the Loki webpage:
        $ python3 LokiTool.py au -intent loc -jsonfile 
        
        - To list utterances in an intent in the Loki webpage:
        $ python3 LokiTool.py lu -intent loc
    """

    # create the top-level parser
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the "au" command ("au" stands for add utterance)
    parser_upload = subparsers.add_parser('au')
    parser_upload.add_argument("-intent", type=str, required=True)
    parser_upload.add_argument("-jsonfile", type=str, required=True)
    parser_upload.set_defaults(func=au)

    # create the parser for the "lu" command ("lu" stands for list utterance)
    parser_upload = subparsers.add_parser('lu')
    parser_upload.add_argument("-intent", type=str, required=True)
    parser_upload.set_defaults(func=lu)

    # parse the args and call whatever function was selected
    args = parser.parse_args()
    
    try:
        args.func(args)
    except AttributeError:
        parser.print_help()
        parser.exit()
        


        

