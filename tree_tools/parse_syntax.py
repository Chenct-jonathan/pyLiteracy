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



class HeadPatterns(Static):
    C_pat: re.Pattern = re.compile("((?<!</ACTION_verb>)(?<!</FUNC_inner>)<ASPECT>了</ASPECT>$|<CLAUSE_(particle|YesNoQ)>[^<]+</CLAUSE_(particle|YesNoQ)>)")
    "\</ACTION_verb>(\<ACTION_verb>說\</ACTION_verb>)"

    Mod_pat: re.Pattern =  re.compile("((<MODAL>[^<]+</MODAL>|<MODIFIER>可能</MODIFIER>|<ACTION_verb>要</ACTION_verb>|<CLAUSE_AnotAQ>[^<]+會</CLAUSE_AnotAQ>)+)")
    "(\<MODAL>[^<]+\</MODAL>)"

    Aux_pat: re.Pattern = re.compile("(((?:<FUNC_inner>就</FUNC_inner>)?(?<!<FUNC_inner>還</FUNC_inner>)<AUX>[就卻是]+</AUX>|<CLAUSE_AnotAQ>[^<]+[^會]</CLAUSE_AnotAQ>))")
    
    Neg_pat: re.Pattern = re.compile("(<FUNC_negation>[^<]+</FUNC_negation>(<ACTION_verb>要</ACTION_verb>)?)")
    "(\<FUNC_negation>[^\<]+\</FUNC_negation>)"

    LightV_pat: re.Pattern = re.compile("(<ACTION_lightVerb>[^<]+</ACTION_lightVerb>)")
    "(\<ACTION_lightVerb>[^\<]+\</ACTION_lightVerb>)"

    Asp_pat: re.Pattern = re.compile("(((<ASPECT>[過了完著]+</ASPECT>)+)(?=<ACTION_lightVerb>)|((<ASPECT>[過了完著]+</ASPECT>)+)(?=<ACTION_verb>)|(<ASPECT>(?:(正在|在|已經))</ASPECT>)(?=<ACTION_verb>)|<ACTION_verb>[^<]+([過了完著])</ACTION_verb>)")
    "(\</ACTION_verb>(\<ASPECT>[過了完著]+\</ASPECT>)|(\<ASPECT>[在]\</ASPECT>)\<ACTION_verb>)"

    Deg_pat: re.Pattern = re.compile("(<FUNC_degreeHead>[太很]</FUNC_degreeHead>)") #I leave possibility for adj. predicates. e.g., 我很高。
    "(\<FUNC_degreeHead>很\</FUNC_degreeHead>)"

    Adv_pat = re.compile("((?:<FUNC_inner>所</FUNC_inner>)?<ModifierP>[^<]+地</ModifierP>|<FUNC_inner>從</FUNC_inner><[^>]+>[^<]+</[^>]+>|<FUNC_inter>[^<]+</FUNC_inter>|(?:<FUNC_inner>所</FUNC_inner>)?<[^>]+>[^<]+</[^>]+><FUNC_modifierHead>地</FUNC_modifierHead>|(?:<TIME_[a-z]+>[^<]+</TIME_[a-z]+>){1,10}(?:<RANGE_period>[^<]+</RANGE_period>)?|<QUANTIFIER>[^<]+</QUANTIFIER>)")

    #Adj_pat = re.compile("(<MODIFIER>[^<]+</MODIFIER>(?:<FUNC_inner>的</FUNC_inner>)?)")
    
    P_pat: re.Pattern = re.compile("(<FUNC_inner>[從在]</FUNC_inner>|<ACTION_verb>到</ACTION_verb>)") #I did not know how to parse 在...裡面 yet.
    "(<FUNC_inner>[從在]</FUNC_inner>)"
    
    V_pat: re.Pattern = re.compile("(?<!<FUNC_inner>的</FUNC_inner>)((<(ACTION_verb|VerbP)>[^<用到]+</(ACTION_verb|VerbP)>|<FUNC_negation>沒有</FUNC_negation>)+(?:<FUNC_inner>[成向]</FUNC_inner>)?)(?!<FUNC_inner>的</FUNC_inner>)")
    "(\<(ACTION_verb|VerbP)>[^\<]+\</(ACTION_verb|VerbP)>)"

    Cls_pat: re.Pattern =  re.compile("(<ENTITY_classifier>[^<]+</ENTITY_classifier>)")
    "(\<ENTITY_classifier>[^\<]+\</ENTITY_classifier>)"

    RC_pat: re.Pattern = re.compile("(<FUNC_inner>的</FUNC_inner>|<MODIFIER_color>[^<]+</MODIFIER_color>)")
    "(\<FUNC_inner>的\</FUNC_inner>)"

    De_Comp_pat: re.Pattern = re.compile("(<FUNC_inner>得</FUNC_inner>)")
    "(\<FUNC_inner>得\</FUNC_inner>)"

    N_pat: re.Pattern = re.compile("((<ENTITY_(nounHead|nouny|noun|oov|pronoun)>[^<]+</ENTITY_(nounHead|nouny|noun|oov|pronoun)>|<TIME_[a-z]+>[^<]+</TIME_[a-z]+>|<LOCATION>[^<]+</LOCATION>|<RANGE_locality>[^<]+</RANGE_locality>|<FUNC_determiner>[^<]+</FUNC_determiner>|<CLAUSE_(What|Where|Who)Q>[^<]+</CLAUSE_(What|Where|Who)Q>)+)")
    "(\<ENTITY_(nounHead|nouny|noun|oov|pronoun)>[^\<]+\</ENTITY_(nounHead|nouny|noun|oov|pronoun)>)"
    
    Conj_pat: re.Pattern = re.compile("(<FUNC_conjunction>[^<]+</FUNC_conjunction>|<FUNC_inner>還</FUNC_inner><AUX>是</AUX>)")

