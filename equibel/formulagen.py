"""This file contains functions to generate random propositional formulas.
"""
#    Copyright (C) 2016
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.

import random

import sympy
from sympy.logic.boolalg import *

functions = [
    And,
    Or,
    Implies,
    Equivalent,
    Not,
]

def random_formula(num_atoms=3, num_connectives=3):
    atoms = sympy.symbols("x1:{}".format(num_atoms+1))
    formula = random.choice(atoms)

    for i in range(num_connectives):
        f = random.choice(functions)
        if f == Not:
            formula = f(formula)
        else:
            formula = f(formula, random.choice(atoms))

    return formula


def simplify(formula):
    return simplify_logic(formula)


def random_formula_simplified(num_atoms=3, num_connectives=3):
    return simplify_logic(random_formula(num_atoms, num_connectives))
