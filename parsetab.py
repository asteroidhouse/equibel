
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = b'\xbb\xdb\xb6\xe4\xe0\xe9w\x17>npz\x9c\x08\x08\xbe'
    
_lr_action_items = {'$end':([5,6,19,],[0,-1,-2,]),'WHITESPACE':([0,3,6,7,8,9,10,11,12,13,14,15,16,17,18,22,23,24,25,26,30,31,32,33,34,35,36,37,39,40,41,42,43,45,46,47,48,49,52,53,54,56,57,58,60,61,63,65,66,68,],[2,-36,2,2,-4,23,-7,-8,-6,27,-20,-18,23,-17,-19,-29,23,-30,23,23,-27,-26,23,-22,-28,23,-33,-34,48,-9,2,23,-24,23,23,-12,-35,-10,23,-23,-14,-11,-16,23,23,-13,-25,23,-15,-21,]),'IDENTIFIER':([0,2,3,4,6,22,23,24,25,26,27,36,37,38,41,48,50,60,64,],[-37,-35,-36,13,-37,-29,-31,-30,-32,-37,13,-33,-34,13,-37,13,13,-37,13,]),'EQUALS':([3,13,27,28,],[-36,-37,-35,41,]),'LSQUARE':([0,2,3,4,6,22,23,24,25,26,27,36,37,38,41,48,50,60,64,],[-37,-35,-36,9,-37,-29,-31,-30,-32,-37,9,-33,-34,9,-37,9,9,-37,9,]),'STRING':([0,2,3,4,6,9,21,22,23,24,25,26,27,36,37,38,41,48,50,52,59,60,64,],[-37,-35,-36,15,-37,-37,30,-29,-31,-30,-32,-37,15,-33,-34,15,-37,15,15,-37,30,-37,15,]),'LPAREN':([0,2,3,4,6,9,13,21,22,23,24,25,26,27,36,37,38,41,48,50,52,59,60,64,],[-37,-35,-36,16,-37,-37,26,16,-29,-31,-30,-32,-37,16,-33,-34,16,-37,16,16,-37,16,-37,16,]),'COMMA':([3,8,10,11,12,13,14,15,17,18,22,23,24,25,30,31,32,33,34,36,37,39,40,42,43,45,47,48,49,51,53,54,56,57,61,68,],[-36,-4,-7,-8,-6,-5,-20,-18,-17,-19,-29,-31,-30,-32,-27,-26,-37,-22,-28,-33,-34,-37,-9,-37,52,-37,-12,-35,-10,58,-23,60,-11,-16,-13,-21,]),'INTEGER':([0,2,3,4,6,9,16,21,22,23,24,25,26,27,29,36,37,38,41,48,50,52,58,59,60,62,64,],[-37,-35,-36,17,-37,-37,-37,31,-29,-31,-30,-32,-37,17,42,-33,-34,17,-37,17,17,-37,-37,31,-37,65,17,]),'RSQUARE':([9,21,22,23,24,25,30,31,32,34,35,36,37,43,44,63,68,],[-37,33,-29,-31,-30,-32,-27,-26,-37,-28,-37,-33,-34,-24,53,-25,-21,]),'NEWLINE':([1,2,3,7,8,9,10,11,12,13,14,15,16,17,18,20,22,23,24,25,26,30,31,32,33,34,35,36,37,39,40,42,43,45,46,47,48,49,52,53,54,56,57,58,60,61,63,65,66,68,],[6,-35,-36,-37,-4,25,-7,-8,-6,-5,-20,-18,25,-17,-19,-3,-29,25,-30,25,25,-27,-26,25,-22,-28,25,-33,-34,-37,-9,25,-24,25,25,-12,-35,-10,25,-23,-14,-11,-16,25,25,-13,-25,25,-15,-21,]),'RPAREN':([3,8,10,11,12,13,14,15,17,18,22,23,24,25,26,33,36,37,38,39,40,45,46,47,48,49,53,54,55,56,57,61,65,66,67,68,],[-36,-4,-7,-8,-6,-5,-20,-18,-17,-19,-29,-31,-30,-32,-37,-22,-33,-34,47,-37,-9,-37,-37,-12,-35,-10,-23,-14,61,-11,-16,-13,-37,-15,68,-21,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'OPT_WHITE_NEWLINE':([9,16,26,32,35,42,45,46,52,58,60,65,],[21,29,38,43,44,51,54,55,59,62,64,67,]),'ELEMENTS':([21,59,],[35,63,]),'LINE':([0,6,],[1,1,]),'ELEMENT':([21,59,],[32,32,]),'ASSIGNMENT':([4,27,38,48,50,64,],[12,12,12,12,12,12,]),'EXPRESSION':([4,27,38,48,50,64,],[7,39,45,39,57,45,]),'LIST':([4,27,38,48,50,64,],[14,14,14,14,14,14,]),'WHITESPACE_NEWLINE':([9,16,23,25,26,32,35,42,45,46,52,58,60,65,],[22,22,36,37,22,22,22,22,22,22,22,22,22,22,]),'COMMA_ARGS':([38,64,],[46,66,]),'LITERAL':([4,27,38,48,50,64,],[8,8,8,8,8,8,]),'LINES':([0,6,],[5,19,]),'ARGS':([27,48,],[40,56,]),'FUNCTION_CALL':([4,27,38,48,50,64,],[10,10,10,10,10,10,]),'empty':([0,6,7,9,13,16,26,32,35,39,41,42,45,46,52,58,60,65,],[3,3,3,24,3,24,24,24,24,3,3,24,24,24,24,24,24,24,]),'OPT_WHITE':([0,6,7,13,39,41,],[4,4,20,28,49,50,]),'ORDERED_PAIR':([4,21,27,38,48,50,59,64,],[18,34,18,18,18,18,34,18,]),'CONSTRUCTOR':([4,27,38,48,50,64,],[11,11,11,11,11,11,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> LINES","S'",1,None,None,None),
  ('LINES -> LINE NEWLINE','LINES',2,'p_LINES','Equibel_Parser_AST.py',50),
  ('LINES -> LINE NEWLINE LINES','LINES',3,'p_LINES','Equibel_Parser_AST.py',51),
  ('LINE -> OPT_WHITE EXPRESSION OPT_WHITE','LINE',3,'p_LINE','Equibel_Parser_AST.py',61),
  ('EXPRESSION -> LITERAL','EXPRESSION',1,'p_EXPRESSION','Equibel_Parser_AST.py',66),
  ('EXPRESSION -> IDENTIFIER','EXPRESSION',1,'p_EXPRESSION','Equibel_Parser_AST.py',67),
  ('EXPRESSION -> ASSIGNMENT','EXPRESSION',1,'p_EXPRESSION','Equibel_Parser_AST.py',68),
  ('EXPRESSION -> FUNCTION_CALL','EXPRESSION',1,'p_EXPRESSION','Equibel_Parser_AST.py',69),
  ('EXPRESSION -> CONSTRUCTOR','EXPRESSION',1,'p_EXPRESSION','Equibel_Parser_AST.py',70),
  ('FUNCTION_CALL -> IDENTIFIER WHITESPACE ARGS','FUNCTION_CALL',3,'p_FUNCTION_CALL','Equibel_Parser_AST.py',77),
  ('ARGS -> EXPRESSION OPT_WHITE','ARGS',2,'p_ARGS','Equibel_Parser_AST.py',81),
  ('ARGS -> EXPRESSION WHITESPACE ARGS','ARGS',3,'p_ARGS','Equibel_Parser_AST.py',82),
  ('CONSTRUCTOR -> IDENTIFIER LPAREN OPT_WHITE_NEWLINE RPAREN','CONSTRUCTOR',4,'p_CONSTRUCTOR','Equibel_Parser_AST.py',87),
  ('CONSTRUCTOR -> IDENTIFIER LPAREN OPT_WHITE_NEWLINE COMMA_ARGS OPT_WHITE_NEWLINE RPAREN','CONSTRUCTOR',6,'p_CONSTRUCTOR','Equibel_Parser_AST.py',88),
  ('COMMA_ARGS -> EXPRESSION OPT_WHITE_NEWLINE','COMMA_ARGS',2,'p_COMMA_ARGS','Equibel_Parser_AST.py',95),
  ('COMMA_ARGS -> EXPRESSION OPT_WHITE_NEWLINE COMMA OPT_WHITE_NEWLINE COMMA_ARGS','COMMA_ARGS',5,'p_COMMA_ARGS','Equibel_Parser_AST.py',96),
  ('ASSIGNMENT -> IDENTIFIER OPT_WHITE EQUALS OPT_WHITE EXPRESSION','ASSIGNMENT',5,'p_ASSIGNMENT','Equibel_Parser_AST.py',101),
  ('LITERAL -> INTEGER','LITERAL',1,'p_LITERAL','Equibel_Parser_AST.py',106),
  ('LITERAL -> STRING','LITERAL',1,'p_LITERAL','Equibel_Parser_AST.py',107),
  ('LITERAL -> ORDERED_PAIR','LITERAL',1,'p_LITERAL','Equibel_Parser_AST.py',108),
  ('LITERAL -> LIST','LITERAL',1,'p_LITERAL','Equibel_Parser_AST.py',109),
  ('ORDERED_PAIR -> LPAREN OPT_WHITE_NEWLINE INTEGER OPT_WHITE_NEWLINE COMMA OPT_WHITE_NEWLINE INTEGER OPT_WHITE_NEWLINE RPAREN','ORDERED_PAIR',9,'p_ORDERED_PAIR','Equibel_Parser_AST.py',113),
  ('LIST -> LSQUARE OPT_WHITE_NEWLINE RSQUARE','LIST',3,'p_LIST','Equibel_Parser_AST.py',119),
  ('LIST -> LSQUARE OPT_WHITE_NEWLINE ELEMENTS OPT_WHITE_NEWLINE RSQUARE','LIST',5,'p_LIST','Equibel_Parser_AST.py',120),
  ('ELEMENTS -> ELEMENT OPT_WHITE_NEWLINE','ELEMENTS',2,'p_ELEMENTS','Equibel_Parser_AST.py',129),
  ('ELEMENTS -> ELEMENT OPT_WHITE_NEWLINE COMMA OPT_WHITE_NEWLINE ELEMENTS','ELEMENTS',5,'p_ELEMENTS','Equibel_Parser_AST.py',130),
  ('ELEMENT -> INTEGER','ELEMENT',1,'p_ELEMENT','Equibel_Parser_AST.py',137),
  ('ELEMENT -> STRING','ELEMENT',1,'p_ELEMENT','Equibel_Parser_AST.py',138),
  ('ELEMENT -> ORDERED_PAIR','ELEMENT',1,'p_ELEMENT','Equibel_Parser_AST.py',139),
  ('OPT_WHITE_NEWLINE -> WHITESPACE_NEWLINE','OPT_WHITE_NEWLINE',1,'p_OPT_WHITE_NEWLINE','Equibel_Parser_AST.py',144),
  ('OPT_WHITE_NEWLINE -> empty','OPT_WHITE_NEWLINE',1,'p_OPT_WHITE_NEWLINE','Equibel_Parser_AST.py',145),
  ('WHITESPACE_NEWLINE -> WHITESPACE','WHITESPACE_NEWLINE',1,'p_WHITESPACE_NEWLINE','Equibel_Parser_AST.py',149),
  ('WHITESPACE_NEWLINE -> NEWLINE','WHITESPACE_NEWLINE',1,'p_WHITESPACE_NEWLINE','Equibel_Parser_AST.py',150),
  ('WHITESPACE_NEWLINE -> WHITESPACE WHITESPACE_NEWLINE','WHITESPACE_NEWLINE',2,'p_WHITESPACE_NEWLINE','Equibel_Parser_AST.py',151),
  ('WHITESPACE_NEWLINE -> NEWLINE WHITESPACE_NEWLINE','WHITESPACE_NEWLINE',2,'p_WHITESPACE_NEWLINE','Equibel_Parser_AST.py',152),
  ('OPT_WHITE -> WHITESPACE','OPT_WHITE',1,'p_OPT_WHITE','Equibel_Parser_AST.py',156),
  ('OPT_WHITE -> empty','OPT_WHITE',1,'p_OPT_WHITE','Equibel_Parser_AST.py',157),
  ('empty -> <empty>','empty',0,'p_empty','Equibel_Parser_AST.py',161),
]
