"""Parser for propositional formulas represented using infix notation.

The symbols used for the logical connectives are as follows:

       +------------+--------+
       | Connective | Symbol |
       +============+========+
       |    conj.   |  ``&`` |
       +------------+--------+
       |    disj.   |  ``|`` |
       +------------+--------+
       |   implies  | ``->`` |
       +------------+--------+
       |    equiv   |  ``=`` |
       +------------+--------+
       |     neg    |  ``~`` |
       +------------+--------+

The precedence and right/left associativity rules of the conectives are as follows:

1. Negation (``~``) has the highest precendence, and is right-associative.
2. Conjunction (``&``) has the next highest precedence, and is left-associative.
3. Disjunction (``|``) is next, is left-associative.
4. Implication (``->``) comes next, and is right-associative.
5. Finally, equivalence (``=``) is last, and is right-associative.

Using these precedence rules, the following formulas are equivalent::

* ``p & q | r   ==   (p & q) | r``
* ``p & q -> r   ==   (p & q) -> r``
* ``p | ~r = q   ==   (p | (~r)) = q``
* ``~p | ~q & r   ==   ((~p) | (~q)) & r``

The only importable function from this file is parse_formula, 
which takes a string such as ``p & q | ~r`` and creates a Sympy logical
formula object representing that formula.
"""
#    Copyright (C) 2016
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.

from __future__ import absolute_import

import sys
import logging

import ply
import ply.lex as lex
import ply.yacc as yacc

from sympy import symbols, simplify
from sympy.logic.boolalg import *


__all__ = ["parse_formula"]


log = logging.getLogger('ply')


##################################################################
######                       LEXER                          ######
##################################################################

keywords = {"True": "TRUE", "False": "FALSE"}

tokens = (["NEG", "AND", "OR", "IMPLIES", "EQUIV", "LPAREN", "RPAREN", 
           "INTEGER", "IDENTIFIER"] + list(keywords.values()))

def t_IDENTIFIER(t):
    r"[_a-zA-Z][_a-zA-Z0-9]*"
    t.type = keywords.get(t.value, "IDENTIFIER")
    return t

t_NEG = r"~"
t_AND = r"&"
t_OR = r"\|"
t_IMPLIES = r"->"
t_EQUIV = r"="
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_INTEGER = r"[0-9]+"

t_ignore = " \t\n"


def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    return t


def t_error(t):
    line = t.value.lstrip()
    i = line.find("\n")
    line = line if i == -1 else line[:i]
    raise ValueError("Syntax error, line {0}: {1}".format(t.lineno + 1, line))


##################################################################
######                     PARSER                           ######
##################################################################

def p_FORMULA(p):
    """FORMULA : ATOM
               | BOOLEAN
               | COMPOUND
               | LPAREN FORMULA RPAREN"""
    p[0] = p[1] if len(p) == 2 else p[2]


def p_ATOM(p):
    """ATOM : IDENTIFIER
            | INTEGER"""
    p[0] = symbols(p[1])


def p_BOOLEAN_TRUE(p):
    """BOOLEAN : TRUE"""
    # true is a singleton object from sympy, of type sympy.logic.boolalg.BooleanTrue
    p[0] = true


def p_BOOLEAN_FALSE(p):
    """BOOLEAN : FALSE"""
    # false is a singleton object from sympy, of type sympy.logic.boolalg.BooleanFalse
    p[0] = false

def p_COMPOUND(p):
    """COMPOUND : NEGATION
                | CONJUNCTION
                | DISJUNCTION
                | IMPLICATION
                | EQUIVALENCE"""
    p[0] = p[1]


def p_NEGATION(p):
    """NEGATION : NEG FORMULA"""
    p[0] = ~ p[2]


def p_CONJUNCTION(p):
    """CONJUNCTION : FORMULA AND FORMULA"""
    p[0] = p[1] & p[3]


def p_DISJUNCTION(p):
    """DISJUNCTION : FORMULA OR FORMULA"""
    p[0] = p[1] | p[3]


def p_IMPLICATION(p):
    """IMPLICATION : FORMULA IMPLIES FORMULA"""
    # Material implication using sympy operator ">>"
    p[0] = p[1] >> p[3]


def p_EQUIVALENCE(p):
    """EQUIVALENCE : FORMULA EQUIV FORMULA"""
    #p[0] = Equivalent(p[1], p[3])
    p[0] = (p[1] >> p[3]) & (p[3] >> p[1])


def p_error(p):
    if p is None:
        raise ValueError("Unknown error")
    raise ValueError("Syntax error, line {0}: {1}".format(p.lineno + 1, p.type))


precedence = (("right", "EQUIV"),
              ("right", "IMPLIES"),
              ("left", "OR"),
              ("left", "AND"),
              ("right", "NEG"))

#lexer = ply.lex.lex(optimize=1, debug=0)
#parser = ply.yacc.yacc(debug=0, write_tables=0)
lexer = lex.lex()
parser = yacc.yacc(errorlog=log)


def parse_formula(text):
    try:
        return parser.parse(text, lexer=lexer)
    except ValueError as err:
        raise ValueError(err)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python formulaparser.py FORMULA_STRING')
        sys.exit(1)

    formula_str = sys.argv[1]
    
    formula = parse_infix_formula(formula_str)
    
    print(repr(formula))
    print("Simplified = \n{0}".format(repr(simplify(formula))))
