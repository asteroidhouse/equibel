import ply.lex
import ply.yacc
import pprint
import sys

def parse_bcf(text):
     keywords = {
          "n": "NODE_START",
          "e": "EDGE_START", 
          "a": "ALPHABET_START",
          "w": "WEIGHT_START",
          "f": "FORMULA_START"
     }

     tokens = (["NEG", "AND", "OR", "LPAREN", "RPAREN", "INTEGER", "IDENTIFIER", "RANGE_OP",
                "NEWLINE", "WHITESPACE"] + list(keywords.values()))

     states = (("within", "exclusive"),)

     start = 'FILE'

     t_within_NEG = r'\-'
     t_within_AND = r'\*'
     t_within_OR = r'\+'
     t_within_LPAREN = r'\('
     t_within_RPAREN = r'\)'
     t_within_INTEGER = r'0|[1-9][0-9]*'

     t_within_RANGE_OP = r'\.\.'

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

     def p_OPT_WHITESPACE(p):
          """OPT_WHITESPACE : WHITESPACE
                            | empty"""
          pass
     
     def p_empty(p):
          """empty :"""
          pass

     def p_FILE(p):
          """FILE : LINES"""
          #print("file")
          p[0] = p[1]

     def p_LINES(p):
          """LINES : OPT_WHITESPACE LINE OPT_WHITESPACE NEWLINE
                   | OPT_WHITESPACE LINE OPT_WHITESPACE NEWLINE LINES"""
          #print("lines")
          p[0] = [p[2]] if len(p) == 5 else [p[2]] + p[5]

     def p_LINE(p):
          """LINE : NODE_LINE
                  | EDGE_LINE
                  | ALPHABET_LINE
                  | WEIGHT_LINE
                  | FORMULA_LINE"""
          #print("line")
          p[0] = p[1]

     def p_NODE_LINE(p):
          """NODE_LINE : NODE_START WHITESPACE NODE_LIST
                       | NODE_START WHITESPACE NODE_RANGE"""
          p[0] = p[3]

     def p_NODE_RANGE(p):
          """NODE_RANGE : NODE OPT_WHITESPACE RANGE_OP OPT_WHITESPACE NODE"""
          start = int(p[1])
          end = int(p[5])
          p[0] = list(range(start, end+1))

     def p_NODE_LIST(p):
          """NODE_LIST : NODE
                       | NODE WHITESPACE NODE_LIST"""
          p[0] = [int(p[1])] if len(p) == 2 else [int(p[1])] + p[3]
          
     def p_NODE(p):
          """NODE : INTEGER"""
          #print("node")
          p[0] = int(p[1])


     def p_EDGE_LINE(p):
          """EDGE_LINE : EDGE_START WHITESPACE EDGE"""
          #print("edge line")
          p[0] = p[3]

     def p_EDGE(p):
          """EDGE : NODE WHITESPACE NODE"""
          #print("edge")
          p[0] = (p[1], p[3])

     def p_ALPHABET_LINE(p):
          """ALPHABET_LINE : ALPHABET_START WHITESPACE ATOM_LIST"""
          #print("alphabet line")
          p[0] = p[3]

     def p_ATOM_LIST(p):
          """ATOM_LIST : ATOM
                       | ATOM WHITESPACE ATOM_LIST"""
          #print("atom list")
          p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

     def p_ATOM(p):
          """ATOM : IDENTIFIER"""
          #print("atom")
          p[0] = p[1]

     def p_WEIGHT_LINE(p):
          """WEIGHT_LINE : WEIGHT_START WHITESPACE NODE WHITESPACE ATOM WHITESPACE WEIGHT"""
          p[0] = (p[3], p[5], p[7])

     def p_WEIGHT(p):
          """WEIGHT : INTEGER"""
          p[0] = p[1]

     def p_FORMULA_LINE(p):
          """FORMULA_LINE : FORMULA_START WHITESPACE NODE WHITESPACE FORMULA"""
          #print("formula start")
          p[0] = (p[3], p[5])

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

     def p_OP(p):
          """OP : AND
                | OR"""
          #print("op")
          p[0] = p[1]


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