@dataclass
class Tree:
    left: 'list[Union[Tree, str]]' # I'm not sure how do i express -> list[Tree or str]
    head: str
    comp: 'Union[str,Tree]' # We might have to change this?
    
    def c_command(parentSTR: str, childSTR: str, self) -> bool:
        pass


@dataclass
class Adjunct:
    left:str
    head:str
    right:str

# We consider only head-init for now.




def split_pos(pat:re.Pattern, src:str) -> Optional[Tuple[str,str,str]]:
    m = pat.search(src)
    if m is None:
        return None

    head_span = m.span()
    return (src[0:head_span[0]], #the string before pat
            m.group(1),          #the string that matches pat
            src[head_span[1]:])  #the string after pat


def split_left(src: str) -> list[str]:
    elemLIST = [word for word in re.split(HeadPatterns.Adv_pat, src) if word != ""]
    #pprint(elemLIST)
        
    return elemLIST

class CP(Tree):
    pass

def parse_CP(parseSTR: str)->CP: #CP is head-final, confirmed
    '''
    1. Target the "C".
    2. Take the string on the right as "COMP" and leave the rest as "LEFT".
    '''
    split = split_pos(HeadPatterns.C_pat, parseSTR)
    if split is None:
        return CP(left = []
                  ,head = "∅"
                  ,comp = parseSTR
                  )
    else: 
        return CP(left=split_left(split[2])
                  , head=split[1]
                  , comp=split[0]
                  )
        #or simply `Tree(*split)`


class TP(Tree):
    pass

def parse_TP(CP_comp: str) -> TP:
    return TP(left = []
              ,head = "∅"
              ,comp = CP_comp
              )


class ModP(Tree):
    pass

def parse_ModP(TP_comp: str) -> ModP:
    split = split_pos(HeadPatterns.Mod_pat, TP_comp)
    if split is None:
        return ModP(left = []
                    ,head = ""
                    ,comp = TP_comp
                    )
    else:
        return ModP(left = split_left(split[0])
                  ,head = split[1]
                  ,comp = split[2]
                  )

#class NegP(Tree):
    #pass

#def parse_NegP(ModP_comp: str) -> NegP:
    #split = split_pos(HeadPatterns.Neg_pat, ModP_comp)
    #if split is None:
        #return NegP(left = []
                    #,head = ""
                    #,comp = ModP_comp
                    #)
    #else:
        #return NegP(left = split_left(split[0])
                  #,head = split[1]
                  #,comp = split[2]
                  #)


class AspP(Tree): #https://www.persee.fr/doc/clao_0153-3320_1995_num_24_1_1466 Some reference for AspP, FYI. :)
    pass 

