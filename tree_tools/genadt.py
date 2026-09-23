#!/usr/bin/env python

# Version 0.1

from typing import Generic, TypeVar, Tuple, List, Literal, Optional, Dict, Iterable, Callable, Iterator, Sequence
from functools import partial
from itertools import chain,count,repeat
from dataclasses import dataclass
import hashlib
import sys
import io
import re
import parsy

from string import ascii_uppercase

NO_TYPEGUARD = True


_A = TypeVar('_A')
_upperCases : list[str] = [c for c in ascii_uppercase]
indent = "    "

# 
# Run this script with an argument of a filepath, 
# it will generate the python scripts according to the type definition written
# in string blocks starting with "adt:\n".
#
# The generated script will be appended to the block where the type is defined.
# Here is an example of defining a linked-list:
#
# """ adt:
#
# data Lst a = Nil
#            | Cons a (Lst a)
#
# """
# # The code below is generated according to the definition above; hash=...
# _A = TypeVar('_A')
# _T_ = TypeVar('_T_')
# class Lst(Generic[_A]):
#     "Is either Nil or Cons."
#     def match(self,*,
#               nil:_T_,
#               cons:Callable[[_A,'Lst[_A]'],_T_]
#               )->_T_:
#         ...

# class Nil(Lst[Any]):
#     def match(self,*,
#               nil:Callable[[],_T_],
#               cons:Callable[[_A,'Lst[_A]'],_T_]
#               )->_T_:
#         return nil()
# def isNil(x:Lst[Any])->TypeGuard[Nil]:
#     return type(x) is Nil
#
# class Cons(Generic[_A],Lst[_A]):
#     data:_A
#     tail:Lst[_A]
#     def __init__(self,data:_A,tail:Lst[_A]):
#         self.data = data
#         self.tail = tail
#     def match(self,*,
#               nil:_T_,
#               cons:Callable[[_A,'Lst[_A]'],_T_]
#               )->_T_:
#         return cons(self.data,self.tail)
# def isCons(x:Lst[_A])->TypeGuard[Cons[_A]]:
#     return type(x) is Cons
#
# # End of generated code

#TODO: 
#  - different ways of implementation: use inheritance, use Union type
#    - for new type annotation
#  - match
#  - add runtime type check
#  - handle comments in adt blocks
#  - adding Ctor.t function that takes a tuple as argument
#  - exception of calling the type constructors in the wrong way
#  - haskell syntax
#  - argparse:
#   - backup file: switch, clean
#   - typeguard option

