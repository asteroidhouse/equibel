import ply.lex
import ply.yacc
import pprint
import sys

def parse_formula(text):
     tokens = ("NEG", "AND", "OR", "LPAREN", "RPAREN", "IDENTIFIER", "WHITESPACE", "NEWLINE")

     t_NEG = r'\-'
     t_AND = r'\*'
     t_OR = r'\+'
     t_LPAREN = r'\('
     t_RPAREN = r'\)'
     t_IDENTIFIER = r'[_a-zA-Z][_a-zA-Z0-9]*'

     t_WHITESPACE = r'[ \t]+'
     
     def t_NEWLINE(t):
          r"\n+"
          t.lexer.lineno += len(t.value)
          return t

     def t_error(t):
          line = t.value.lstrip()
          i = line.find("\n")
          line = line if i == -1 else line[:i]
          raise ValueError("Syntax error, line {0}: {1}".format(t.lineno + 1, line))

     def p_FORMULA_LINE(p):
          """FORMULA_LINE : OPT_WHITESPACE FORMULA OPT_WHITESPACE NEWLINE"""
          p[0] = p[2]

     def p_FORMULA(p):
          """FORMULA : LPAREN OPT_WHITESPACE FORM OPT_WHITESPACE RPAREN"""
          #print("formula")
          p[0] = p[3]

     def p_FORM(p):
          """FORM : OPT_WHITESPACE SIMPLE_FORM
                  | OPT_WHITESPACE COMPOUND_FORM"""
          #print("form")
          p[0] = p[2]

     def p_SIMPLE_FORM(p):
          """SIMPLE_FORM : ATOM
                         | NEG OPT_WHITESPACE ATOM
                         | LPAREN OPT_WHITESPACE FORM OPT_WHITESPACE RPAREN
                         | NEG OPT_WHITESPACE LPAREN OPT_WHITESPACE FORM OPT_WHITESPACE RPAREN"""
          #print("simple form")
          if len(p) == 2:
               p[0] = p[1]
          elif len(p) == 4:
               p[0] = (p[1], p[3])
          elif len(p) == 6:
               p[0] = p[3]
          elif len(p) == 8:
               p[0] = (p[1], p[5])
     
     def p_COMPOUND_FORM(p):
          """COMPOUND_FORM : OP OPT_WHITESPACE LPAREN OPT_WHITESPACE FORM_LIST OPT_WHITESPACE RPAREN"""
          #print("compound form")
          p[0] = (p[1], p[5])
     
     def p_FORM_LIST(p):
          """FORM_LIST : FORM
                       | FORM WHITESPACE FORM_LIST"""
          #print("form list")
          p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

     def p_ATOM(p):
          """ATOM : IDENTIFIER"""
          #print("atom")
          p[0] = p[1]

     def p_OP(p):
          """OP : AND
                | OR"""
          #print("op")
          p[0] = p[1]

     def p_OPT_WHITESPACE(p):
          """OPT_WHITESPACE : WHITESPACE
                            | empty"""
          pass
     
     def p_empty(p):
          """empty :"""
          pass

     def p_error(p):
          if p is None:
               raise ValueError("Unknown error")
          raise ValueError("Syntax error, line {0}: {1}".format(p.lineno + 1, p.type))

     lexer = ply.lex.lex()
     parser = ply.yacc.yacc()
     try:
          return parser.parse(text, lexer=lexer)
     except ValueError as err:
          print(err)
          return []


if __name__ == '__main__':
     if len(sys.argv) < 2:
          print('usage: python3 BCF_Parser.py file')
          sys.exit(1)

     filename = sys.argv[1]
     f = open(filename, 'r')
     
     token_list = parse_formula(f.read())

     pprint.pprint(token_list)
