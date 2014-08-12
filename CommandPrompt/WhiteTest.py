import ply.lex
import ply.yacc
import sys
import pprint

def parse_equibel(text):
     tokens = ("IDENTIFIER", "INTEGER", "STRING", "LPAREN", "RPAREN", "COMMA",
               "LSQUARE", "RSQUARE", "WHITESPACE", "NEWLINE")

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



     #------------------------------------------------------------------------------------------------------
     #                                                PARSER
     #------------------------------------------------------------------------------------------------------
     def p_LINES(p):
          """LINES : LINE
                   | LINE NEWLINE LINES"""
          print("lines")
          p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

     # TODO: Think about semicolon terminators, in terms of:
     #         1) Signaling the end of a statement, to allow multiple statements
     #            on the same line, and
     #         2) Indicating that output should be suppressed when executing the
     #            line.
     def p_LINE(p):
          """LINE : OPT_WHITE EXPRESSION OPT_WHITE"""
          print("line")
          p[0] = p[2]

     def p_EXPRESSION(p):
          """EXPRESSION : LITERAL
                        | FUNCTION_CALL
                        | PAREN_EXPRESSION"""
          p[0] = p[1]

     def p_PAREN_EXPRESSION(p):
          """PAREN_EXPRESSION : LPAREN EXPRESSION RPAREN"""
          p[0] = p[2]


     # TODO: Think about parenthesized expressions as arguments, particularly
     #       parenthesized function calls, whose return values are to be used
     #       as arguments.
     def p_FUNCTION_CALL(p):
          """FUNCTION_CALL : IDENTIFIER
                           | IDENTIFIER WHITESPACE ARGS"""
          p[0] = ('id', p[1]) if len(p) == 2 else ('function', p[1], p[3])

     def p_ARGS(p):
          """ARGS : EXPRESSION
                  | ARGS WHITESPACE EXPRESSION"""
          p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

     
     def p_LITERAL(p):
          """LITERAL : INTEGER
                     | STRING
                     | ORDERED_PAIR
                     | LIST"""
          p[0] = p[1]

     def p_ORDERED_PAIR(p):
          """ORDERED_PAIR : LPAREN OPT_WHITE_NEWLINE INTEGER OPT_WHITE_NEWLINE COMMA \
                            OPT_WHITE_NEWLINE INTEGER OPT_WHITE_NEWLINE RPAREN"""
          print("pair")
          p[0] = (int(p[3]), int(p[7]))

     def p_LIST(p):
          """LIST : LSQUARE OPT_WHITE_NEWLINE RSQUARE
                  | LSQUARE OPT_WHITE_NEWLINE ELEMENTS OPT_WHITE_NEWLINE RSQUARE"""
          if len(p) == 4:
               print("empty list")
               p[0] = []
          else:
               print("list")
               p[0] = p[3]

     def p_ELEMENTS(p):
          """ELEMENTS : ELEMENT
                      | ELEMENTS OPT_WHITE_NEWLINE COMMA OPT_WHITE_NEWLINE ELEMENT"""
          print("elements")
          p[0] = [p[1]] if len(p) == 3 else [p[1]] + p[5]

     # Might extend this to allow arbitrary expressions within lists, but this would allow for
     # nested lists, which are not used for anything in equibel-lang.
     def p_ELEMENT(p):
          """ELEMENT : INTEGER
                     | STRING
                     | ORDERED_PAIR"""
          print("element")
          p[0] = p[1]

     def p_OPT_WHITE_NEWLINE(p):
          """OPT_WHITE_NEWLINE : WHITESPACE_NEWLINE
                               | empty"""
          print("optional whitespace/newlines")

     def p_WHITESPACE_NEWLINE(p):
          """WHITESPACE_NEWLINE : WHITESPACE
                                | NEWLINE
                                | WHITESPACE_NEWLINE WHITESPACE
                                | WHITESPACE_NEWLINE NEWLINE"""
          print("whitespace or newlines")

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

     """
     precedence = (("nonassoc", "FOURTH"), 
                   ("nonassoc", "THIRD"),
                   ("nonassoc", "SECOND"),
                   ("nonassoc", "FIRST"))
     """

     precedence = (("left", "IDENTIFIER"), ("right", "WHITESPACE"))
     #precedence = (("right", "WHITESPACE"), ("right", "IDENTIFIER"))

     lexer = ply.lex.lex()
     parser = ply.yacc.yacc()

     try:
          return parser.parse(text, lexer=lexer)
     except ValueError as err:
          print(err)
          return []

if __name__ == '__main__':
     if len(sys.argv) < 2:
          print("usage: python3 WhiteTest.py file")
          sys.exit(1)

     filename = sys.argv[1]
     f = open(filename, 'r')

     tokens = parse_equibel(f.read().strip())
     pprint.pprint(tokens)
