import sys
from equibel.simbool.proposition import *

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

# TODO: Think about how to handle directed vs undirected edges, 
#       both here and in the Graph class.
def convert_to_bcf(graph):
     bcf_str = ""
     
     if graph.directed:
          bcf_str += TYPE_TEMPLATE.format("directed")
     else:
          bcf_str += TYPE_TEMPLATE.format("undirected")

     for node_num in graph.nodes:
          bcf_str += NODE_TEMPLATE.format(node_num)
     
     for atom in graph.atoms:
          bcf_str += ATOM_TEMPLATE.format(atom)
     
     for (start_node_num, end_node_num) in graph.edges:
          bcf_str += EDGE_TEMPLATE.format(start_node_num, end_node_num)
     
     for node in graph.nodes.values():
          for atom in node.weights:
               # TODO: Create a public interface to access weights?
               weight = node.weights[atom]
               bcf_str += WEIGHT_TEMPLATE.format(node.num, atom, weight)
     
     # This is separated from the above for loop for prettiness, to group 
     # all the formulas together.
     for node in graph.nodes.values():
          for formula in node.formulas:
               formatted_formula = "({0})".format(convert_formula_to_bcf(formula))
               bcf_str += FORMULA_TEMPLATE.format(node.num, formatted_formula)
     
     return bcf_str


def convert_formula_to_bcf(formula):
     # Atomic propositions are the base case for the recursion.
     if formula.is_atomic():
          return formula.name

     terms = formula.get_terms()
     bcf_op = bcf_op_dict[formula.get_op()]
     return "{0}({1})".format(bcf_op, " ".join([convert_formula_to_bcf(term) for term in terms]))