def reverse_vr(ModP_comp: str) -> str:
    reverse_vr_pat = r"(<ACTION_lightVerb>[^<]+</ACTION_lightVerb>)?(?<!在</ASPECT>)(<ACTION_verb>[^<]+</ACTION_verb>)+(<FUNC_inner>[成向]</FUNC_inner>)?((<ASPECT>[過了完著]</ASPECT>)+)"
    vr = re.search(reverse_vr_pat, ModP_comp)
    if vr is not None:
        vr = re.search(reverse_vr_pat, ModP_comp).group(4)
    if vr is not None:
        ModP_comp = re.sub(reverse_vr_pat, lambda m: f"{m.group(4) or ''}{m.group(1) or ''}{m.group(0).replace(m.group(4) or '', '').replace(m.group(1) or '', '')}", ModP_comp, 1)
    
    return ModP_comp

def parse_AspP(ModP_comp: str) -> AspP:
    ModP_comp = reverse_vr(ModP_comp)
    split = split_pos(HeadPatterns.Asp_pat, ModP_comp) # Maybe try reverse VR before split_pos()
    if split is None:
        return AspP(left = []
                    ,head = ""
                    ,comp = ModP_comp
                    )
    else:
        return AspP(left = split_left(split[0])
              ,head = split[1]
              ,comp = split[2]
              )

class LightVP(Tree):
    pass

def parse_LightVP(AspP_comp: str) -> LightVP:
    split = split_pos(HeadPatterns.LightV_pat, AspP_comp)
    if split is None:
        return LightVP(left = []
                       ,head = "∅"
                       ,comp = AspP_comp
                       )
    else:
        return LightVP(left = split_left(split[0])
                  ,head = split[1]
                  ,comp = split[2]
                  )

class VP(Tree):
    pass

class AuxP(Tree):
    pass

class DegP(Tree):
    pass

class PP(Tree):
    pass

def parse_VP(LightVP_comp: str, check_DegP: bool)->Optional[Union[VP, DegP]]:
    split = split_pos(HeadPatterns.Aux_pat, LightVP_comp)
    if split:
        return AuxP(left = split_left(split[0])
                  ,head = split[1]
                  ,comp = split[2]
                  )    
    
    split = split_pos(HeadPatterns.V_pat, LightVP_comp)
    if split:
        return VP(left = split_left(split[0])
                  ,head = split[1]
                  ,comp = split[2]
                  )
    
    if check_DegP == True:
        split = split_pos(HeadPatterns.Deg_pat, LightVP_comp)
        if split:
            return DegP(left = split_left(split[0])
                        ,head = split[1]
                        ,comp = split[2]
                        )
    
    split = split_pos(HeadPatterns.P_pat, LightVP_comp)
    if split:
        return PP(left = split_left(split[0])
                  ,head = split[1]
                  ,comp = split[2]
                  )
    
    return VP(left = ""
                  ,head = ""
                  ,comp = LightVP_comp
                  )


class ClsP(Tree):
    pass

def parse_ClsP(VP_comp: str) -> ClsP:
    split = split_pos(HeadPatterns.Cls_pat, VP_comp)
    if split is None:
        return ClsP(left = []
                    ,head = ""
                    ,comp = VP_comp
                    )
    else:
        return ClsP(left = split_left(split[0])
                  ,head = split[1]
                  ,comp = split[2]
                  )

def parse_RC(ClsP_comp: str) -> Optional[Adjunct]:
    split = split_pos(HeadPatterns.RC_pat, ClsP_comp)
    if split is None:
        return None
    else: 
        return Adjunct(left=split_left(split[0])
                       , head=split[1]
                       , right=split[2]
                       )


class AdjP(Tree):
    pass

class NP(Tree):
    pass

