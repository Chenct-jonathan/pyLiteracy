
from dataclasses import dataclass
from typing import Any, Union, Generator, Optional, Literal, TypeVar

# prefix components:
_space =  '   '
_branch = '│  '
# pointers:
_tee =    '├──'
_last =   '└──'

HeadType = Literal['initial','final']


RangedStr = tuple[str, tuple[int,int]]


class Tree:
    # Range information is used for tree printing.
    left: 'Union[str,RangedStr,Tree,list[str]]'
    head: Union[str, RangedStr]
    comp: 'Union[str, RangedStr,Tree]'
    parent: 'Optional[Tree]' = None
    head_type: HeadType = 'initial'
    
    folded: bool = False

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name,value)
        if name in ['comp','left'] and isinstance(value,Tree):
            value.parent = self

    def __init__(self,l: 'Optional[Union[str,RangedStr,Tree,list[str]]]' = None
                     ,h: Optional[Union[str,RangedStr]] = None
                     ,c: 'Optional[Union[str,RangedStr,Tree]]' = None
                     ,*
                     ,head_type: Literal['initial', 'final'] = 'initial'
                     ,left: 'Optional[Union[str,Tree,list[str]]]' = None
                     ,head: Optional[Union[str,RangedStr]] = None
                     ,comp: 'Optional[Union[str,Tree]]' = None
                     ):
        """
        The constructor can only be used in two ways: 
        1. `Tree(l,h,c)` when `head_type='initial`
        2. `Tree(left=.., head=.., comp=..)`
        Two methods cannot be mixed.
        """
        if (not (l is None or h is None or c is None))\
           and (left is None and head is None and comp is None)\
           and head_type=='initial':
            #Tree(left,head,comp) when head_type=='initial'
            #DOES NOT ACCEPT Tree(l,h,c, head_type='final')
            self.left, self.head, self.comp = l, h, c
        elif (l is None and h is None and c is None)\
             and (not (left is None or head is None or comp is None)):
            #Tree(head=...,left=...,comp=..., head_type=...)
            self.left, self.head, self.comp = left, head, comp
        else:
            raise Exception('Wrong use of the Tree constructor. ')

    def __printTree(self, prefix: str="") -> Generator[str,None,None]:

        left_content = "left:" + (type(self.left).__name__ + f"[{self.left.head}]" 
                                   if isinstance(self.left, Tree)
                                   else f"\"{self.left}\"")
        yield prefix + _tee + left_content
        if isinstance(self.left, Tree): 
            yield from self.left.__printTree(prefix = prefix + _branch + "     ") 
        
        comp_content = "comp:" + (type(self.comp).__name__ + f"[{self.comp.head}]" 
                                   if isinstance(self.comp, Tree)
                                   else f"\"{self.comp}\"")
        yield prefix + _last + comp_content
        if isinstance(self.comp, Tree): 
            yield from self.comp.__printTree(prefix = prefix + _space + "     ") 

    def __printTreeLR(self) -> Generator[str,None,None]:
        ...

    def pstr(self) -> str:
        return (f"{type(self).__name__}[{self.head}]\n"+
                "\n".join(list(self.__printTree()))
               )
    def __str__(self) -> str:
        return self.pstr()
    def __repr__(self) -> str:
        return self.pstr()
    def pprint(self):
        print(self.pstr())


## the algorithm is taken from https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
# def tree(dir_path: Path, prefix: str=''):
#     contents = list(dir_path.iterdir())
#     # contents each get pointers that are ├── with a final └── :
#     pointers = [tee] * (len(contents) - 1) + [last]
#     for pointer, path in zip(pointers, contents):
#         yield prefix + pointer + path.name
#         if path.is_dir(): # extend the prefix and recurse:
#             extension = branch if pointer == tee else space 
#             # i.e. space because last, └── , above so no more |
#             yield from tree(path, prefix=prefix+extension)

class VP(Tree):
    pass
class ClsP(Tree):
    pass
class NP(Tree):
    pass
"""
example:

VP[吃]
├──left:他
└──comp:ClsP[五碗]
        ├──left:""
        └──comp:NP[飯]
                ├──left:""
                └──comp:""

                
                 ┌────""
         ┌─NP────┴───飯
         │  └─......
 ┌─ClsP─五碗
 │  └─""
VP───吃
 └─他
                 ┌────comp:""
         ┌─NP────┴───head:飯
         │  └─left:......
 ┌─ClsP─head:五碗
 │  └─left:""
VP───head:吃
 └─left:他
               

# full NP

              ┌──""
         ┌──N'┴─飯
    ┌──N'──香香的
 ┌─N'─軟軟的
NP──""
              ┌──comp:""
         ┌──N'┴────N:飯
    ┌──N'┴─adjt:香香的
 ┌─N'─adjt:軟軟的
NP──spec:""

       ┌───────""
NP─────┴──────飯
 └─軟軟的,香香的
       ┌───────comp:""
NP─────┴──────head:飯
 └─left:軟軟的,香香的

# AspP example and movement

input = "被騙了五千元"

        ┌────────────────────────了
        │              ┌─◁ 五千元
        │       ┌──VP──┴─騙
        │       │   └─""
  ┌─AspP┴LightVP┴被
  │  │    └─""
  │  └─""
IP─""
 └─""

                       ┌─◁ 五千元
        ┌─了           │
        │       ┌──VP──┴─騙
        │       │   └─""
  ┌─AspP┴LightVP┴被
  │  │    └─""
  │  └─""
IP─""
 └─""
             ┌──────────────────────comp:了
             │            ┌──comp◁ 五千元
             │  ┌──comp:VP───head:騙
             │  │        └──left:""
  ┌─comp:AspP┴LightVP-head:被
  │       │    └─left""
  │       └─left:""
IP─head:""
 └─left:""
        ┌───────────────────────< >
        │          ┌────◁ 五千元 ║
  ┌─AspP┴LightVP-VP──騙了<═══════╝
  │  │    │       └─""
  │  │    └─被
  │  └─""
IP─""
 └─""

"""



ex1 = VP(head = "吃"
        ,left = "他"
        ,comp = ClsP(head = "五碗"
                    ,left = ""
                    ,comp = NP(head = "飯"
                              ,left = ""
                              ,comp = ""  
                              )
                    )
        )

def swap(t1:Tree, field1:str, t2:Tree, field2:str):
    temp = t1.__dict__[field1]
    t1.__dict__[field1] = t2.__dict__[field2]
    t2.__dict__[field2] = temp

if __name__ == '__main__':
    pass