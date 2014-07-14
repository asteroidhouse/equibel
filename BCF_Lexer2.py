import ply.lex
import ply.yacc
import pprint
import sys


def parse_bcf(text):
     keywords = {
          "e": "EDGE_START", 
          "a": "ALPHABET_START",
          "w": "WEIGHT_START",
          "f": "FORMULA_START"
     }

     tokens = (["NEG", "AND", "OR", "LPAREN", "RPAREN", "INTEGER", "IDENTIFIER", "NEWLINE", 
                "WHITESPACE"] + list(keywords.values()))

     states = (("within", "exclusive"),)

     t_within_NEG = r'\-'
     t_within_AND = r'\*'
     t_within_OR = r'\+'
     t_within_LPAREN = r'\('
     t_within_RPAREN = r'\)'
     t_within_INTEGER = r'0|[1-9][0-9]*'
     t_ANY_WHITESPACE = r'[ \t]+'
     t_within_IDENTIFIER = r'[_a-zA-Z][_a-zA-Z0-9]*'

     def t_LINE_TYPE(t):
          r"[a-zA-Z][_a-zA-Z0-9]*"
          t.type = keywords.get(t.value, "IDENTIFIER")
          t.lexer.begin("within")
          return t

     def t_within_NEWLINE(t):
          r"\n+"
          t.lexer.lineno += len(t.value)
          t.lexer.begin("INITIAL")
          return t

     def t_within_error(t):
          line = t.value.lstrip()
          i = line.find("\n")
          line = line if i == -1 else line[:i]
          raise ValueError("Syntax error, line {0}: {1}".format(t.lineno + 1, line))

     def t_error(t):
          line = t.value.lstrip()
          i = line.find("\n")
          line = line if i == -1 else line[:i]
          raise ValueError("Syntax error, line {0}: {1}".format(t.lineno + 1, line))

     lexer = ply.lex.lex()
     lexer.input(text)

     for token in lexer:
          print(token)
     
     return []


if __name__ == '__main__':
     if len(sys.argv) < 2:
          print('usage: python3 BCF_Parser.py file')
          sys.exit(1)

     filename = sys.argv[1]
     f = open(filename, 'r')
     
     token_list = parse_bcf(f.read())

     pprint.pprint(token_list)
