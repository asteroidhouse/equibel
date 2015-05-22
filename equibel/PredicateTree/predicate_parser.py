from __future__ import absolute_import

import sys

from ply import lex
from ply import yacc

from equibel.PredicateTree.predicate import Predicate

tokens = ("IDENTIFIER", "INTEGER", "LPAREN", "RPAREN", "COMMA")

t_IDENTIFIER = r'[_a-zA-Z][_a-zA-Z0-9]*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA  = r','

t_ignore = " \t\n"


def t_INTEGER(t):
    r"0|[1-9][0-9]*"
    t.value = int(t.value)
    return t


def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    return t


def t_error(t):
    line = t.value.lstrip()
    i = line.find("\n")
    line = line if i == -1 else line[:i]
    raise ValueError("Syntax error, line {0}: {1}".format(t.lineno + 1, line))


def p_PREDICATE(p):
    """PREDICATE : IDENTIFIER LPAREN ARGS RPAREN"""
    p[0] = Predicate(p[1], p[3])


def p_ARGS(p):
    """ARGS : ARG
           | ARG COMMA ARGS"""
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]


def p_ARG(p):
    """ARG : INTEGER
          | IDENTIFIER
          | PREDICATE"""
    p[0] = p[1]


def p_error(p):
    if p is None:
        raise ValueError("Unknown error")
    raise ValueError("Syntax error, line {0}: {1}".format(p.lineno + 1, p.type))

lexer = lex.lex()
parser = yacc.yacc()


def parse_predicate(text):
    try:
        return parser.parse(text, lexer=lexer)
    except ValueError as err:
        print(err)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python3 PredicateParser.py filename')
        sys.exit(1)

    filename = sys.argv[1]
    f = open(filename, 'r')

    try:
        for line in f.readlines():
            predicate = parse_predicate(line)
            print(predicate)
    except Exception as err:
        print(err)
