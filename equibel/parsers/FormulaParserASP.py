"""
"""
#    Copyright (C) 2014-2015 by
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.

from __future__ import absolute_import

import sys

import ply.lex
import ply.yacc

from equibel.simbool.proposition import *
from equibel.simbool.simplify import *

__all__ = ["parse_asp_formula"]

# --------------------------------------------------------------------
#                             LEXER
# --------------------------------------------------------------------

keywords = {"neg": "NEG", "and": "AND", "or": "OR", 
            "implies": "IMPLIES", "iff": "IFF"}

tokens = (["INTEGER", "IDENTIFIER", "LPAREN", "RPAREN", 
           "COMMA"] + list(keywords.values()))

t_INTEGER = r'[0-9]+'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA  = r','

t_ignore = " \t\n"

def t_IDENTIFIER(t):
    r"[_a-zA-Z][_a-zA-Z0-9]*"
    t.type = keywords.get(t.value, "IDENTIFIER")
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


# --------------------------------------------------------------------
#                             PARSER
# --------------------------------------------------------------------

def p_FORMULA(p):
    """FORMULA : ATOM
               | COMPOUND"""
    p[0] = p[1]


def p_ATOM(p):
    """ATOM : IDENTIFIER
            | INTEGER"""
    p[0] = Prop(p[1])


def p_COMPOUND(p):
    """COMPOUND : NEGATION
                | CONJUNCTION
                | DISJUNCTION
                | IMPLICATION
                | EQUIVALENCE"""
    p[0] = p[1]


def p_NEGATION(p):
    """NEGATION : NEG LPAREN FORMULA RPAREN"""
    p[0] = ~ p[3]


def p_CONJUNCTION(p):
    """CONJUNCTION : AND LPAREN FORMULA COMMA FORMULA RPAREN"""
    p[0] = p[3] & p[5]


def p_DISJUNCTION(p):
    """DISJUNCTION : OR LPAREN FORMULA COMMA FORMULA RPAREN"""
    p[0] = p[3] | p[5]


def p_IMPLICATION(p):
    """IMPLICATION : IMPLIES LPAREN FORMULA COMMA FORMULA RPAREN"""
    # Material implication using operator ">"
    p[0] = p[3] > p[5]


def p_EQUIVALENCE(p):
    """EQUIVALENCE : IFF LPAREN FORMULA COMMA FORMULA RPAREN"""
    p[0] = (p[3] > p[5]) & (p[5] > p[3])


def p_error(p):
    if p is None:
        raise ValueError("Unknown error")
    raise ValueError("Syntax error, line {0}: {1}".format(p.lineno + 1, p.type))


lexer = ply.lex.lex(optimize=1, debug=0)
parser = ply.yacc.yacc(debug=0, write_tables=0)

def parse_asp_formula(text):
    try:
        return parser.parse(text, lexer=lexer)
    except ValueError as err:
        print(err)
        return []


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python FormulaParserASP.py file')
        sys.exit(1)

    filename = sys.argv[1]
    f = open(filename, 'r')
    
    contents = f.read().strip()
    lines = contents.split("\n")
    for line in lines:
        formula = parse_asp_formula(line)
        print("Formula = {0}".format(repr(formula)))
        print("Simplified = {0}".format(repr(simplify(formula))))
