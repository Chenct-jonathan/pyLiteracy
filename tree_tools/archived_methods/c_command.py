#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ArticutAPI import Articut
from dataclasses import dataclass
from pprint import pprint
from typing import Optional, Tuple, Callable, Union, TypeVar, Generic, Any

import copy
import json
import re
import os

class Static:
    def __new__(cls):
        raise TypeError('Static classes cannot be instantiated')

_E = TypeVar("_E")
_R = TypeVar("_R")
class Either(Generic[_E,_R]):
    pass
@dataclass
class Left(Either[_E,Any]):
    left: _E
@dataclass
class Right(Either[Any,_R]):
    right: _R


with open("account.info", "r", encoding="utf-8") as f:
    accountDICT = json.load(f)

username = accountDICT['username']
apikey   = accountDICT['apikey']
articut = Articut(username, apikey)

@dataclass
class Tree:
    left: str
    head: str
    comp: 'Union[str,Tree,list[str]]'
    
    def reverse_search(self, target, path=""):
        # Check if the current node's 'head' or 'left' matches the target
        if self.head == target:
            return f"{path}.head"
        elif self.left == target:
            return f"{path}.left"
        
        # Recursively search in the 'comp' if it exists and is a Tree instance
        if isinstance(self.comp, Tree):
            result = self.comp.reverse_search(target, f"{path}.comp")
            if result:
                return result

        # If the target isn't found at this level or in 'comp', return None
        return None    


    def c_command(self, commander: str, commandee: str ):
        commander_pos = f"self{self.reverse_search(commander)}"
        commandee_pos = f"self{self.reverse_search(commandee)}"
        
        #if commandee_pos in commander_pos: --> Trying to achieve this.
             #return True
         #else:
             #return False
        
        return [commander_pos, commandee_pos]
        

if __name__ == '__main__':
    realTree = Tree(left='',
                  head='∅',
                  comp=Tree(left=Tree(left='<ENTITY_noun>大家</ENTITY_noun><QUANTIFIER>都</QUANTIFIER><ACTION_verb>喜歡</ACTION_verb><FUNC_inner>的</FUNC_inner>',
                                  head='<ENTITY_pronoun>我</ENTITY_pronoun>',
                                  comp=''),
                          head='∅',
                          comp=Tree(left='<trace>Subj_trace</trace><TIME_day>昨天</TIME_day>',
                                    head='<ACTION_verb>吃</ACTION_verb><ASPECT>了</ASPECT>',
                                    comp=Tree(left='<trace>Subj_trace</trace>',
                                                 head='∅',
                                                 comp=Tree(left='',
                                                         head='<trace>V_trace</trace>',
                                                         comp=Tree(left='',
                                                                   head='<ENTITY_classifier>五碗</ENTITY_classifier>',
                                                                   comp=Tree(left='<ENTITY_noun>大家</ENTITY_noun><QUANTIFIER>都</QUANTIFIER><ACTION_verb>喜歡</ACTION_verb><ACTION_verb>吃</ACTION_verb><FUNC_inner>的</FUNC_inner>',
                                                                           head='<ENTITY_nouny>飯</ENTITY_nouny>',
                                                                           comp='')))))))
    
    result = realTree.reverse_search('<trace>Subj_trace</trace><TIME_day>昨天</TIME_day>')
    print(result)
    print(realTree.c_command("<ACTION_verb>吃</ACTION_verb><ASPECT>了</ASPECT>", "<ENTITY_nouny>飯</ENTITY_nouny>"))

