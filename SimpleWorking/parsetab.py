
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = b'\xab\x83\x1e,\xceOB\xcd\xa4=\x9d$\xfb\xa6\x16\xad'
    
_lr_action_items = {'RPAREN':([2,3,4,5,7,9,10,12,13,15,16,18,22,33,34,37,38,39,40,41,42,43,45,48,50,51,53,54,55,56,],[-5,-6,-26,-7,-24,-27,-13,-4,-25,-24,33,-29,38,-8,-30,48,-12,-16,-20,-21,-14,-17,51,-11,55,-28,-15,56,-10,-9,]),'LPAREN':([0,6,8,10,22,23,24,25,26,28,29,30,31,35,42,49,50,],[6,6,6,22,6,-22,6,-23,6,6,-19,-18,6,6,50,6,6,]),'MINUS':([2,3,4,5,7,9,10,11,12,13,15,16,18,19,21,33,34,38,39,40,41,42,43,48,51,53,55,56,],[-5,-6,-26,-7,-24,-27,-13,29,-4,-25,-24,29,-29,-24,29,-8,-30,-12,29,29,29,-14,29,-11,-28,29,-10,-9,]),'PLUS_EQUALS':([10,],[23,]),'$end':([1,2,3,4,5,7,9,10,11,12,13,14,18,33,34,38,40,41,42,43,44,48,51,55,56,],[0,-5,-6,-26,-7,-24,-27,-13,-3,-4,-25,-1,-29,-8,-30,-12,-20,-21,-14,-17,-2,-11,-28,-10,-9,]),'PLUS':([2,3,4,5,7,9,10,11,12,13,15,16,18,19,21,33,34,38,39,40,41,42,43,48,51,53,55,56,],[-5,-6,-26,-7,-24,-27,-13,30,-4,-25,-24,30,-29,-24,30,-8,-30,-12,30,30,30,-14,30,-11,-28,30,-10,-9,]),'NEWLINE':([2,3,4,5,7,9,10,11,12,13,14,18,33,34,38,40,41,42,43,48,51,55,56,],[-5,-6,-26,-7,-24,-27,-13,-3,-4,-25,31,-29,-8,-30,-12,-20,-21,-14,-17,-11,-28,-10,-9,]),'LSQUARE':([0,6,8,22,23,24,25,26,28,29,30,31,35,49,50,],[8,8,8,8,-22,8,-23,8,8,-19,-18,8,8,8,8,]),'RSQUARE':([2,3,4,5,7,8,9,10,12,13,17,18,19,20,21,33,34,38,40,41,42,43,46,48,51,52,55,56,],[-5,-6,-26,-7,-24,18,-27,-13,-4,-25,34,-29,-24,-33,-34,-8,-30,-12,-20,-21,-14,-17,-31,-11,-28,-32,-10,-9,]),'INTEGER':([0,6,8,22,23,24,25,26,28,29,30,31,32,35,47,49,50,],[7,15,19,7,-22,7,-23,7,7,-19,-18,7,45,7,52,7,7,]),'DOT':([2,3,4,5,7,9,10,11,12,13,15,16,18,19,21,33,34,36,38,39,40,41,42,43,48,51,53,55,56,],[-5,-6,-26,-7,-24,-27,-13,27,-4,-25,-24,27,-29,36,27,-8,-30,47,-12,27,27,27,-14,27,-11,-28,27,-10,-9,]),'STRING':([0,6,8,22,23,24,25,26,28,29,30,31,35,49,50,],[13,13,13,13,-22,13,-23,13,13,-19,-18,13,13,13,13,]),'COMMA':([2,3,4,5,7,9,10,12,13,15,17,18,19,20,21,33,34,37,38,39,40,41,42,43,46,48,51,52,53,54,55,56,],[-5,-6,-26,-7,-24,-27,-13,-4,-25,32,35,-29,-24,-33,-34,-8,-30,49,-12,-16,-20,-21,-14,-17,-31,-11,-28,-32,-15,49,-10,-9,]),'IDENTIFIER':([0,6,8,22,23,24,25,26,27,28,29,30,31,35,49,50,],[10,10,10,10,-22,10,-23,10,42,10,-19,-18,10,10,10,10,]),'EQUALS':([10,],[24,]),'MINUS_EQUALS':([10,],[25,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'ORDERED_PAIR':([0,6,8,22,24,26,28,31,35,49,50,],[4,4,4,4,4,4,4,4,4,4,4,]),'COMMA_ARGS':([22,50,],[37,54,]),'BINARY_OPERATOR':([11,16,21,39,40,41,43,53,],[28,28,28,28,28,28,28,28,]),'FUNCTION_CALL':([0,6,8,22,24,26,28,31,35,49,50,],[5,5,5,5,5,5,5,5,5,5,5,]),'LINES':([0,31,],[1,44,]),'ELEMENTS':([8,],[17,]),'LIST':([0,6,8,22,24,26,28,31,35,49,50,],[9,9,9,9,9,9,9,9,9,9,9,]),'LINE':([0,31,],[14,14,]),'ASSIGNMENT':([0,6,8,22,24,26,28,31,35,49,50,],[2,2,2,2,2,2,2,2,2,2,2,]),'MOD_ASSIGNMENT':([0,6,8,22,24,26,28,31,35,49,50,],[3,3,3,3,3,3,3,3,3,3,3,]),'ELEMENT':([8,35,],[20,46,]),'EXPRESSION':([0,6,8,22,24,26,28,31,35,49,50,],[11,16,21,39,40,41,43,11,21,53,39,]),'LITERAL':([0,6,8,22,24,26,28,31,35,49,50,],[12,12,12,12,12,12,12,12,12,12,12,]),'ASSIGN_OPERATOR':([10,],[26,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> LINES","S'",1,None,None,None),
  ('LINES -> LINE','LINES',1,'p_LINES','Simplified_Parser4.py',61),
  ('LINES -> LINE NEWLINE LINES','LINES',3,'p_LINES','Simplified_Parser4.py',62),
  ('LINE -> EXPRESSION','LINE',1,'p_LINE','Simplified_Parser4.py',73),
  ('EXPRESSION -> LITERAL','EXPRESSION',1,'p_EXPRESSION','Simplified_Parser4.py',79),
  ('EXPRESSION -> ASSIGNMENT','EXPRESSION',1,'p_EXPRESSION','Simplified_Parser4.py',80),
  ('EXPRESSION -> MOD_ASSIGNMENT','EXPRESSION',1,'p_EXPRESSION','Simplified_Parser4.py',81),
  ('EXPRESSION -> FUNCTION_CALL','EXPRESSION',1,'p_EXPRESSION','Simplified_Parser4.py',82),
  ('EXPRESSION -> LPAREN EXPRESSION RPAREN','EXPRESSION',3,'p_parenthesized_expression','Simplified_Parser4.py',88),
  ('FUNCTION_CALL -> EXPRESSION DOT IDENTIFIER LPAREN COMMA_ARGS RPAREN','FUNCTION_CALL',6,'p_FUNCTION_CALL','Simplified_Parser4.py',101),
  ('FUNCTION_CALL -> EXPRESSION DOT IDENTIFIER LPAREN RPAREN','FUNCTION_CALL',5,'p_FUNCTION_CALL','Simplified_Parser4.py',102),
  ('FUNCTION_CALL -> IDENTIFIER LPAREN COMMA_ARGS RPAREN','FUNCTION_CALL',4,'p_FUNCTION_CALL','Simplified_Parser4.py',103),
  ('FUNCTION_CALL -> IDENTIFIER LPAREN RPAREN','FUNCTION_CALL',3,'p_FUNCTION_CALL','Simplified_Parser4.py',104),
  ('FUNCTION_CALL -> IDENTIFIER','FUNCTION_CALL',1,'p_FUNCTION_CALL','Simplified_Parser4.py',105),
  ('FUNCTION_CALL -> EXPRESSION DOT IDENTIFIER','FUNCTION_CALL',3,'p_member_access','Simplified_Parser4.py',120),
  ('COMMA_ARGS -> COMMA_ARGS COMMA EXPRESSION','COMMA_ARGS',3,'p_COMMA_ARGS','Simplified_Parser4.py',124),
  ('COMMA_ARGS -> EXPRESSION','COMMA_ARGS',1,'p_COMMA_ARGS','Simplified_Parser4.py',125),
  ('FUNCTION_CALL -> EXPRESSION BINARY_OPERATOR EXPRESSION','FUNCTION_CALL',3,'p_operator_call','Simplified_Parser4.py',133),
  ('BINARY_OPERATOR -> PLUS','BINARY_OPERATOR',1,'p_BINARY_OPERATOR','Simplified_Parser4.py',139),
  ('BINARY_OPERATOR -> MINUS','BINARY_OPERATOR',1,'p_BINARY_OPERATOR','Simplified_Parser4.py',140),
  ('ASSIGNMENT -> IDENTIFIER EQUALS EXPRESSION','ASSIGNMENT',3,'p_ASSIGNMENT','Simplified_Parser4.py',147),
  ('MOD_ASSIGNMENT -> IDENTIFIER ASSIGN_OPERATOR EXPRESSION','MOD_ASSIGNMENT',3,'p_MOD_ASSIGNMENT','Simplified_Parser4.py',153),
  ('ASSIGN_OPERATOR -> PLUS_EQUALS','ASSIGN_OPERATOR',1,'p_ASSIGN_OPERATOR','Simplified_Parser4.py',157),
  ('ASSIGN_OPERATOR -> MINUS_EQUALS','ASSIGN_OPERATOR',1,'p_ASSIGN_OPERATOR','Simplified_Parser4.py',158),
  ('LITERAL -> INTEGER','LITERAL',1,'p_LITERAL','Simplified_Parser4.py',162),
  ('LITERAL -> STRING','LITERAL',1,'p_LITERAL','Simplified_Parser4.py',163),
  ('LITERAL -> ORDERED_PAIR','LITERAL',1,'p_LITERAL','Simplified_Parser4.py',164),
  ('LITERAL -> LIST','LITERAL',1,'p_LITERAL','Simplified_Parser4.py',165),
  ('ORDERED_PAIR -> LPAREN INTEGER COMMA INTEGER RPAREN','ORDERED_PAIR',5,'p_ORDERED_PAIR','Simplified_Parser4.py',171),
  ('LIST -> LSQUARE RSQUARE','LIST',2,'p_LIST','Simplified_Parser4.py',177),
  ('LIST -> LSQUARE ELEMENTS RSQUARE','LIST',3,'p_LIST','Simplified_Parser4.py',178),
  ('ELEMENTS -> ELEMENTS COMMA ELEMENT','ELEMENTS',3,'p_ELEMENTS','Simplified_Parser4.py',194),
  ('ELEMENTS -> INTEGER DOT DOT INTEGER','ELEMENTS',4,'p_ELEMENTS','Simplified_Parser4.py',195),
  ('ELEMENTS -> ELEMENT','ELEMENTS',1,'p_ELEMENTS','Simplified_Parser4.py',196),
  ('ELEMENT -> EXPRESSION','ELEMENT',1,'p_ELEMENT','Simplified_Parser4.py',209),
]
