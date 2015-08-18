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

__all__ = ["parse_formula"]

# --------------------------------------------------------------------
#                             LEXER
# --------------------------------------------------------------------

tokens = ("NEG", "AND", "OR", "LPAREN", "RPAREN", "IDENTIFIER", "WHITESPACE")

t_NEG = r'\-'
t_AND = r'\*'
t_OR = r'\+'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_IDENTIFIER = r'[_a-zA-Z][_a-zA-Z0-9]*'

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

# --------------------------------------------------------------------
#                             PARSER
# --------------------------------------------------------------------

def p_FORMULA_LINE(p):
    """FORMULA_LINE : OPT_WHITESPACE FORMULA OPT_WHITESPACE"""
    p[0] = p[2]


def p_FORMULA(p):
    """FORMULA : LPAREN OPT_WHITESPACE FORM OPT_WHITESPACE RPAREN"""
    p[0] = p[3]


def p_FORM(p):
    """FORM : SIMPLE_FORM
            | COMPOUND_FORM"""
    p[0] = p[1]


def p_SIMPLE_FORM(p):
    """SIMPLE_FORM : ATOM
                   | NEG OPT_WHITESPACE ATOM
                   | LPAREN OPT_WHITESPACE FORM OPT_WHITESPACE RPAREN
                   | NEG OPT_WHITESPACE LPAREN OPT_WHITESPACE FORM OPT_WHITESPACE RPAREN"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = Prop('~', p[3])
    elif len(p) == 6:
        p[0] = p[3]
    elif len(p) == 8:
        p[0] = Prop('~', p[5])


def p_COMPOUND_FORM(p):
    """COMPOUND_FORM : OP OPT_WHITESPACE LPAREN OPT_WHITESPACE FORM_LIST OPT_WHITESPACE RPAREN"""
    p[0] = Prop(p[1], *p[5])


def p_FORM_LIST(p):
    """FORM_LIST : FORM OPT_WHITESPACE
                 | FORM WHITESPACE FORM_LIST"""
    p[0] = [p[1]] if len(p) == 3 else [p[1]] + p[3]


def p_ATOM(p):
    """ATOM : IDENTIFIER"""
    p[0] = Prop(p[1])


def p_OP(p):
    """OP : AND_OP
          | OR_OP"""
    p[0] = p[1]


# This rule was introduced to translate between the notation used 
# to represent a conjunction in the input language and the notation
# used by the simbool module.
def p_AND_OP(p):
    """AND_OP : AND"""
    p[0] = '&'


# This rule was introduced to translate between the notation used 
# to represent a disjunction in the input language and the notation
# used by the simbool module.
def p_OR_OP(p):
    """OR_OP : OR"""
    p[0] = '|'


def p_OPT_WHITESPACE(p):
    """OPT_WHITESPACE : WHITESPACE
                      | empty"""
    pass


def p_empty(p):
    """empty :"""
    pass


def p_error(p):
    if p is None:
        raise ValueError("Unknown error")
    raise ValueError("Syntax error, line {0}: {1}".format(p.lineno + 1, p.type))


lexer = ply.lex.lex(optimize=1, debug=0)
parser = ply.yacc.yacc(debug=0, write_tables=0)


def parse_formula(text):
    try:
        return parser.parse(text, lexer=lexer)
    except ValueError as err:
        print(err)
        return []


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python FormulaParserSim.py file')
        sys.exit(1)

    filename = sys.argv[1]
    f = open(filename, 'r')
    
    formula = parse_formula(f.read().strip())
    
    print(repr(formula))
    print("Simplified = \n{0}".format(repr(simplify(formula))))