def parse_NP(ClsP: Tree, checkCLS: bool) -> NP:
    rc = parse_RC(ClsP.comp)
    if rc is None:
        '''
        here's a new sample for the n_head
        suppose N_COMP will always be ""
        when we find N + N (e.g., 我同學)
        instead of always getting the first 我
        i add line 284 285 as an example to capture longer nouns seperated by Articut
        
        p.s. Articut "我" will only be parsed as possessive when followed by a pronoun.
        when its possessive, it will be viewed as NP.left, which is perfectly correct.
        While its not, we might just see all the N+N as an N instead
        '''
        split = split_pos(HeadPatterns.N_pat, ClsP.comp)
        if checkCLS == True and split is None:
            if ClsP.head != "":
                return NP(left = []
                          ,head = "∅"
                          ,comp = ""
                          )
            else:
                return NP(left = []
                          ,head = ""
                          ,comp = ""
                          )
        else:
            if split is None:
                pass
            else:
                if parse_VP(split[2], check_DegP=False).head != "":
                    return NP(left = "",
                          head = "",
                          comp = ""
                      )
                else:
                    return NP(left = split_left(split[0]),
                              head = split[1],
                              comp = ""
                          )
    else:
        if rc.right == "":
            '''
            or NP(left=[''.join(rc.left) + rc.head],head="∅",comp="")
            '''
            return AdjP(
                left = "",
                head = ''.join(rc.left) + rc.head,
                comp = ""
            )            
        n_tree = NP(
            left = [], 
            head = "",
            comp = rc.right
        )
        n_head = parse_NP(n_tree, False)
        if n_head == None:
            return NP(
                left = [''.join(rc.left) + rc.head],
                head = "",
                comp = ""
            )            
        else:  
        #xx的yy
            return NP(
                left = [''.join(rc.left) + rc.head],
                head = n_head.head,
                comp = ""
            )


class De_CompP(Tree):
    pass

def parse_De_CompP(VP_comp: str) -> De_CompP:
    split = split_pos(HeadPatterns.De_Comp_pat, VP_comp)
    if split is None:
        return De_CompP(left = []
                        ,head = ""
                        ,comp = VP_comp
                        )
    else:
        return De_CompP(left = split_left(split[0])
                        ,head = split[1]
                        ,comp = split[2]
                        )


"""
equivalent to writing:
CP -> ? !c_pat TP
    | ø ø TP
TP -> ø ModP
ModP -> ? !mod_pat NegP
    | "" "" NegP
NegP -> ? neg_pat LightVP
    | "" "" LightVP
LightVP -> ? lightV_pat (VP | DegP | [pred_on_neg])
    | ø ø (VP | DegP | [pred_on_neg])
VP -> ? v_pat (CP | ClsP)
DegP -> ? deg_pat ClsP
ClsP -> ? cls_pat NP
    | ø ø NP
NP -> (? rc_pat) ? ??
    | ? n_pat ?
    | ø ø ?

"""
# pred_on_neg: Tree -> input:str -> Either[Err,Tree] #how to represent the continuation?

def gen_realTree(treeDICT: dict) -> Tree:
    if treeDICT["VP"].head == "":
        #print("--------------------------------------------------------------------------------------------------------------------------------")
        print("\nCannot Find Predicate.\nThis Is NOT A Complete Grammatical Sentence.")
        #print("--------------------------------------------------------------------------------------------------------------------------------")
        
        return None    
    projLIST = ['CP', 'TP', 'ModP', 'AspP', 'LightVP', 'VP', 'ClsP', 'NP', 'De_CompP']
    realDICT = copy.deepcopy(treeDICT)
    projLIST = [proj for proj in projLIST if proj in realDICT]
    
    for max_proj in range(len(projLIST) - 1, -1, -1):
        if realDICT[projLIST[max_proj]].head != "":
            for higher_proj in range(projLIST.index(projLIST[max_proj]) - 1, -1, -1):
                if realDICT[projLIST[higher_proj]].head != "":
                    parent_proj = projLIST[higher_proj]
                    current_proj = projLIST[max_proj]
                    realDICT[parent_proj].comp = realDICT[current_proj]
                    
    for max_proj in list(realDICT.keys()):
        if realDICT[max_proj].head == "":
            realDICT.pop(max_proj, None)
            
    return realDICT["CP"]

