import ply.lex
import ply.yacc
import sys
import pprint
from nodes import *

def parse_equibel(text):
     tokens = ("IDENTIFIER", "INTEGER", "STRING", "LPAREN", "RPAREN", "COMMA", "EQUALS",
               "PLUS", "MINUS", "PLUS_EQUALS", "MINUS_EQUALS", "LSQUARE", "RSQUARE", 
               "WHITESPACE", "NEWLINE")

     t_IDENTIFIER = r'[a-zA-Z][_a-zA-Z0-9]*'

     t_LPAREN  = r'\('
     t_RPAREN  = r'\)'
     t_LSQUARE = r'\['
     t_RSQUARE = r'\]'

     t_COMMA   = r','
     t_EQUALS  = r'='

     t_PLUS = r'\+'
     t_MINUS = r'\-'
     t_PLUS_EQUALS = r'\+='
     t_MINUS_EQUALS = r'\-='

     #t_ignore = " \t"
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



     #------------------------------------------------------------------------------------------------------
     #                                                PARSER
     #------------------------------------------------------------------------------------------------------
     def p_LINES(p):
          """LINES : LINE NEWLINE LINES 
                   | LINE NEWLINE"""
          print("lines")
          p[0] = Nodes([p[1]]) if len(p) == 3 else p[3].append(p[1])

     # TODO: Think about semicolon terminators, in terms of:
     #         1) Signaling the end of a statement, to allow multiple statements
     #            on the same line, and
     #         2) Indicating that output should be suppressed when executing the
     #            line.
     def p_LINE(p):
          """LINE : EXPRESSION"""
          print("line")
          p[0] = p[1]

     def p_EXPRESSION(p):
          """EXPRESSION : LITERAL
                        | ASSIGNMENT
                        | FUNCTION_CALL"""
          print("expression")
          p[0] = p[1]

     def p_parenthesized_expression(p):
          """EXPRESSION : LPAREN EXPRESSION RPAREN"""
          print("parenthesized expression")
          p[0] = p[2]

     # TODO: Also, think about adding support for qualifying function names 
     #       with receiver names, to allow 'methods' to be called on specific 
     #       objects. This would allow:
     #              g2.add_nodes [1,2,3,4]
     #       instead of requiring a context switch:
     #              use g2
     #              add_nodes [1,2,3,4]
     def p_FUNCTION_CALL(p):
          """FUNCTION_CALL : IDENTIFIER WHITESPACE ARGS
                           | IDENTIFIER"""
          print("function call")
          p[0] = CallNode(None, p[1]) if len(p) == 2 else CallNode(None, p[1], p[3])

     def p_ARGS(p):
          """ARGS : EXPRESSION WHITESPACE ARGS
                  | EXPRESSION"""
          print("args")
          p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]
     
     # Calling x + 2 is treated as x.+(2), that is, it invokes the + function of x, with 2 
     # as an argument.
     def p_operator_call(p):
          """FUNCTION_CALL : EXPRESSION BINARY_OPERATOR EXPRESSION"""
          print("operator call")
          p[0] = CallNode(p[1], p[2], [p[3]])

     def p_BINARY_OPERATOR(p):
          """BINARY_OPERATOR : PLUS
                             | MINUS"""
          print("binary operator")
          p[0] = p[1]


     def p_ASSIGNMENT(p):
          """ASSIGNMENT : IDENTIFIER EQUALS EXPRESSION"""
          print("assignment")
          p[0] = SetLocalNode(p[1], p[3])


     def p_LITERAL(p):
          """LITERAL : INTEGER
                     | STRING
                     | ORDERED_PAIR
                     | LIST"""
          print("literal")
          p[0] = LiteralNode(p[1])

     def p_ORDERED_PAIR(p):
          """ORDERED_PAIR : LPAREN INTEGER COMMA INTEGER RPAREN"""
          print("pair")
          p[0] = (int(p[2]), int(p[4]))

     def p_LIST(p):
          """LIST : LSQUARE RSQUARE
                  | LSQUARE ELEMENTS RSQUARE"""
          if len(p) == 3:
               print("empty list")
               p[0] = []
          else:
               print("list")
               p[0] = p[2]

     def p_ELEMENTS(p):
          """ELEMENTS : ELEMENT COMMA ELEMENTS
                      | ELEMENT"""
          print("elements")
          p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

     # Might extend this to allow arbitrary expressions within lists, but this would allow for 
     # nested lists, which are not used for anything in equibel-lang.
     def p_ELEMENT(p):
          """ELEMENT : INTEGER
                     | STRING
                     | ORDERED_PAIR"""
          print("element")
          p[0] = p[1]

     def p_OPT_WHITE(p):
          """OPT_WHITE : WHITESPACE
                       | empty"""
          print("optional whitespace")

     def p_empty(p):
          """empty :"""
          pass

     def p_error(p):
          if p is None:
               raise ValueError("unknown error!")
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
          print("usage: python3 Simplified_Parser.py file")
          sys.exit(1)

     filename = sys.argv[1]
     f = open(filename, 'r')

     tokens = parse_equibel(f.read())
     print(tokens)
