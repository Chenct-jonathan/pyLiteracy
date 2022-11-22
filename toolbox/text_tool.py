#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def textPurger(tagInputSTR):
    rawInputSTR = tagInputSTR.replace(" ", "").replace("&gt","").replace("&lt","").replace("<s>","").replace("</s>","")
    return rawInputSTR

