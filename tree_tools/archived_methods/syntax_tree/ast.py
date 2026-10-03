from __future__ import annotations

from typing import Callable, TypeVar
from syntax_tree.type import TokenOfPos

from dataclasses import dataclass

_A,_B,_C,_T = TypeVar('_A'),TypeVar('_B'),TypeVar('_C'),TypeVar('_T')


""" Haskell ast:
data RuleTerm = TokenOfPOS str
              | RuleName str
              | Alt list[RuleTerm]
              | Seq list[RuleTerm]

              | Opt RuleTerm 
              | Many Optional[int] RuleTerm

data RuleDef = RuleDef {ruleName:str, ruleTerm:RuleTerm}
"""


class RuleTerm:
    d: tuple
    __ctor: Callable
    def __init__(self,ctor:Callable[...,RuleTerm],d:tuple):
        self.d = d
        self.__ctor = ctor
    def match(self,
                posToken: Callable[[str],_T],
                ruleName: Callable[[str],_T],
                alt:Callable[[list[RuleTerm]],_T],
                seq:Callable[[list[RuleTerm]],_T],
                # opt:Callable[[RuleTerm],_T],
                )->_T:
        if self.__ctor == PosToken:
            return posToken(*self.d)
        elif self.__ctor == RuleName:
            return ruleName(*self.d)
        elif self.__ctor == Alt:
            return alt(*self.d)
        elif self.__ctor == Seq:
            return seq(*self.d)
        # elif self.__ctor == Opt:
        #     return opt(*self.d)
        else:
            raise Exception(f'Failed to pattern match {str(self)}.')
    
    def iscase(self,thecase:Callable):
        return self.__ctor == thecase

    def __repr__(self):
        if self.__ctor == PosToken:
            return f'PosToken({self.d})'
        elif self.__ctor == RuleName:
            return f'RuleName({self.d})'
        elif self.__ctor == Alt:
            return f'Alt({self.d})'
        elif self.__ctor == Seq:
            return f'Seq({self.d})'

def PosToken(a1:str)->RuleTerm:
    return RuleTerm(PosToken,(a1,))
def RuleName(a1:str)->RuleTerm:
    return RuleTerm(RuleName,(a1,))
def Alt(a1:list[RuleTerm])->RuleTerm:
    return RuleTerm(Alt,(a1,))
def Seq(a1:list[RuleTerm])->RuleTerm:
    return RuleTerm(Seq,(a1,))
# def Opt(a1:RuleTerm)->RuleTerm:
#     return RuleTerm(Opt,(a1,))


@dataclass
class RuleDef:
    ruleName:str
    ruleTerm:RuleTerm

