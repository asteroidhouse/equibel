
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = b'`(\x04\x06d\x07\xd9\x94\xf1Q(~\xb5\xa0o\xcf'
    
_lr_action_items = {'RPAREN':([4,5,6,7,8,9,11,],[9,-2,-5,-6,-4,-1,-3,]),'COMMA':([5,6,7,8,9,],[10,-5,-6,-4,-1,]),'INTEGER':([3,10,],[8,8,]),'IDENTIFIER':([0,3,10,],[2,6,6,]),'$end':([1,9,],[0,-1,]),'LPAREN':([2,6,],[3,3,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'ARGS':([3,10,],[4,11,]),'PREDICATE':([0,3,10,],[1,7,7,]),'ARG':([3,10,],[5,5,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> PREDICATE","S'",1,None,None,None),
  ('PREDICATE -> IDENTIFIER LPAREN ARGS RPAREN','PREDICATE',4,'p_PREDICATE','PredicateParser.py',36),
  ('ARGS -> ARG','ARGS',1,'p_ARGS','PredicateParser.py',40),
  ('ARGS -> ARG COMMA ARGS','ARGS',3,'p_ARGS','PredicateParser.py',41),
  ('ARG -> INTEGER','ARG',1,'p_ARG','PredicateParser.py',45),
  ('ARG -> IDENTIFIER','ARG',1,'p_ARG','PredicateParser.py',46),
  ('ARG -> PREDICATE','ARG',1,'p_ARG','PredicateParser.py',47),
]
