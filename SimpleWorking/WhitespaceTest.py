import sys
import ply.lex
import ply.yacc

def parse_whitespace(text):
     tokens = ("WHITESPACE", "LPAREN", "WORD", "RPAREN", "NEWLINE")

     t_WHITESPACE = r'[ \t]+'
     t_LPAREN = r'\('
     t_RPAREN = r'\)'
     t_WORD = r'[a-zA-Z][a-zA-Z0-9]*'
     
     def t_NEWLINE(t):
          r"\n+"
          t.lexer.lineno += len(t.value)
          return t
     
     def t_error(t):
          line = t.value.lstrip()
          i = line.find("\n")
          line = line if i == -1 else line[:i]
          raise ValueError("Syntax error, line {0}: {1}".format(t.lineno + 1, line))

     def p_ITEM(p):
          """ITEM : LPAREN OPT_WHITE THING OPT_WHITE RPAREN"""
          p[0] = p[3]

     def p_THING(p):
          """THING : WORD"""
          p[0] = p[1]

     def p_OPT_WHITE(p):
          """OPT_WHITE : WHITESPACE
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
          print('usage: python3 WhitespaceTest.py file')
          sys.exit(1)

     filename = sys.argv[1]
     f = open(filename, 'r')
     
     token_list = parse_whitespace(f.read().strip())

     print(token_list)
