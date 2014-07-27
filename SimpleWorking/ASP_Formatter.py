import sys
sys.path.append('simbool')
from simbool.proposition import *

NODE_TEMPLATE    = "node({0}).\n"
RANGE_TEMPLATE   = "node({0}..{1}).\n"
EDGE_TEMPLATE    = "edge({0},{1}).\n"
ATOM_TEMPLATE    = "atom({0}).\n"
WEIGHT_TEMPLATE  = "weight({0},{1},{2}).\n"
FORMULA_TEMPLATE = "formula({0},{1}).\n"

AND_TEMPLATE   = "and({0},{1})"
OR_TEMPLATE    = "or({0},{1})"
NEG_TEMPLATE   = "neg({0})"

# TODO: Think about how to handle directed vs undirected edges, 
#       both here and in the Graph class.
def convert_to_asp(graph):
     asp_str = ""
     
     for node_num in graph.nodes:
          asp_str += NODE_TEMPLATE.format(node_num)
     
     # DONE: Keep track of atoms in the common alphabet at the Graph level.
     for atom in graph.atoms:
          asp_str += ATOM_TEMPLATE.format(atom)
     
     for (start_node_num, end_node_num) in graph.edges:
          asp_str += EDGE_TEMPLATE.format(start_node_num, end_node_num)
     
     for node in graph.nodes.values():
          for atom in node.weights:
               # TODO: Create a public interface to access weights?
               weight = node.weights[atom]
               asp_str += WEIGHT_TEMPLATE.format(node.num, atom, weight)
     
     # This is separated from the above for loop for prettiness, to group 
     # all the formulas together.
     for node in graph.nodes.values():
          for formula in node.formulas:
               formatted_formula = convert_formula_to_asp(formula)
               asp_str += FORMULA_TEMPLATE.format(node.num, formatted_formula)
               #asp_str += FORMULA_TEMPLATE.format(node.num, repr(formula))
     
     return asp_str


def convert_formula_to_asp(formula):
     # Atomic propositions are the base case for the recursion.
     if formula.is_atomic():
          return formula.name

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
          first_operand  = convert_formula_to_asp(terms[0])
          second_operand = convert_formula_to_asp(terms[1])
     else:
          first_operand   = convert_formula_to_asp(terms[0])
          # This creates a new formula with the same operator as the one being 
          # parsed, creating a smaller disjunction/conjunction (that is, one 
          # with fewer operands). This is done so that recursive calls to this 
          # function will produce binary formulas.
          rest_of_formula = Prop(formula.get_op(), *terms[1:])
          second_operand  = convert_formula_to_asp(rest_of_formula)

     if formula.get_op() == '&':
          return AND_TEMPLATE.format(first_operand, second_operand)
     elif formula.get_op() == '|':
          return OR_TEMPLATE.format(first_operand, second_operand)

