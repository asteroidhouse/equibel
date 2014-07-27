import ply.lex
import ply.yacc
import sys
import pprint
from nodes import *

debug_mode = False

def parse_equibel(text):
     tokens = ("IDENTIFIER", "INTEGER", "STRING", "LPAREN", "RPAREN", "COMMA", "EQUALS",
               "PLUS", "MINUS", "PLUS_EQUALS", "MINUS_EQUALS", "LSQUARE", "RSQUARE", 
               "DOT", "NEWLINE")

     t_IDENTIFIER = r'[a-zA-Z][_a-zA-Z0-9]*'

     t_LPAREN  = r'\('
     t_RPAREN  = r'\)'
     t_LSQUARE = r'\['
     t_RSQUARE = r'\]'

     t_COMMA   = r','
     
     t_EQUALS  = r'='
     t_PLUS    = r'\+'
     t_MINUS   = r'\-'
     t_PLUS_EQUALS  = r'\+='
     t_MINUS_EQUALS = r'\-='

     t_DOT = r'\.'

     # Ignore spaces and tabs.
     t_ignore = " \t"

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
          if debug_mode:
               print("lines")
          p[0] = RootNode([p[1]]) if len(p) == 3 else p[3].append(p[1])

     # TODO: Think about semicolon terminators, in terms of:
     #         1) Signaling the end of a statement, to allow multiple statements
     #            on the same line, and
     #         2) Indicating that output should be suppressed when executing the
     #            line.
     def p_LINE(p):
          """LINE : EXPRESSION"""
          if debug_mode:
               print("line")
          p[0] = p[1]

     def p_EXPRESSION(p):
          """EXPRESSION : LITERAL
                        | ASSIGNMENT
                        | MOD_ASSIGNMENT
                        | FUNCTION_CALL"""
          if debug_mode:
               print("expression")
          p[0] = p[1]

     def p_parenthesized_expression(p):
          """EXPRESSION : LPAREN EXPRESSION RPAREN"""
          if debug_mode:
               print("parenthesized expression")
          p[0] = p[2]

     # DONE: Also, think about adding support for qualifying function names 
     #       with receiver names, to allow 'methods' to be called on specific 
     #       objects. This would allow:
     #              g2.add_nodes [1,2,3,4]
     #       instead of requiring a context switch:
     #              use g2
     #              add_nodes [1,2,3,4]
     def p_FUNCTION_CALL(p):
          """FUNCTION_CALL : EXPRESSION DOT IDENTIFIER LPAREN COMMA_ARGS RPAREN
                           | IDENTIFIER LPAREN COMMA_ARGS RPAREN
                           | IDENTIFIER"""
          if debug_mode:
               print("function call")
          if len(p) == 2:
               p[0] = CallNode(None, p[1])
          elif len(p) == 5:
               p[0] = CallNode(None, p[1], p[3])
          else:
               p[0] = CallNode(p[1], p[3], p[5])
     
     def p_COMMA_ARGS(p):
          """COMMA_ARGS : EXPRESSION COMMA COMMA_ARGS
                        | EXPRESSION"""
          if debug_mode:
               print("comma args")
          p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]
     
     # Calling x + 2 is treated as x.+(2), that is, it invokes the + function of x, with 2 
     # as an argument.
     def p_operator_call(p):
          """FUNCTION_CALL : EXPRESSION BINARY_OPERATOR EXPRESSION"""
          if debug_mode:
               print("operator call")
          p[0] = CallNode(p[1], p[2], [p[3]])

     def p_BINARY_OPERATOR(p):
          """BINARY_OPERATOR : PLUS
                             | MINUS"""
          if debug_mode:
               print("binary operator")
          p[0] = p[1]


     def p_ASSIGNMENT(p):
          """ASSIGNMENT : IDENTIFIER EQUALS EXPRESSION"""
          if debug_mode:
               print("assignment")
          p[0] = SetLocalNode(p[1], p[3])

     def p_MOD_ASSIGNMENT(p):
          """MOD_ASSIGNMENT : IDENTIFIER ASSIGN_OPERATOR EXPRESSION"""
          p[0] = ModAssignNode(p[1], p[2], p[3])

     def p_ASSIGN_OPERATOR(p):
          """ASSIGN_OPERATOR : PLUS_EQUALS
                             | MINUS_EQUALS"""
          p[0] = p[1]

     def p_LITERAL(p):
          """LITERAL : INTEGER
                     | STRING
                     | ORDERED_PAIR
                     | LIST"""
          if debug_mode:
               print("literal")
          p[0] = LiteralNode(p[1])

     def p_ORDERED_PAIR(p):
          """ORDERED_PAIR : LPAREN INTEGER COMMA INTEGER RPAREN"""
          if debug_mode:
               print("ordered pair")
          p[0] = (int(p[2]), int(p[4]))

     def p_LIST(p):
          """LIST : LSQUARE RSQUARE
                  | LSQUARE ELEMENTS RSQUARE"""
          if len(p) == 3:
               if debug_mode:
                    print("empty list")
               p[0] = []
          else:
               if debug_mode:
                    print("list")
               p[0] = p[2]

     def p_ELEMENTS(p):
          """ELEMENTS : ELEMENT COMMA ELEMENTS
                      | ELEMENT"""
          if debug_mode:
               print("elements")
          p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

     # Might extend this to allow arbitrary expressions within lists, but this would allow for 
     # nested lists, which are not used for anything in equibel-lang.
     def p_ELEMENT(p):
          """ELEMENT : INTEGER
                     | STRING
                     | ORDERED_PAIR"""
          if debug_mode:
               print("element")
          p[0] = p[1]

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
