import ply.lex
import ply.yacc
import pprint
import sys

def parse_bcf(text):
     keywords = {"e": "EDGE_START", "a": "ALPHABET_START"}
     tokens = (["SYMBOL", "ZERO", "ALPHA", "POS_DIGIT", "WHITESPACE", "NEWLINE"] + list(keywords.values()))

     t_ZERO = r'0'
     t_ALPHA = r'[a-zA-Z]'
     t_POS_DIGIT = r'[1-9]'
     t_WHITESPACE = r'[ \t]+'
     t_NEWLINE = r'\n'

     start = 'FILE'

     def t_SYMBOL(t):
          r"[a-zA-Z]\w*"
          t.type = keywords.get(t.value, "SYMBOL")
          return t

     def t_newline(t):
          r"\n+"
          t.lexer.lineno += len(t.value)

     def t_error(t):
          line = t.value.lstrip()
          i = line.find("\n")
          line = line if i == -1 else line[:i]
          raise ValueError("Syntax error, line {0}: {1}".format(t.lineno + 1, line))

     def p_OPT_WHITESPACE(p):
          """OPT_WHITESPACE : WHITESPACE
                            | empty"""
          pass
     
     def p_empty(p):
          """empty :"""
          pass

     def p_FILE(p):
          """FILE : LINES"""
          p[0] = p[1]

     def p_LINES(p):
          """LINES : OPT_WHITESPACE LINE OPT_WHITESPACE
                   | OPT_WHITESPACE LINE OPT_WHITESPACE LINES"""
          p[0] = [p[2]] if len(p) == 4 else [p[2]] + p[4]

     def p_LINE(p):
          """LINE : EDGE_LINE
                  | ALPHABET_LINE"""
          p[0] = p[1]

     def p_EDGE_LINE(p):
          """EDGE_LINE : EDGE_START WHITESPACE EDGE"""
          #print("Edge start")
          p[0] = p[3]

     def p_ALPHABET_LINE(p):
          """ALPHABET_LINE : ALPHABET_START WHITESPACE ATOM_LIST"""
          p[0] = p[3]

     def p_ATOM_LIST(p):
          """ATOM_LIST : ATOM
                       | ATOM WHITESPACE ATOM_LIST"""
          p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

     def p_ATOM(p):
          """ATOM : SYMBOL"""
          p[0] = p[1]

     def p_EDGE(p):
          """EDGE : NODE WHITESPACE NODE"""
          p[0] = (p[1], p[3])

     def p_NODE(p):
          """NODE : INTEGER"""
          p[0] = p[1]

     def p_ALPHANUM_STR(p):
          """ALPHANUM_STR : ALPHANUM
                          | ALPHANUM ALPHANUM_STR"""
          p[0] = p[1] if len(p) == 2 else p[1] + p[2]

     def p_ALPHANUM(p):
          """ALPHANUM : ALPHA
                      | DIGIT"""
          p[0] = str(p[1])

     def p_INTEGER(p):
          """INTEGER : DIGIT
                     | POS_DIGIT DIGITS"""
          #print("integer")
          p[0] = p[1] if len(p) == 2 else int(str(p[1]) + str(p[2]))

     def p_DIGITS(p):
          """DIGITS : DIGIT
                    | DIGIT DIGITS"""
          p[0] = int(p[1]) if len(p) == 2 else int(str(p[1]) + str(p[2]))

     def p_DIGIT(p):
          """DIGIT : ZERO
                   | POS_DIGIT"""
          p[0] = int(p[1])

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
     
     token_list = parse_bcf(f.read())

     pprint.pprint(token_list)
