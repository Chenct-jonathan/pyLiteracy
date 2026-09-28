from __future__ import annotations

from typing import Sequence, Union, Optional
from itertools import chain
from .treeart import binary_edge


class TokenOfPos:
    pos : str
    text : str
    def __init__(self,pos:str,text:str):
        self.pos = pos
        self.text = text
    def __str__(self):
        return f'{self.pos}({self.text})'
    def __repr__(self):
        return f'TokenOfPos({self.pos},{self.text})'

class RoseTree:
    children:list['RoseTree']
    def __init__(self,content, children:Sequence['RoseTree']=[]):
        self.content = content
        self.children = list(children)

    def copy(self)->RoseTree:
        "The content will be the reference if it's an object."
        if len(self.children)==0:
            return RoseTree(self.content,[])
        else:
            return RoseTree(self.content, 
                            list(map(RoseTree.copy, self.children)))
        
    def compactFormatStr(self, layerLength=6)->str:
        def render(tree:RoseTree)->list[str]:
            if len(tree.children)==0:
                return [str(tree.content)]
            else:
                contLen = len(tree.content)
                padding = contLen-layerLength+1 if contLen>=layerLength else 0
                        # +1 is an additional "_" character to separate parent and child nodes
                contentStr = str(tree.content).ljust(layerLength+padding, '_')
                newLayerLength = layerLength+padding

                def prependingFirstLeaf(leaf:str)->str:
                    return contentStr + leaf
                def prependingHead(leaf:str)->str:
                    return '|'.ljust(newLayerLength, '_') + leaf
                def prependingNonchildLeaf(leaf:str)->str:
                    return '|'.ljust(newLayerLength, ' ') + leaf
                def prependingEnd(leaf:str)->str:
                    return ' '.ljust(newLayerLength, ' ') + leaf
                
                def renderFirstChild(t:RoseTree)->list[str]:
                    allLeaves = render(t)
                    return [ prependingFirstLeaf(allLeaves[0])
                        , *map(prependingNonchildLeaf,allLeaves[1:])]
                def renderMiddleChildren(t:RoseTree)->list[str]:
                    allLeaves = render(t)
                    return [ prependingHead(allLeaves[0])
                        , *map(prependingNonchildLeaf,allLeaves[1:])]
                def renderLastChild(t:RoseTree)->list[str]:
                    allLeaves = render(t)
                    return [ prependingHead(allLeaves[0])
                        , *map(prependingEnd,allLeaves[1:])]
                def renderSoleChild(t:RoseTree)->list[str]:
                    allLeaves = render(t)
                    return [ prependingFirstLeaf(allLeaves[0])
                        , *map(prependingEnd,allLeaves[1:])]
                
                if len(tree.children) > 1:
                    return [ *renderFirstChild(tree.children[0])
                        , *chain(*map(renderMiddleChildren, tree.children[1:-1]))
                        , *renderLastChild(tree.children[-1])
                        ]
                else: #len(tree.children)==1
                    return renderSoleChild(tree.children[0])

        return "\n".join(render(self))


class SyntaxTree(RoseTree):
    content : Union[str,TokenOfPos] #str is for phrase
    children : list['SyntaxTree']
    parent : Optional['SyntaxTree']
    def __init__(self,content:Union[str,TokenOfPos], children:list['SyntaxTree'] = [], parent:Optional['SyntaxTree'] = None):
        self.content = content
        self.children = children
        self.parent = parent
        
    def addChild(self,child:'SyntaxTree'):
        self.children.append(child)
        child.parent = self
    def addChildren(self,children:list['SyntaxTree']):
        for child in children:
            self.addChild(child)
    def registerParentInfo(self)->'SyntaxTree':
        """
        Used to update parenthood info to a non-parent-registered tree.
        """
        for c in self.children:
            c.parent = self
            if isinstance(c.content, str):
                c.registerParentInfo()
        return self
    
    def copy(self)->'SyntaxTree':
        if len(self.children)==0:
            return SyntaxTree(self.content,children=[],parent=self.parent)
        else:
            return SyntaxTree(self.content, 
                              list(map(SyntaxTree.copy, self.children)), 
                              self.parent)

    def __repr__(self):
        return f"Tree({self.content},{self.children})"
    def compactFormatStr(self, layerLength=6) -> str:
        return super().compactFormatStr(layerLength)
    def ppstr(self, *args):
        return self.compactFormatStr(*args)
    
    def _is_binarytree(self)->bool:
        child_num = len(self.children)
        if child_num == 0:
            return True
        elif child_num == 1 or child_num > 2:
            return False
        else:
            return self.children[0]._is_binarytree() \
                   and self.children[1]._is_binarytree()
    
    def bin_str(self):
        def f(t:SyntaxTree)->str:
            if t.children:
                return binary_edge(str(t.content), f(t.children[0]), f(t.children[1]), align='center')
            else:
                return str(t.content)
        return f(self) if self._is_binarytree() else ""



    def pprint(self, *args):
        bin_str = self.bin_str()
        if bin_str:
            print(bin_str)
        else:
            print(self.compactFormatStr(*args))
    