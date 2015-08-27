"""Formatter to create the Belief Change Format (BCF) representation
of an arbitrary EquibelGraph instance.
"""
#    Copyright (C) 2014-2015 by
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.

__all__ = ['convert_to_bcf', 'convert_formula_to_bcf']


TYPE_TEMPLATE    = "t {0}\n"
NODE_TEMPLATE    = "n {0}\n"
RANGE_TEMPLATE   = "n {0}..{1}\n"
EDGE_TEMPLATE    = "e {0} {1}\n"
ATOM_TEMPLATE    = "a {0}\n"
WEIGHT_TEMPLATE  = "w {0} {1} {2}\n"
FORMULA_TEMPLATE = "f {0} {1}\n"

ENTAILMENT_CONSTRAINT_TEMPLATE  = "m {0}\n"
CONSISTENCY_CONSTRAINT_TEMPLATE = "s {0}\n"

# This dictionary maps from the operators used in the proposition
# class to the operators used in BCF.
bcf_op_dict = {
    '&': '*',
    '|': '+',
    '~': '-'
}


def convert_to_bcf(G):
    bcf_str = ""

    if G.is_directed():
        bcf_str += TYPE_TEMPLATE.format("directed")
    else:
        bcf_str += TYPE_TEMPLATE.format("undirected")

    for node_id in G.nodes():
        bcf_str += NODE_TEMPLATE.format(node_id)

    for atom in G.atoms():
        bcf_str += ATOM_TEMPLATE.format(atom)

    for (from_node_id, to_node_id) in G.edges():
        bcf_str += EDGE_TEMPLATE.format(from_node_id, to_node_id)
        if not G.is_directed():
            bcf_str += EDGE_TEMPLATE.format(to_node_id, from_node_id)

    for node_id in G.nodes():
        for atom in G.atom_weights(node_id):
            weight = G.weight(node_id, atom)
            bcf_str += WEIGHT_TEMPLATE.format(node_id, atom, weight)

    # This is separated from the above for loop for prettiness, to group
    # all the formulas together.
    for node_id in G.nodes():
        for formula in G.formulas(node_id):
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
