
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = b"\x89\xc8\xbd\x94\x94\x0b\x16DVz\x0e'\x97Y\x88A"
    
_lr_action_items = {'INTEGER':([3,10,],[5,5,]),'LPAREN':([1,6,],[3,3,]),'IDENTIFIER':([0,3,10,],[1,6,6,]),'$end':([2,9,],[0,-1,]),'COMMA':([5,6,7,8,9,],[-4,-5,10,-6,-1,]),'RPAREN':([4,5,6,7,8,9,11,],[9,-4,-5,-2,-6,-1,-3,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'ARGS':([3,10,],[4,11,]),'ARG':([3,10,],[7,7,]),'PREDICATE':([0,3,10,],[2,8,8,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> PREDICATE","S'",1,None,None,None),
  ('PREDICATE -> IDENTIFIER LPAREN ARGS RPAREN','PREDICATE',4,'p_PREDICATE','/Users/paulvicol/Learn/Python/ParserTests/CommandPrompt/ASP/PredicateTree/PredicateParser.py',35),
  ('ARGS -> ARG','ARGS',1,'p_ARGS','/Users/paulvicol/Learn/Python/ParserTests/CommandPrompt/ASP/PredicateTree/PredicateParser.py',39),
  ('ARGS -> ARG COMMA ARGS','ARGS',3,'p_ARGS','/Users/paulvicol/Learn/Python/ParserTests/CommandPrompt/ASP/PredicateTree/PredicateParser.py',40),
  ('ARG -> INTEGER','ARG',1,'p_ARG','/Users/paulvicol/Learn/Python/ParserTests/CommandPrompt/ASP/PredicateTree/PredicateParser.py',44),
  ('ARG -> IDENTIFIER','ARG',1,'p_ARG','/Users/paulvicol/Learn/Python/ParserTests/CommandPrompt/ASP/PredicateTree/PredicateParser.py',45),
  ('ARG -> PREDICATE','ARG',1,'p_ARG','/Users/paulvicol/Learn/Python/ParserTests/CommandPrompt/ASP/PredicateTree/PredicateParser.py',46),
]
