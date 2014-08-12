import ply.lex
import ply.yacc
import sys

def parse_pm(text):
     tokens = ("PLUS", "MINUS", "EQUALS", "PLUS_EQUALS", "MINUS_EQUALS", "NEWLINE", "WHITESPACE")

     t_PLUS = r'\+'
     t_MINUS = r'\-'
     t_EQUALS = r'='
     t_PLUS_EQUALS = r'\+='
     t_MINUS_EQUALS = r'\-='

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

     lexer = ply.lex.lex()
     lexer.input(text)

     for token in lexer:
          print(token)

if __name__ == '__main__':
     if len(sys.argv) < 2:
          print('usage: python3 plus_minus.py file')
          sys.exit(1)

     filename = sys.argv[1]
     f = open(filename, 'r')
     
     parse_pm(f.read())