def parse_S(parseSTR: str, genTree: bool, showTree: bool) -> dict:
    treeDICT = {}
    
    tCP = parse_CP(parseSTR)
    if tCP.head != "":
        treeDICT["CP"] = tCP
    
    tTP = parse_TP(tCP.comp)
    if tTP.head != "":
        treeDICT["TP"] = tTP    
    
    tModP = parse_ModP(tTP.comp)
    if tModP.head != "":
        treeDICT["ModP"] = tModP    
    
    tAspP = parse_AspP(tModP.comp)
    if tAspP.head != "":
        treeDICT["AspP"] = tAspP     
    
    tLightVP = parse_LightVP(tAspP.comp)
    if tLightVP.head != "":
        treeDICT["LightVP"] = tLightVP    
    
    tVP = parse_VP(tLightVP.comp, check_DegP=True)
    treeDICT["VP"] = tVP
    
    #pprint(treeDICT)    
    if tVP.head != "":
        check_rc = split_pos(HeadPatterns.RC_pat, tVP.comp)
        check_embed = parse_VP(tVP.comp, check_DegP=False)
        if check_rc is None and check_embed.head != "":
            treeDICT["VP"].comp = parse_S(treeDICT["VP"].comp, genTree=True, showTree=False)        
            
        else:
            treeDICT["VP"] = tVP
            
            tClsP = parse_ClsP(tVP.comp)
            if tClsP.head != "":
                treeDICT["ClsP"] = tClsP
                
            tNP = parse_NP(tClsP, True)
            if tNP.head != "":
                treeDICT["NP"] = tNP
                
            tDe_CompP = parse_De_CompP(tVP.comp)
            if tDe_CompP.head != "":
                treeDICT["De_CompP"] = tDe_CompP
            
        #treeDICT = {
            #"CP": tCP,
            #"TP": tTP,
            #"ModP": tModP,
            #"AspP": tAspP,
            #"LightVP": tLightVP,
            #"VP": tVP,
            #"ClsP": tClsP,
            #"NP": tNP,
            #"De_CompP": tDe_CompP
        #}
         
    if genTree == True:
        realTree = gen_realTree(treeDICT)
        
        if showTree == True and realTree != None:
            print("\n")
            pprint(realTree)
        
        return realTree
    
    else:
        if showTree == True:
            print("\n")
            output_tree(treeDICT)
        
        return treeDICT        
        
@dataclass
class EPP_movement():
    target_phrase: 'Union[str, Tree]'
    original_pos: str
    target_pos: str
    

