from __future__ import absolute_import
from __future__ import print_function

import sys
import equibel.parsers.FormulaParserASP as FormulaParserASP

from equibel.simbool.proposition import *
from equibel.simbool.simplify import *

# TODO: See if this can be made cleaner.
def combine_formulas(models):
    disjunctions = dict()

    for model in models:
        conjunctions = dict()
        new_formula_predicates = model['new_formula']
        for new_formula_pred in new_formula_predicates:
            node_num, formula = extract_formula(new_formula_pred)
            if node_num in conjunctions:
                conjunctions[node_num] = simplify(conjunctions[node_num] & formula)
            else:
                conjunctions[node_num] = formula
        
        for node_num in conjunctions:
            conjunction = conjunctions[node_num]
            if node_num in disjunctions:
                disjunctions[node_num] = simplify(disjunctions[node_num] | conjunction)
            else:
                disjunctions[node_num] = conjunction
            
    # TODO: Some simplification.
    for node_num in disjunctions:
        disjunctions[node_num] = simplify(disjunctions[node_num])

    return disjunctions

# TODO: Add error checking?
def extract_formula(formula_term):
    arguments   = formula_term.args()
    node_id     = arguments[0]
    formula_str = str(arguments[1])
    formula    = FormulaParserASP.parse_asp_formula(formula_str)
    return (node_id, formula)
