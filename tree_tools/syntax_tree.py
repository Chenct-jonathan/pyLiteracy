
from typing import TypeVar
_A,_B,_C,_T = TypeVar('_A'),TypeVar('_B'),TypeVar('_C'),TypeVar('_T')



#----------syntax_tree example(s)--------
from syntax_tree.parser import parserOfRules

rule1 = '''
p1 -> a p2
p2 -> p1 | b
'''
text1 = "<a>x</a><a>y</a><b>0</b>"

# parserDict = parserOfRules(rule1)
# tree = parserDict.ruleParser['p1'].parse(text1)
#parserDict.singleEntry = p1 | p2
"""
Use tree.ppstr() to get the string of the pretty-printting-string,
or tree.pprint() to directly print it.

should print the below text in this case:
p1____a(x)
|_____p2____p1____a(y)
            |_____p2____b(0)
"""

rule2 = """
DP -> FUNC_degreeHead MODIFIER
S -> ENTITY_pronoun DP
"""
text2 = "<ENTITY_pronoun>她</ENTITY_pronoun><FUNC_degreeHead>很</FUNC_degreeHead><MODIFIER>開心</MODIFIER>"
parserDict = parserOfRules(rule2)
tree = parserDict.ruleParser['S'].parse(text2)


PSR = """
S -> (NP|S') (Aux)? VP
NP -> (pronoun|(Det)? (AP)? N (PP)? (S')?)
VP -> (AdvP)? V (AP|NP(NP|PP|S')?)? (XP)*
AP -> (deg)? A (PP|S')?
PP -> P (NP)?
Det -> (Art|Dem|NP-poss)
X -> S ((Conj)? X)? Conj X
S' -> (Comp)?S
Aux -> (Inf.|Modal)?(Perf.)?(Prog.)

"""

articutPOS = """
AP -> (deg)? A PP?
A -> MODIFIER | MODIFIER_color
deg -> FUNC_degreeHead

PP -> P (NP)?
P -> RANGE_locality | RANGE_period
VP -> ACTION_verb NP?
NP -> ENTITY_pronoun|(Det)? (AP)? N (PP)?
N -> ENTITY_[^classifier]
Det -> FUNC_determiner

np --> classifier (Modifier)*? n
modifier --> anything + 的_func_inner

"""
#TODOs:
#   - implement typed parser, lazy parser
#   - add simple regex: ^start-with, end-with$, !not
#   - add complex parsing rules
#   - consider keeping parsing trace


# testing
test_rule3 = """
p1 -> a (b c)?
p2 -> p1 d |  r{a+} b 
"""
parserDict = parserOfRules(test_rule3)
r3_p1 = parserDict.ruleParser['p1']

r3_t1 = "<a>x</a>"
r3_t2 = "<a>x1</a><b>x2</b><a>x3</a><d>x4</d>"
r3_t3 = "<a>x1</a><b>x2</b><aa>x3</aa><b>x4</b>"

def run_test_rule3():
    r3_p1.parse(r3_t1).pprint()
    r3_p1.parse(r3_t2).pprint()
    r3_p1.parse(r3_t3).pprint()

test_rule4 = """
p1 -> a b
    | a c
"""
r4_t1 = "<a>x1</a><c>x2</c>" #should fail
parserDict = parserOfRules(test_rule4)
r4_p1 = parserDict.ruleParser['p1']

test_regtok1 = """
p1 -> r{.*}   #this receives any token
"""
parserDict = parserOfRules(test_regtok1)
# parserDict.ruleParser['p1'].parse("<abc>xxx</abc>").pprint()

test_contentTerm = """
p1 -> >ab|c<  # accept any pos token with content ab or c
p2 -> MODIFIER>very|so< . # accept MODIFIER with content is 'very' or 'so'
p3 -> r{ENTITY_.*}>abc<  
"""
parserDict = parserOfRules(test_contentTerm)
# parserDict.ruleParser['p1'].parse('<gggg>ab</gggg>').pprint()
# parserDict.ruleParser['p1'].parse('<hhh>c</hhh>').pprint()
# parserDict.ruleParser['p2'].parse('<MODIFIER>very</MODIFIER>').pprint()
# parserDict.ruleParser['p3'].parse('<ENTITY_person>abc</ENTITY_person>').pprint()


test_placeholder = """
p1 -> (a|@) b
"""
parserDict = parserOfRules(test_placeholder)
# parserDict.ruleParser['p1'].parse('<a>x</a><b>y</b>').pprint()
# parserDict.ruleParser['p1'].parse('<b>y</b>').pprint()

test_bintree = """
p1 -> a p1 | b @
"""
parserDict = parserOfRules(test_bintree)
parserDict.ruleParser['p1'].parse('<a>x</a><a>y</a><a>z</a><a>x</a><a>y</a><b>0</b>').pprint()

#------------RoseTree example------------
from syntax_tree.type import RoseTree

_rt_sample1 = RoseTree('P',
    [RoseTree('P1',
        [RoseTree('1')
        ,RoseTree('2')
        ])
        
    ,RoseTree('P2',
        [RoseTree('3')])
    ,RoseTree('P3',
        [RoseTree('P4', 
            [RoseTree('4')
            ,RoseTree('P5',
                [RoseTree('5')
                ,RoseTree('6')]
                )
            ])
        ,RoseTree('7')
        ])
    ]
)
# P___P1____1
# |   |_____2
# |___P2____3
# |___P3___P4___4
#     |    |____P5___5
#     |         |____6
#     |____7