def ex_EPP_movement(treeDICT: dict, genTree: bool, showTree: bool) -> (EPP_movement, 'Union[Tree,dict]'):
    projLIST = ['CP', 'TP', 'ModP', 'AspP', 'LightVP', 'VP']
    projLIST = [proj for proj in projLIST if proj in treeDICT]
    if treeDICT["VP"].head == "":
        print("\nEPP_movement：No Necessary EPP Movement Scenario.\n")
        return None
    else:
        if treeDICT["TP"].left == []:
            for max_proj in projLIST:
                try:
                    if treeDICT[max_proj].left != []:
                        subjectP = max(treeDICT[max_proj].left, key=len)
                        subj = Tree(left=[],
                                    head="",
                                    comp=subjectP)
                        treeDICT["TP"].left.insert(0, parse_NP(subj, False))
                        treeDICT["TP"].comp = treeDICT["TP"].comp.replace("{}".format(str(treeDICT[max_proj].left[0])), "<trace>t</trace>", 1)
                        if max_proj != "LightVP" and max_proj != "VP": 
                            treeDICT[max_proj].left[0] = "<trace>Subj_trace</trace>"
                            treeDICT["LightVP"].left.insert(-1, "<trace>Subj_trace</trace>")
                        elif max_proj == "LightVP":
                            treeDICT[max_proj].left.insert(0, "<trace>Subj_trace</trace>") 
                        else:
                            #del treeDICT[max_proj].left[0]
                            treeDICT["LightVP"].left.insert(-1, "<trace>Subj_trace</trace>")
                        try:    
                            for trace_pos in projLIST[::-1]:
                                if trace_pos not in ["CP", "TP", "VP"] and "<trace>Subj_trace</trace>" not in treeDICT[trace_pos].left:
                                    treeDICT[trace_pos].left.insert(0, "<trace>Subj_trace</trace>")
                        except KeyError:
                            continue
                        
                        
                        print("\n")
                        pprint(EPP_movement(target_phrase = parse_NP(subj, False)
                                        , original_pos = max_proj + "_left"
                                        ,target_pos = "TP_left"
                                        ))                        
                        
                        if genTree == True:
                            realTree = gen_realTree(treeDICT)
                            
                            if showTree == True:
                                print("\n")
                                pprint(realTree)
                                
                            return (EPP_movement(target_phrase = parse_NP(subj, False)
                                                    , original_pos = max_proj + "_left"
                                                    ,target_pos = "TP_left"
                                                    ), 
                                        realTree)
                        
                        else:
                            if showTree == True:
                                output_tree(treeDICT)                        
                        
                                return (EPP_movement(target_phrase = parse_NP(subj, False)
                                                    , original_pos = max_proj + "_left"
                                                    ,target_pos = "TP_left"
                                                    ), 
                                        treeDICT)
                            
                except KeyError:
                    continue
            else:
                treeDICT["TP"].left.insert(0, "<Pro>Pro_Support</Pro>")
                treeDICT["TP"].comp.insert(0, "<trace>Subj_trace</trace>")
                treeDICT["LightVP"].left.insert(0, "<trace>Subj_trace</trace>")
                for trace_pos in ["LightVP","AspP","ModP"]:
                    try:    
                        if "<trace>Subj_trace</trace>" not in treeDICT[trace_pos].left:
                            treeDICT[trace_pos].left.insert(0, "<trace>Subj_trace</trace>")
                    except KeyError:
                        continue
                    
                print("\n")
                pprint(EPP_movement(target_phrase = "<Pro>Pro_Support</Pro>" 
                                , original_pos = "LightVP_left"
                                ,target_pos = "TP_left"
                                ))                
                
                if genTree == True:
                    realTree = gen_realTree(treeDICT)
                
                    if showTree == True:
                        print("\n")
                        pprint(realTree)                    
            
                        return (EPP_movement(target_phrase = "<Pro>Pro_Support</Pro>" 
                                            , original_pos = "LightVP_left"
                                            ,target_pos = "TP_left"
                                            ),
                                realTree)
                    
                else:
                    if showTree == True:
                        output_tree(treeDICT)
                        
                        return (EPP_movement(target_phrase = "<Pro>Pro_Support</Pro>" 
                                            , original_pos = "LightVP_left"
                                            ,target_pos = "TP_left"
                                            ),
                                treeDICT)                        

@dataclass
class verb_raising():
    target_phrase: str
    original_pos: str
    target_pos: str
    
def ex_verb_raising(treeDICT: dict, genTree: bool, showTree: bool) -> (EPP_movement, 'Union[Tree,dict]'):
    if treeDICT["AspP"].head != "" and treeDICT["VP"].head != "":
        target_phrase = treeDICT["VP"].head
        if "在" in treeDICT["AspP"].head:
            treeDICT["AspP"].head = treeDICT["AspP"].head + treeDICT["VP"].head
        else: 
            treeDICT["AspP"].head = treeDICT["VP"].head + treeDICT["AspP"].head
        
        treeDICT["VP"].head = treeDICT["VP"].head.replace(target_phrase, "<trace>V_trace</trace>")
        
        print("\n")
        pprint(verb_raising(target_phrase = target_phrase 
                                , original_pos = "VP_head"
                                ,target_pos = "AspP_head"
                                ))        
        
        if genTree == True:
            realTree = gen_realTree(treeDICT)
            
            if showTree == True:
                pprint(realTree)
            
            return (verb_raising(target_phrase = target_phrase 
                                        , original_pos = "VP_head"
                                        ,target_pos = "AspP_head"
                                        ),
                    realTree)
        else:
            if showTree == True:
                output_tree(treeDICT)
            
            return (verb_raising(target_phrase = target_phrase 
                                        , original_pos = "VP_head"
                                        ,target_pos = "AspP_head"
                                        ),
                    treeDICT)            
            
    else:
        print("\nVerb Raising：No Necessary Verb Raising Scenario.\n")
        return None

