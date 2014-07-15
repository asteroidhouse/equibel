
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = b'\xbb\xdb\xb6\xe4\xe0\xe9w\x17>npz\x9c\x08\x08\xbe'
    
_lr_action_items = {'IDENTIFIER':([0,2,4,5,6,20,22,23,24,26,27,30,32,39,42,49,51,62,65,],[-37,-35,-36,11,-37,-32,-31,-30,-29,-37,11,-34,-33,11,-37,11,11,-37,11,]),'LPAREN':([0,2,4,5,6,8,11,20,22,23,24,25,26,27,30,32,39,42,49,51,53,60,62,65,],[-37,-35,-36,7,-37,-37,26,-32,-31,-30,-29,7,-37,7,-34,-33,7,-37,7,7,-37,7,-37,7,]),'LSQUARE':([0,2,4,5,6,20,22,23,24,26,27,30,32,39,42,49,51,62,65,],[-37,-35,-36,8,-37,-32,-31,-30,-29,-37,8,-34,-33,8,-37,8,8,-37,8,]),'RPAREN':([4,9,10,11,12,13,14,15,16,18,20,22,23,24,26,30,32,35,39,40,41,46,47,48,49,50,54,55,56,57,58,61,63,66,67,68,],[-36,-17,-18,-5,-7,-19,-8,-6,-4,-20,-32,-31,-30,-29,-37,-34,-33,-22,47,-9,-37,-37,-12,-37,-35,-10,-23,61,-14,-11,-16,-13,-37,68,-15,-21,]),'EQUALS':([4,11,27,28,],[-36,-37,-35,42,]),'$end':([1,6,19,],[0,-1,-2,]),'COMMA':([4,9,10,11,12,13,14,15,16,18,20,22,23,24,30,31,32,33,34,35,36,37,40,41,43,44,47,48,49,50,54,56,57,58,61,68,],[-36,-17,-18,-5,-7,-19,-8,-6,-4,-20,-32,-31,-30,-29,-34,-37,-33,-37,-28,-22,-27,-26,-9,-37,52,53,-12,-37,-35,-10,-23,62,-11,-16,-13,-21,]),'NEWLINE':([2,3,4,7,8,9,10,11,12,13,14,15,16,17,18,20,22,23,24,26,29,30,31,32,33,34,35,36,37,38,40,41,44,46,47,48,49,50,52,53,54,56,57,58,61,62,63,64,67,68,],[-35,6,-36,20,20,-17,-18,-5,-7,-19,-8,-6,-4,-37,-20,20,20,-30,-29,20,-3,-34,20,-33,20,-28,-22,-27,-26,20,-9,-37,-24,20,-12,20,-35,-10,20,20,-23,-14,-11,-16,-13,20,20,-25,-15,-21,]),'WHITESPACE':([0,4,6,7,8,9,10,11,12,13,14,15,16,17,18,20,22,23,24,26,30,31,32,33,34,35,36,37,38,40,41,42,44,46,47,48,49,50,52,53,54,56,57,58,61,62,63,64,67,68,],[2,-36,2,22,22,-17,-18,27,-7,-19,-8,-6,-4,2,-20,22,22,-30,-29,22,-34,22,-33,22,-28,-22,-27,-26,22,-9,49,2,-24,22,-12,22,-35,-10,22,22,-23,-14,-11,-16,-13,22,22,-25,-15,-21,]),'INTEGER':([0,2,4,5,6,7,8,20,21,22,23,24,25,26,27,30,32,39,42,49,51,52,53,59,60,62,65,],[-37,-35,-36,9,-37,-37,-37,-32,31,-31,-30,-29,37,-37,9,-34,-33,9,-37,9,9,-37,-37,63,37,-37,9,]),'RSQUARE':([8,20,22,23,24,25,30,32,33,34,36,37,38,44,45,64,68,],[-37,-32,-31,-30,-29,35,-34,-33,-37,-28,-27,-26,-37,-24,54,-25,-21,]),'STRING':([0,2,4,5,6,8,20,22,23,24,25,26,27,30,32,39,42,49,51,53,60,62,65,],[-37,-35,-36,10,-37,-37,-32,-31,-30,-29,36,-37,10,-34,-33,10,-37,10,10,-37,36,-37,10,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'FUNCTION_CALL':([5,27,39,49,51,65,],[12,12,12,12,12,12,]),'ARGS':([27,49,],[40,57,]),'ELEMENT':([25,60,],[33,33,]),'WHITESPACE_NEWLINE':([7,8,20,22,26,31,33,38,46,48,52,53,62,63,],[24,24,30,32,24,24,24,24,24,24,24,24,24,24,]),'COMMA_ARGS':([39,65,],[46,67,]),'EXPRESSION':([5,27,39,49,51,65,],[17,41,48,41,58,48,]),'LINES':([0,6,],[1,19,]),'ORDERED_PAIR':([5,25,27,39,49,51,60,65,],[13,34,13,13,13,13,34,13,]),'CONSTRUCTOR':([5,27,39,49,51,65,],[14,14,14,14,14,14,]),'ASSIGNMENT':([5,27,39,49,51,65,],[15,15,15,15,15,15,]),'LITERAL':([5,27,39,49,51,65,],[16,16,16,16,16,16,]),'LINE':([0,6,],[3,3,]),'OPT_WHITE_NEWLINE':([7,8,26,31,33,38,46,48,52,53,62,63,],[21,25,39,43,44,45,55,56,59,60,65,66,]),'ELEMENTS':([25,60,],[38,64,]),'empty':([0,6,7,8,11,17,26,31,33,38,41,42,46,48,52,53,62,63,],[4,4,23,23,4,4,23,23,23,23,4,4,23,23,23,23,23,23,]),'OPT_WHITE':([0,6,11,17,41,42,],[5,5,28,29,50,51,]),'LIST':([5,27,39,49,51,65,],[18,18,18,18,18,18,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> LINES","S'",1,None,None,None),
  ('LINES -> LINE NEWLINE','LINES',2,'p_LINES','Equibel_Parser2.py',50),
  ('LINES -> LINE NEWLINE LINES','LINES',3,'p_LINES','Equibel_Parser2.py',51),
  ('LINE -> OPT_WHITE EXPRESSION OPT_WHITE','LINE',3,'p_LINE','Equibel_Parser2.py',56),
  ('EXPRESSION -> LITERAL','EXPRESSION',1,'p_EXPRESSION','Equibel_Parser2.py',61),
  ('EXPRESSION -> IDENTIFIER','EXPRESSION',1,'p_EXPRESSION','Equibel_Parser2.py',62),
  ('EXPRESSION -> ASSIGNMENT','EXPRESSION',1,'p_EXPRESSION','Equibel_Parser2.py',63),
  ('EXPRESSION -> FUNCTION_CALL','EXPRESSION',1,'p_EXPRESSION','Equibel_Parser2.py',64),
  ('EXPRESSION -> CONSTRUCTOR','EXPRESSION',1,'p_EXPRESSION','Equibel_Parser2.py',65),
  ('FUNCTION_CALL -> IDENTIFIER WHITESPACE ARGS','FUNCTION_CALL',3,'p_FUNCTION_CALL','Equibel_Parser2.py',73),
  ('ARGS -> EXPRESSION OPT_WHITE','ARGS',2,'p_ARGS','Equibel_Parser2.py',77),
  ('ARGS -> EXPRESSION WHITESPACE ARGS','ARGS',3,'p_ARGS','Equibel_Parser2.py',78),
  ('CONSTRUCTOR -> IDENTIFIER LPAREN OPT_WHITE_NEWLINE RPAREN','CONSTRUCTOR',4,'p_CONSTRUCTOR','Equibel_Parser2.py',83),
  ('CONSTRUCTOR -> IDENTIFIER LPAREN OPT_WHITE_NEWLINE COMMA_ARGS OPT_WHITE_NEWLINE RPAREN','CONSTRUCTOR',6,'p_CONSTRUCTOR','Equibel_Parser2.py',84),
  ('COMMA_ARGS -> EXPRESSION OPT_WHITE_NEWLINE','COMMA_ARGS',2,'p_COMMA_ARGS','Equibel_Parser2.py',91),
  ('COMMA_ARGS -> EXPRESSION OPT_WHITE_NEWLINE COMMA OPT_WHITE_NEWLINE COMMA_ARGS','COMMA_ARGS',5,'p_COMMA_ARGS','Equibel_Parser2.py',92),
  ('ASSIGNMENT -> IDENTIFIER OPT_WHITE EQUALS OPT_WHITE EXPRESSION','ASSIGNMENT',5,'p_ASSIGNMENT','Equibel_Parser2.py',97),
  ('LITERAL -> INTEGER','LITERAL',1,'p_LITERAL','Equibel_Parser2.py',102),
  ('LITERAL -> STRING','LITERAL',1,'p_LITERAL','Equibel_Parser2.py',103),
  ('LITERAL -> ORDERED_PAIR','LITERAL',1,'p_LITERAL','Equibel_Parser2.py',104),
  ('LITERAL -> LIST','LITERAL',1,'p_LITERAL','Equibel_Parser2.py',105),
  ('ORDERED_PAIR -> LPAREN OPT_WHITE_NEWLINE INTEGER OPT_WHITE_NEWLINE COMMA OPT_WHITE_NEWLINE INTEGER OPT_WHITE_NEWLINE RPAREN','ORDERED_PAIR',9,'p_ORDERED_PAIR','Equibel_Parser2.py',109),
  ('LIST -> LSQUARE OPT_WHITE_NEWLINE RSQUARE','LIST',3,'p_LIST','Equibel_Parser2.py',115),
  ('LIST -> LSQUARE OPT_WHITE_NEWLINE ELEMENTS OPT_WHITE_NEWLINE RSQUARE','LIST',5,'p_LIST','Equibel_Parser2.py',116),
  ('ELEMENTS -> ELEMENT OPT_WHITE_NEWLINE','ELEMENTS',2,'p_ELEMENTS','Equibel_Parser2.py',125),
  ('ELEMENTS -> ELEMENT OPT_WHITE_NEWLINE COMMA OPT_WHITE_NEWLINE ELEMENTS','ELEMENTS',5,'p_ELEMENTS','Equibel_Parser2.py',126),
  ('ELEMENT -> INTEGER','ELEMENT',1,'p_ELEMENT','Equibel_Parser2.py',133),
  ('ELEMENT -> STRING','ELEMENT',1,'p_ELEMENT','Equibel_Parser2.py',134),
  ('ELEMENT -> ORDERED_PAIR','ELEMENT',1,'p_ELEMENT','Equibel_Parser2.py',135),
  ('OPT_WHITE_NEWLINE -> WHITESPACE_NEWLINE','OPT_WHITE_NEWLINE',1,'p_OPT_WHITE_NEWLINE','Equibel_Parser2.py',140),
  ('OPT_WHITE_NEWLINE -> empty','OPT_WHITE_NEWLINE',1,'p_OPT_WHITE_NEWLINE','Equibel_Parser2.py',141),
  ('WHITESPACE_NEWLINE -> WHITESPACE','WHITESPACE_NEWLINE',1,'p_WHITESPACE_NEWLINE','Equibel_Parser2.py',145),
  ('WHITESPACE_NEWLINE -> NEWLINE','WHITESPACE_NEWLINE',1,'p_WHITESPACE_NEWLINE','Equibel_Parser2.py',146),
  ('WHITESPACE_NEWLINE -> WHITESPACE WHITESPACE_NEWLINE','WHITESPACE_NEWLINE',2,'p_WHITESPACE_NEWLINE','Equibel_Parser2.py',147),
  ('WHITESPACE_NEWLINE -> NEWLINE WHITESPACE_NEWLINE','WHITESPACE_NEWLINE',2,'p_WHITESPACE_NEWLINE','Equibel_Parser2.py',148),
  ('OPT_WHITE -> WHITESPACE','OPT_WHITE',1,'p_OPT_WHITE','Equibel_Parser2.py',152),
  ('OPT_WHITE -> empty','OPT_WHITE',1,'p_OPT_WHITE','Equibel_Parser2.py',153),
  ('empty -> <empty>','empty',0,'p_empty','Equibel_Parser2.py',157),
]
