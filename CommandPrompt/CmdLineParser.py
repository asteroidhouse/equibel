from ply import lex
from ply import yacc

#--------------------------------------------------------------------------------
#                                  LEXER
#--------------------------------------------------------------------------------
tokens = ("STRING", "INTEGER", "COMMA", "DOT", "LPAREN", "RPAREN", "LSQUARE", "RSQUARE")

t_STRING = r'\w+'
t_COMMA = r','
t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'

t_ignore = " \t\n"


def t_INTEGER(t):
     r"0|[1-9][0-9]*"
     t.value = int(t.value)
     return t

def t_NEWLINE(t):
     r"\n+"
     t.lexer.lineno += len(t.value)
     return t

def t_error(t):
     line = t.value.lstrip()
     i = line.find("\n")
     line = line if i == -1 else line[:i]
     raise ValueError("Syntax error, line {0}: {1}".format(t.lineno + 1, line))

#--------------------------------------------------------------------------------
#                                  PARSER
#--------------------------------------------------------------------------------

def p_LIST(p):
     """LIST : LSQUARE ITEMS RSQUARE
             | LSQUARE RANGE RSQUARE
             | LSQUARE RSQUARE"""
     p[0] = [] if len(p) == 3 else p[2]

def p_RANGE(p):
     """RANGE : INTEGER DOT DOT INTEGER"""
     p[0] = list(range(p[1], p[4] + 1))

def p_ITEMS(p):
     """ITEMS : ITEM
              | ITEM COMMA ITEMS"""
     p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

def p_ITEM(p):
     """ITEM : INTEGER
             | STRING
             | TUPLE"""
     p[0] = p[1]

def p_TUPLE(p):
     """TUPLE : LPAREN INTEGER COMMA INTEGER RPAREN"""
     p[0] = (int(p[2]), int(p[4]))

def p_error(p):
     if p is None:
          raise ValueError("Unknown error")
     raise ValueError("Syntax error, line {0}: {1}".format(p.lineno + 1, p.type))

lexer = lex.lex()

tuple_parser = yacc.yacc(start='TUPLE')
list_parser  = yacc.yacc(start='LIST')


def parse_tuple(text):
     try:
          return tuple_parser.parse(text, lexer=lexer)
     except ValueError as err:
          print(err)

def parse_list(text):
     try:
          return list_parser.parse(text, lexer=lexer)
     except ValueError as err:
          print(err)
