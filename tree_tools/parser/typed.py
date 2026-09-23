from typing import Generic, TypeVar, Union, Any, Callable, TypeGuard

import parsy

_S,_A,_T = TypeVar('_S'),TypeVar('_A'),TypeVar('_T')



class Parser(Generic[_S,_A],parsy.Parser):
    def parse(self,stream: Union[str, bytes, list[_S]])->_A:
        return super().parse(stream)
    def parse_partial(self, stream: Union[str, bytes, list[_S]]) -> tuple[Any, Union[str, bytes, list[_S]]]:
        return super().parse_partial(stream)
    def bind(self, bind_fn: Callable[[_A], 'Parser[_S,_T]'])->'Parser[_S,_T]':
        x = super().bind(bind_fn)
        x.__class__ = Parser
        return x
    
def from_parsy(p:parsy.Parser)-> Parser[Any,Any]:
    return p