def main():
    if len(sys.argv) != 2:
        print("Usage: python genadt.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    process_the_file(filename)
    print("Finished generating adts.")


def process_the_file(filename):
    try:
        with open(filename, 'r') as file:
            content_lines = file.readlines()
        
        """
        splitting the contents to: ...{adt decl}{maybe previously generated code}...
        """
        _1,_2 = fileP.parse(content_lines)
        adtblocks:List[AdtDeclBlock] = _1
        postlines:List[str] = _2

        processedAdts = list(map(ProcessedAdtBlock.fromAdtDecl, adtblocks))
        generated:str = \
            "".join(
                "".join(x.generate_code()) for x in processedAdts)

        with open(filename, 'w') as file:
            file.write(generated)
            file.writelines(postlines)
                    
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")




example="""
data Lst[a] = Nil
            | Cons(_:a, tail:Lst[a])
data Maybe[b] = Nothing
              | Just(_:b)
"""

def interleave(x:_A,it:Iterator[_A])->Iterator[_A]:
    return chain.from_iterable(zip(it,repeat(x)))

#----------------------------------------------------------------
#--------------------------- I. AST -----------------------------
#----------------------------------------------------------------
# AST data types for adt declaration
    

class TypeExpr:
    typeName:str
    args:List['TypeExpr']
    def __init__(self,typeName:str,args:List['TypeExpr']):
        self.typeName = typeName
        self.args = args
    def __str__(self) -> str:
        if self.args:#len>0
            return "{}[{}]".format(self.typeName, 
                                   ','.join(map(str,self.args)))
        else:
            return self.typeName

    def __repr__(self) -> str:
        return self.__str__()
    
    @classmethod
    def from_mere_typevars(cls,typename:str, tvs:List[str])->'TypeExpr':
        return TypeExpr(typename,[TypeExpr(tv,[]) for tv in tvs])
    
    def subst_with_dict(self,typeVar_map:Dict[str,str])->'TypeExpr':
        "This method MUTATES the fields."
        if self.args:#len>0
            for te in self.args:
                te.subst_with_dict(typeVar_map)
        else:
            x = typeVar_map.get(self.typeName)
            if x:
                self.typeName = x
        return self
    
    def copy(self)->'TypeExpr':
        return TypeExpr(self.typeName,[te.copy() for te in self.args])
    
    def extract_typevars(self)->Iterator[str]:
        """
        Return all TypeExprs that is kind * in terms of Haskell.
        (for example, the 'list' in 'list[a]' is kind (*->*), and 'a' is kind *)
        """
        if self.args:
            return chain.from_iterable(
                arg.extract_typevars() for arg in self.args)
        else:
            return iter([self.typeName])


class CtorArg:
    fieldName:str
    typ:TypeExpr
    def __init__(self,fieldName:str,typ:TypeExpr):
        self.fieldName = fieldName
        self.typ = typ
    def __str__(self):
        return self.fieldName+":"+str(self.typ)
    def __repr__(self) -> str:
        return self.__str__()
    def copy(self)->'CtorArg':
        return CtorArg(self.fieldName, self.typ.copy())

def lowercase_head(name:str)->str:
    return name[0].lower()+name[1:]

class Ctor:
    ctorName:str
    args:List[CtorArg]
    def __init__(self,ctorName:str,args:List[CtorArg]):
        """
        ctorName: leading by uppercase
        args: List[Tuple[lowercase identifier, type expression]]
        """
        self.ctorName = ctorName
        self.args = args
    def __str__(self):
        return "{}({})".format(
            self.ctorName,
            ','.join(map(str,self.args)) if self.args else ""
        )
    def __repr__(self) -> str:
        return self.__str__()
    def extract_typevars(self)->set[str]:
        return set(chain.from_iterable(
            arg.typ.extract_typevars() for arg in self.args))
    def copy(self)->'Ctor':
        return Ctor(self.ctorName, [ctarg.copy() for ctarg in self.args])
    


class DataDef:
    typeName:str
    typeVars:List[str]
    ctors:List[Ctor]
    def __init__(self,typeName:str,typeVars:List[str],ctors:List[Ctor]):
        """
        typeName: leading by uppercase
        typeVars: leading by lowercase
        """
        self.typeName = typeName
        self.typeVars = typeVars
        self.ctors = ctors
    def __str__(self):
        return "data {}{} = {}".format(
                    self.typeName,
                    f"[{','.join(self.typeVars)}]" if self.typeVars else "",
                    '\n\t| '.join(map(str,self.ctors))
                    )
    def __repr__(self) -> str:
        return self.__str__()
    
    def subst_with_dict(self,typeVar_map:Dict[str,str])->'DataDef':
        "Change the name of type variables according to the given table."
        for i,tv in enumerate(self.typeVars):
            x = typeVar_map.get(tv)
            if x:
                self.typeVars[i] = x
        typeVars_in_ctors = (x.typ for x in 
                                chain.from_iterable(ctor.args for ctor in self.ctors))
        for tv in typeVars_in_ctors:
            tv.subst_with_dict(typeVar_map)
        return self
    
    def copy(self)->'DataDef':
        return DataDef(self.typeName, self.typeVars.copy(), [ctor.copy() for ctor in self.ctors])




#----------------------------------------------------------------
#-------------- II. Parsers of adt decl block -------------------
#----------------------------------------------------------------
#ENTRY: parseAST

tokenize = lambda input:re.findall(r'data|[a-zA-Z_][\w]*|=|\||\(|\)|:|,|\[|\]',input)
###----------

#stream is List[token]
def parseAST(src: str)->List[DataDef]:
    stream = tokenize(src)
    return parseDataDef.many().parse(stream)


identifier = parsy.test_item(str.isidentifier,'identifier')
upIdentifier = parsy.test_item(lambda x:str.isidentifier(x) and 
                                        str.isupper(x[0]),
                               'uppercase headed identifier')
loIdentifier = parsy.test_item(lambda x:str.isidentifier(x) and 
                                        (str.islower(x[0]) or x[0]=='_'),
                               'lowercase headed identifier')
def token(tok:str)->parsy.Parser:
    return parsy.test_item(lambda x:x==tok,'token:"'+tok+'"')


def parenList(paren:Literal['()','[]'],p:parsy.Parser)->parsy.Parser: 
    "return the parser of the list of result of p"
    return token(paren[0]) >> p.sep_by(token(','),min=1) << token(paren[1])

def optParenList(paren:Literal['()','[]'],p:parsy.Parser)->parsy.Parser:
    """
    Is different from parenList.optional(). parenList.optional() will still pass
    if the content between the parenthesis is in wrong format.
    When optParenList receives any lparen, the rest of the stream must then be 
    the right format.
    """
    @parsy.generate
    def g():
        lp = yield parsy.peek(token(paren[0]).optional())
        if lp is None:
            return None
        else:
            return (yield parenList(paren,p))
    return g

#typeexpt:Parser[Tuple[str,List[str]]]
@parsy.generate
def typeExpr_vars_only():
    id = yield identifier
    param = yield optParenList('[]',loIdentifier)
    return (id, param if param else [])


#Parser[TypeExpr]
typeExprP = parsy.forward_declaration()
@parsy.generate
def _typeExprP():
    id = yield identifier
    param:Optional[List[TypeExpr]] = yield optParenList('[]',typeExprP) 
    return TypeExpr(id,param if param else [])
typeExprP.become(_typeExprP)


@parsy.generate
def ctorP():
    ctor = yield upIdentifier
    params: Optional[List[CtorArg]] =\
        yield optParenList('()', 
                parsy.seq((loIdentifier << token(':')),
                            typeExprP
                ).combine(CtorArg))
    return Ctor(ctor,params if params else [])

def combine_DataDef(dataname:Tuple[str,List[str]],ctors:List[Ctor])->DataDef:
    return DataDef(dataname[0], dataname[1], ctors)
parseDataDef = parsy.seq(
    _data =    token('data'),
    dataname = typeExpr_vars_only,
    _eq =      token('='),
    ctors =    ctorP.sep_by(token('|'),min=1)
).combine_dict(combine_DataDef)




#----------------------------------------------------------------
#------------------- III. Code generation -----------------------
#----------------------------------------------------------------
# ENTRY: generate_code_of_datadefs: List[DataDef] -> Iterator[str]


def generate_code_of_datadefs(datas:List[DataDef])->Iterator[str]:
    # construct the typevar map
    # the idea: the typevar in ast map to an actual typevar name
    typevar_num = max(*(len(dd.typeVars) for dd in datas)) \
                    if len(datas)>1 else len(datas[0].typeVars)
    typevar_list = typevarList(typevar_num)
    
    subst_datas = [data.copy().subst_with_dict(typevarMap(typevar_list, data)) 
                   for data in datas]
    
    return chain(
        gen_aux(typevar_list),
        chain.from_iterable(
            gen_one_DataDef(data) for data in subst_datas)
    )



def typevarList(n:int)->List[str]:
    "Generate the list: _A,_B,_C..,_A1,_B1...,_A2,_B2,..."
    it = ('_'+x for x in
            chain(# chain: *Iterable[T] -> Iterable[T]
                _upperCases,
                chain.from_iterable(# from_iterable: Iterable[Iterable[T]]->Iterable[T]
                    #Iterable[Iterable[str]]
                    ((x+str(i) for x in _upperCases) for i in
                        count(1)))
            )
        )
    return [next(it) for _ in range(n)]

def typevarMap(typevars:List[str],data:DataDef)->Dict[str,str]:
    return dict(zip(data.typeVars,
                    typevars))

def gen_aux(typevars:List[str])->List[str]:
    "Generate TypeVar declarations"

    return [ "from typing import TypeVar,Generic,Callable"\
                +("" if NO_TYPEGUARD else ",TypeGuard"),
             ','.join(typevars)\
                 + (" = " if typevars else "")\
                 + ','.join(map(lambda t:f"TypeVar('{t}')", typevars)),
             "_T_ = TypeVar('_T_')"
           ]

def wrap_recursive_type(t:TypeExpr, rt:str)->str:
    """
    If t has any reference to rt, then t should be wrapped as a string.
    For example, when defining the class `Lst`, all the occurrences of `Lst`
    should be wrapped like `'Lst[int]'`, `'Lst[Lst[Any]]'`.
    """
    def exist_rt(te:TypeExpr)->bool:
        if te.typeName == rt:
            return True
        else:
            return any(exist_rt(tt) for tt in te.args)
    
    if exist_rt(t):
        return f"'{str(t)}'"
    else:
        return str(t)

def ctorMatchSignature(retType:str, rectype:str)->Callable[[Ctor],str]:
    "example: Cons ==> 'cons:Callable[[_T,Lst[_T]],Lst[_T]]'"
    def f(ctor:Ctor)->str:
        return "{}: Callable[[{}], {}],"\
                .format(lowercase_head(ctor.ctorName),
                        ','.join(wrap_recursive_type(arg.typ, rectype) 
                                    for arg in ctor.args),
                        retType
                )
    return f

def gen_match_signature( dataDef:DataDef)->Iterator[str]:
    "Generate the match method's def clause and type signature."
    return chain(
        ["def match(self,*,"],
        ("          "+line for line in 
            map(ctorMatchSignature('_T_', dataDef.typeName), 
                dataDef.ctors)),
        ["         )->_T_:"]
    )
    
def gen_typedef(dataDef:DataDef)->Iterator[str]:
    "Generate the class for the type, e.g., List"
    ctors = dataDef.ctors
    inherit_part = "(Generic[{}])".format(','.join(dataDef.typeVars))\
                        if dataDef.typeVars else ""
    
    #description
    ctorNum = len(ctors)
    if ctorNum==0:
        description = "Cannot be constructed because there's no constructor defined."
    elif ctorNum==1:
        description = f"Can only be {ctors[0].ctorName}."
    else:
        description = "Can be either "\
                      + ', '.join([c.ctorName for c in ctors[:-1]])\
                      + ("," if ctorNum>2 else "")\
                      + f" or {ctors[-1].ctorName}."
    return chain(
        [f"class {dataDef.typeName}{inherit_part}:"],
        [indent+f"\"{description}\""],
        (indent+line for line in gen_match_signature(dataDef)),
        [indent*2+"..."],
        #an empty line
        [""]
    )

def replaceWithAny(patterns:List[str],input:str)->str:
    "Replace the occurence of patterns in `input` to 'Any'."
    if patterns:
        return 'Any'.join(re.split('|'.join(patterns),input))
    else:
        return input


def gen_one_ctor(dataDef:DataDef, ctor:Ctor)->Iterator[str]:
    typeName: str = dataDef.typeName
    ctorName: str = ctor.ctorName
    def_typevars: List[str] = dataDef.typeVars
    ctor_typevars: set[str] = ctor.extract_typevars().intersection(set(def_typevars))
        # is actually bounded vars (bounded by def_typevars)
    def_type_str = "{}[{}]".format(typeName,','.join(def_typevars)) if def_typevars else typeName
        #e.g., Lst[a]
    generic_def_type_str = replaceWithAny(list(set(def_typevars)-ctor_typevars), 
                                          def_type_str)
    
    # constructing inherit_part
    if ctor_typevars:
        inherit_part = \
            "Generic[{}],{}".format(
                ','.join(ctor_typevars),
                generic_def_type_str
            )
    else:
        # If the Ctor has no typevar, the typevar positions of the inherited type 
        # should be all Any
        # e.g., in the `Lst` example, the inheritance of `Nil` should be `(Lst[Any])`
        inherit_part = replaceWithAny(def_typevars, def_type_str)
    
    # dealing with '_' field
    inf_fields = (f'_f{i}' for i in count(1))
    argtype_pairs: list[tuple[str,str]] = [((arg.fieldName if arg.fieldName!='_' else next(inf_fields))
                                           ,str(arg.typ))
                                           for arg in ctor.args]
    fields: list[str] = [p[0] for p in argtype_pairs]
    
    #initBlock
    if fields:#len(fields)>0
        initBlock = chain(\
            [indent+"def __init__(self,{}):"\
            .format(', '.join(("{}:{}".format(field,argtyp)
                                for (field,argtyp) in argtype_pairs)))],
            (indent*2+"self.{field} = {field}".format(field = field)
            for field in fields),
        )
    else:
        initBlock = []
    
    #isCtor_part
    if NO_TYPEGUARD:
        isCtor_part = []
    else:
        isCtor_part = \
            ["def is{}(x:{})->TypeGuard[{}]:".format(
                ctorName,
                generic_def_type_str,
                "{}[{}]".format(ctorName, ','.join(ctor_typevars)) 
                    if ctor.args else ctorName)
            , indent+"return type(x) is "+ctorName,
            ]

    return chain(
        #class declaration
        [f"class {ctorName}({inherit_part}):"],
        
        #field declaration
        (indent+"{}: {}".format(field,argtyp)
            for (field,argtyp) in argtype_pairs),
        
        #__init__
        initBlock,

        #match signature
        (indent+line for line in gen_match_signature(dataDef)),

        #match body
        [indent*2+"return {}({})"\
         .format(lowercase_head(ctorName),
                 ','.join(f"self.{field}" for field in fields))],
        
        #isCtor test function
        isCtor_part,

        #an empty line
        [""]
    )


def gen_one_DataDef(dataDef: DataDef)->Iterator[str]:
    return chain(
        # type def
        gen_typedef(dataDef),
        # Constructors
        chain.from_iterable(
            gen_one_ctor(dataDef,ctor) for ctor in dataDef.ctors),
        # an empty line
        [""]
    )

#----------------------------------------------------------------
#--------------- IV. File processing procedures -----------------
#----------------------------------------------------------------
# ENTRY: fileP : Parser[tuple[list[AdtDeclBlock], list[str]]]


class AdtDeclBlock:
    pre:List[str] #the text before the adt block
    adtdecl:List[str] #including the first and last line of `"""`
    hash:Optional[str]
    code:List[str]
    def __init__(self
                ,pre:List[str]
                ,adtdecl:List[str]
                ,m_code_block:Optional[tuple[str,List[str]]]):
        self.pre = pre
        self.adtdecl = adtdecl
        if m_code_block:
            self.hash = m_code_block[0]
            self.code = m_code_block[1]
        else:
            self.hash = None
            self.code = []

class ProcessedAdtBlock(AdtDeclBlock):
    dataDefs:List[DataDef]

    def __init__(self,declblock:AdtDeclBlock, dataDefs:List[DataDef]):
        super().__init__(
            declblock.pre,
            declblock.adtdecl,
            (declblock.hash,declblock.code) if declblock.hash else None
            )
        self.dataDefs = dataDefs

    @classmethod
    def fromAdtDecl(cls,declblock:AdtDeclBlock)->'ProcessedAdtBlock':
        # Need to handle parsing errors.
        dataDefs = parseAST(''.join(declblock.adtdecl[1:-1]))
        return ProcessedAdtBlock(declblock, dataDefs)

    def generate_code(self)->Iterator[str]:
        hashOfBlock = hashlib.sha256(str(self.dataDefs).encode()).hexdigest()[:10]
        if self.hash and hashOfBlock!=self.hash:
            print("Warning: hash doesn't match, the old generated code will be replaced.")
            genCode = True
        elif self.hash == hashOfBlock:
            genCode = False
        else:
            genCode = True
        
        code_part:Iterator[str] = chain(
            [f"# The code below is generated according to the definition above; hash={hashOfBlock}\n\n"],
            interleave('\n',generate_code_of_datadefs(self.dataDefs)),
            ["# End of generated code.\n"]
        ) if genCode else chain(
            [f"# The code below is generated according to the definition above; hash={self.hash}\n"],
            self.code,
            ["# End of generated code.\n"]
        )

        return chain(
            self.pre,
            self.adtdecl,
            code_part
        )

itemP = parsy.test_item

adt_declP = itemP(lambda line: bool(re.fullmatch(r'("""|\'\'\')\s*adt\s*:\s*',line))
                 ,"adt declaration")
multi_line_strP = itemP(lambda line:bool(re.fullmatch(r'("""|\'\'\').*\s*',line))
                       , "multi-line string")

# Parser[list[str]]
adt_declblockP = \
    adt_declP.map(lambda x:[x])\
    + parsy.any_char.until(multi_line_strP)\
    + multi_line_strP.map(lambda x:[x])

#Parser[Hash]  
start_of_codeblockP = \
    itemP(lambda line:bool(re.fullmatch(
            r'# The code below is generated according to the definition above; hash=.+\s*'
            ,line))
         , "generated code block").map(lambda line:re.findall(r'hash=(.+)\s*',line)[0])
end_of_codeblockP = itemP(lambda line:bool(re.fullmatch(r'# End of generated code\..*\s*'
                                                       ,line))
                         , "end of generated code block")
# Parser[tuple[str,list[str]]]
code_blockP = parsy.seq(
    start_of_codeblockP,
    parsy.any_char.until(end_of_codeblockP)
    )\
    << end_of_codeblockP

# Parser[Optional[tuple[str,list[str]]]]
maybe_code_blockP = parsy.peek(start_of_codeblockP).optional().bind(
    lambda codeblock: code_blockP if codeblock else parsy.success(None))



# Parser[tuple[list[AdtDeclBlock], list[str]]]
fileP = parsy.seq(
    parsy.seq(
        parsy.any_char.until(adt_declP),
        adt_declblockP,
        maybe_code_blockP,
        ).combine(AdtDeclBlock).many()
    , parsy.any_char.many()
    )




###-----------------------

def take(n:int, x:Iterable)->List:
    it = iter(x)
    return [next(it) for _ in range(n)]


if __name__ == "__main__":
    main()  
    # toks = tokenize(example)
    # datas = parseAST(toks)
    # print(hash(datas[1]))
    # code_lines = generate_code(datas)
    

    
    