def output_tree(treeDICT: dict):
    if treeDICT["VP"].head == "":    
        #print("--------------------------------------------------------------------------------------------------------------------------------")
        print("\nCannot Find Predicate.\nThis Is NOT A Complete Grammatical Sentence.")
        #print("--------------------------------------------------------------------------------------------------------------------------------")
        
        return None
    
    else:        
        try:
            projLIST = ['CP', 'TP', 'ModP', 'AspP', 'LightVP', 'VP', 'ClsP', 'NP', 'De_CompP']
            projLIST = [proj for proj in projLIST if proj in treeDICT]
            
            for max_proj in projLIST:
                if treeDICT[max_proj].head != "":
                    print(f"\n [{max_proj}]:")
                    pprint(treeDICT[max_proj])       
            
            return "Successfully"
    
        except Exception as e:
            print("\n", e)
            raise



if __name__ == '__main__':
    #inputSTR = "妹妹喜歡和爸爸聊天。"
    #parseLIST = [i for i in articut.parse(inputSTR, level="lv1")["result_pos"] if len(i) > 1]
    #for parseSTR in parseLIST:
        #if len(re.findall("<[^>]+>[^<]+</[^>]+>", parseSTR)) > 1:
            #print("*InputSTR:{}".format(inputSTR))
            #treeDICT = parse_S(parseSTR, genTree=False, showTree=True)
            ##pprint(treeDICT)
            #realTree = parse_S(parseSTR, genTree=True, showTree=True)
            #print("\n")
            
            ##print("*Narrow Syntax Operations:")
            ##EPP_tree = ex_EPP_movement(treeDICT, genTree=True, showTree=True)
            ##vraise_tree = ex_verb_raising(treeDICT, genTree=True, showTree=True)
            #print("--------------------------------------------------------------------------------------------------------------------------------")    
    
    
    with open("./data/test_data.json", "r", encoding="utf-8") as jsonFILE:
        testLIST = json.load(jsonFILE)
     
    for inputSTR in testLIST[200:250]:
        parseLIST = [i for i in articut.parse(inputSTR, level="lv1")["result_pos"] if len(i) > 1]
        #pprint(parseLIST)
        for parseSTR in parseLIST:
            if len(re.findall("<[^>]+>[^<]+</[^>]+>", parseSTR)) > 1:
                print("*InputSTR:{}".format(inputSTR))
                treeDICT = parse_S(parseSTR, genTree=False, showTree=False)
                realTree = parse_S(parseSTR, genTree=True, showTree=True)
                print("\n")
                
                #print("*Narrow Syntax Operations:")
                #EPP_tree = ex_EPP_movement(treeDICT, genTree=True, showTree=True)
                #vraise_tree = ex_verb_raising(treeDICT, genTree=True, showTree=True)
                print("--------------------------------------------------------------------------------------------------------------------------------")
            
    '''
    These examples help understand the parsing process.

    我覺得說他可以被吃五碗他喜歡的飯。(It's a weird but I just want to display all the Ps.)
    他可以吃五碗飯。(without a C)
    他吃五碗飯。(without a Modal)
    她參加比賽。(without a Classifier)
    他很高。(without a Verb. But MC allows Deg-Adj Predicate/VP Predicate.)
    他跑得很快。（VP without Complement NP but a "De" complement instead.）
    他吃了他喜歡的零食。(RC）
    他吃了五包他喜歡的零食。(RC and Classifier）
    他白飯。(Ungrammatical)
    樹上沒有葉子。(Neg)
    '''
    #userINPUT = "我覺得說他可以被吃五碗他喜歡的飯。他可以吃五碗飯。他吃五碗飯。她參加比賽。他很高。他跑得很快。他吃了他喜歡的零食。他吃了五包他喜歡的零食。他白飯。樹上沒有葉子。"
    #inputLIST = userINPUT.split("。")

    '''
    I hope the output goes like:

    /S
    /CP---+---CP.json {
          |               "SPEC_CP":"",
          |               "C":"",
          |               "COMP_CP":ModP
          |              }
          |
          |
          |---/ModP---+---ModP.json {
                                  "SPEC_ModP":"",
                                  "Mod":"",
                                  "COMP_ModP":LightVP
                                 }
    '''
    #os.mkdir("S")
    #CP_path = os.path.join("./S", "CP")
    #os.mkdir(CP_path)

    #with open("./S/CP/CP.json", "w", encoding="utf-8") as CP_file:
            #json.dump(S["CP"], CP_file, indent=4, ensure_ascii=False)