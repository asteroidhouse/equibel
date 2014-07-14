import ply.lex
import ply.yacc
import sys
import pprint

def parse_equibel(text):
     tokens = ("IDENTIFIER", "INTEGER", "STRING", "LPAREN", "RPAREN", "COMMA", "LSQUARE", "RSQUARE",
               "WHITESPACE", "NEWLINE")

     #t_ORDERED_PAIR = r'\(\s*(0|[1-9][0-9]*)\s*,\s*(0|[1-9][0-9]*)\s*\)'
     t_IDENTIFIER = r'[a-zA-Z][_a-zA-Z0-9]*'

     t_LPAREN  = r'\('
     t_RPAREN  = r'\)'
     t_LSQUARE = r'\['
     t_RSQUARE = r'\]'

     t_COMMA   = r','

     t_WHITESPACE = r'[ \t]+'

     def t_INTEGER(t):
          r'0|[1-9][0-9]*'
          t.value = int(t.value)
          return t

     def t_STRING(t):
          r'"[^"]*"|\'[^\']*\''
          t.value = t.value[1:-1]
          return t

     def t_NEWLINE(t):
          r"[\n]+"
          t.lexer.lineno += len(t.value)
          return t

     def t_error(t):
          line = t.value.lstrip()
          i = line.find("\n")
          line = line if i == -1 else line[:i]
          print("failed to parse {0}: {1}".format(t.lineno + 1, line))

     lexer = ply.lex.lex()
     lexer.input(text)

     for token in lexer:
          print(token)

if __name__ == '__main__':
     if len(sys.argv) < 2:
          print("usage: python3 Equibel_Parser.py file")
          sys.exit(1)

     filename = sys.argv[1]
     f = open(filename, 'r')

     tokens = parse_equibel(f.read())
     pprint.pprint(tokens)
