from nose.tools import *
from equibel.node import Node
from equibel.simbool.proposition import Prop

def test_node_init():
     node = Node(1)
     assert_equals(node.num, 1)
     assert_equals(node.weights, dict())
     assert_equals(node.formulas, set())

def test_add_atom_default_weight():
     node = Node(1)
     node.add_atom('q')
     assert_equals(node.weights['q'], 1)

def test_add_atom_with_weight():
     node = Node(1)
     node.add_atom('q', 3)
     assert_equals(node.weights['q'], 3)

def test_add_atoms():
     node = Node(1)
     node.add_atoms(['p', 'q', 'r'])
     assert_equals(node.get_atoms(), ['p', 'q', 'r'])

def test_get_atoms():
     node = Node(1)
     node.add_atom('q')
     node.add_atom('p')
     assert_equals(node.get_atoms(), ['p', 'q'])

def test_add_weight_existing_atom():
     node = Node(1)
     node.add_atom('q')
     assert_equals(node.weights['q'], 1)
     node.add_weight('q', 3)
     assert_equals(node.weights['q'], 3)

# Should an exception be thrown instead?
def test_add_weight_non_extant_atom():
     node = Node(1)
     node.add_weight('q', 3)
     assert_equals(node.weights['q'], 3)

def test_remove_existing_atom():
     node = Node(1)
     node.add_atom('q')
     node.remove_atom('q')
     assert_equals(node.weights, dict())

def test_remove_non_extant_atom():
     node = Node(1)
     node.remove_atom('q')
     assert_equals(node.weights, dict())

def test_remove_existing_weight():
     node = Node(1)
     node.add_weight('q', 3)
     node.remove_weight('q')
     assert_equals(node.weights['q'], 1)

def test_remove_non_extant_weight():
     node = Node(1)
     node.remove_weight('q')
     assert_equals(node.weights, dict())


# The following tests use Prop from simbool.proposition
# -------------------------------------------------------
def test_add_formula():
     node = Node(1)
     p,q = [Prop(letter) for letter in 'pq']
     formula = p & q
     node.add_formula(formula)
     assert formula in node.formulas
     assert_equals(node.get_atoms(), ['p', 'q'])

def test_remove_existing_formula_same_object():
     node = Node(1)
     p,q = [Prop(letter) for letter in 'pq']
     formula = p & q
     node.add_formula(formula)
     node.remove_formula(formula)
     assert_equals(node.formulas, set())

def test_remove_existing_formula_equal_object():
     node = Node(1)
     p,q = [Prop(letter) for letter in 'pq']
     formula = p & q
     node.add_formula(formula)
     node.remove_formula(Prop('q') & Prop('p'))
     assert_equals(node.formulas, set())

def test_remove_non_extant_formula():
     node = Node(1)
     node.remove_formula(Prop('q') & Prop('p'))
     assert_equals(node.formulas, set())


# Mixed tests
# -------------------------------------------------------

def test_auto_adding_atoms():
     node = Node(1)
     node.add_weight('p', 4)
     node.add_formula(Prop('p') | Prop('r') | Prop('q'))
     assert_equals(node.get_atoms(), ['p', 'q', 'r'])
     assert_equals(node.weights['p'], 4)
     assert_equals(node.weights['q'], 1)
     assert_equals(node.weights['r'], 1)
