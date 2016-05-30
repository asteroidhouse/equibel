"""Formatter to create the Belief Change Format (BCF) representation
of an arbitrary EquibelGraph instance.
"""
#    Copyright (C) 2016 by
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.


__all__ = ['convert_to_bcf', 'convert_formula_to_bcf']


NODE_TEMPLATE    = "n {0}\n"
RANGE_TEMPLATE   = "n {0}..{1}\n"
EDGE_TEMPLATE    = "e {0} {1}\n"
ATOM_TEMPLATE    = "a {0}\n"
FORMULA_TEMPLATE = "f {0} {1}\n"

# This dictionary maps from the operators used in the proposition
# class to the operators used in BCF.
bcf_op_dict = {
    '&': '*',
    '|': '+',
    '~': '-'
}


def convert_to_bcf(G):
    bcf_str = ""

    for node_id in G.nodes():
        bcf_str += NODE_TEMPLATE.format(node_id)

    for atom in G.atoms():
        bcf_str += ATOM_TEMPLATE.format(atom)

    for (from_node, to_node) in G.edges():
        bcf_str += EDGE_TEMPLATE.format(from_node, to_node)
        bcf_str += EDGE_TEMPLATE.format(to_node, from_node)

    # This is separated from the above for loop for prettiness, to group
    # all the formulas together.
    for node in G.nodes():
        formula = G.formula_conj(node):
        formatted_formula = "({0})".format(convert_formula_to_bcf(formula))
        bcf_str += FORMULA_TEMPLATE.format(node_id, formatted_formula)

    return bcf_str


def convert_formula_to_bcf(formula):
    if formula.is_atomic():
        return formula.get_name()

    terms = formula.get_terms()
    bcf_op = bcf_op_dict[formula.get_op()]
    return "{0}({1})".format(bcf_op,
                             " ".join([convert_formula_to_bcf(term) for term in terms]))
