"""Formatter to create the Answer Set Programming (ASP) representation
of an arbitrary EquibelGraph instance. The ASP format is used when 
giving a graph to the gringo/clingo ASP tools.
"""
#    Copyright (C) 2014-2015 by
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    BSD license.

from equibel.simbool.proposition import Prop


__all__ = ['convert_to_asp', 'convert_formula_to_asp']


NODE_TEMPLATE    = "node({0}).\n"
RANGE_TEMPLATE   = "node({0}..{1}).\n"
EDGE_TEMPLATE    = "edge({0},{1}).\n"
ATOM_TEMPLATE    = "atom({0}).\n"
WEIGHT_TEMPLATE  = "weight({0},{1},{2}).\n"
FORMULA_TEMPLATE = "formula({0},{1}).\n"

AND_TEMPLATE   = "and({0},{1})"
OR_TEMPLATE    = "or({0},{1})"
NEG_TEMPLATE   = "neg({0})"


def convert_to_asp(G):
    asp_str = ""

    for node_id in G.nodes():
        asp_str += NODE_TEMPLATE.format(node_id)

    for atom in G.atoms():
        asp_str += ATOM_TEMPLATE.format(atom)

    # DONE: This is one way to handle undirected edges: when writing the ASP
    #       code, explicitly encode both directions if the G is undirected.
    for (from_node_id, to_node_id) in G.edges():
        asp_str += EDGE_TEMPLATE.format(from_node_id, to_node_id)
        if not G.is_directed():
            asp_str += EDGE_TEMPLATE.format(to_node_id, from_node_id)

    for node_id in G.nodes():
        weights = G.atom_weights(node_id)
        for atom in weights:
            weight = weights[atom]
            asp_str += WEIGHT_TEMPLATE.format(node_id, atom, weight)

    # This is separated from the above for loop for prettiness, to group
    # all the formulas together.
    for node_id in G.nodes():
        formulas = G.formulas(node_id)
        for formula in formulas:
            formatted_formula = convert_formula_to_asp(formula)
            asp_str += FORMULA_TEMPLATE.format(formatted_formula, node_id)

    return asp_str


def convert_formula_to_asp(formula):
    # Atomic propositions are the base case for the recursion.
    if formula.is_atomic():
        name = formula.get_name()
        if name is True:
            return 'true'
        elif name is False:
            return 'false'
        else:
            return name

    if formula.get_op() == '~':
        term = formula.get_terms()[0]
        formatted_term = convert_formula_to_asp(term)
        return NEG_TEMPLATE.format(formatted_term)

    terms = formula.get_terms()
    if len(terms) == 1:
        # This handles the case when we have a conjunction/disjunction with
        # only one operand, like *(p) or +(p).
        term = formula.get_terms()[0]
        return convert_formula_to_asp(term)
    elif len(terms) == 2:
        first_operand = convert_formula_to_asp(terms[0])
        second_operand = convert_formula_to_asp(terms[1])
    else:
        first_operand = convert_formula_to_asp(terms[0])
        # This creates a new formula with the same operator as the one being
        # parsed, creating a smaller disjunction/conjunction (that is, one
        # with fewer operands). This is done so that recursive calls to this
        # function will produce binary formulas.
        rest_of_formula = Prop(formula.get_op(), *terms[1:])
        second_operand = convert_formula_to_asp(rest_of_formula)

    if formula.get_op() == '&':
        return AND_TEMPLATE.format(first_operand, second_operand)
    elif formula.get_op() == '|':
        return OR_TEMPLATE.format(first_operand, second_operand)
