from nose.tools import with_setup, raises

import sympy
from sympy import symbols
from sympy.logic.boolalg import *
import equibel as eb


def create_three_node_chain():
    G = eb.EquibelGraph()
    G.add_edges_from([(0,1), (1,2)])
    return G


def test_graph_add_nodes():
    G = eb.EquibelGraph()
    G.add_node(0)
    G.add_nodes_from([1,2])
    assert(G.nodes() == [0,1,2])


def test_graph_add_edges():
    G = eb.EquibelGraph()
    G.add_edge(0,1)
    G.add_edges_from([(1,2), (2,3)])
    assert(G.nodes() == [0,1,2,3])
    assert(G.edges() == [(0,1), (1,2), (2,3)])


def test_graph_add_one_formula_from_str():
    p, q = symbols('p q')
    G = eb.EquibelGraph()
    G.add_node(0)
    G.add_formula(0, 'p & q')
    assert(G.formulas(0) == {p & q})
    assert(G.formulas() == {0: {p & q}})


def test_graph_add_one_formula_from_object():
    p, q, r = symbols('p q r')
    formula = p & q >> r
    G = eb.EquibelGraph()
    G.add_node(0)
    G.add_formula(0, formula)
    assert(G.formulas(0) == {p & q >> r})
    assert(G.formulas() == {0: {p & q >> r}})


def test_graph_add_formulas_to_multiple_nodes():
    p, q, r = symbols('p q r')
    G = create_three_node_chain()
    G.add_formula(0, 'p & q')
    assert(G.formulas() == {0: {p & q}, 1: set([]), 2: set([])})
    G.add_formula(1, 'p | ~r')
    assert(G.formulas() == {0: {p & q}, 1: {p | ~r}, 2: set([])})


def test_graph_add_multiple_formulas_to_one_node():
    p, q, r = symbols('p q r')
    G = eb.EquibelGraph()
    G.add_node(0)
    G.add_formula(0, 'p & q')
    G.add_formula(0, 'p | ~r')
    assert(G.formulas(0) == {p & q, p | ~r})
    assert(G.formula_conj(0) == (p & q) & (p | ~r))


def test_get_formulas_for_node_with_no_formulas():
    G = eb.EquibelGraph()
    G.add_node(0)
    assert(G.formulas() == {0: set()})
    print(G.formulas(0))
    assert(G.formulas(0) == set())


@raises(eb.EquibelGraphException)
def test_get_formulas_for_nonexistent_node_exception():
    G = eb.EquibelGraph()
    G.add_node(0)
    G.formulas(1)

@raises(eb.EquibelGraphException)
def test_add_formula_to_nonexistent_node_exception():
    G = eb.EquibelGraph()
    G.add_node(0)
    G.add_formula(1, 'p')


@raises(Exception)
def test_add_empty_formula_str():
    G = eb.EquibelGraph()
    G.add_node(0)
    G.add_formula(0, '')


@raises(Exception)
def test_add_incorrect_formula_str():
    G = eb.EquibelGraph()
    G.add_node(0)
    G.add_formula(0, ')')


def test_atoms_one_node():
    p, q, r = symbols('p q r')
    G = eb.EquibelGraph()
    G.add_node(0)
    G.add_formula(0, 'p & q -> r')
    assert(G.atoms(0) == { p, q, r })
    assert(G.atoms() == { p, q, r })


def test_atoms_multiple_nodes():
    p, q, r = symbols('p q r')
    G = create_three_node_chain()
    G.add_formula(1, 'p & q')
    G.add_formula(2, '~r')
    assert(G.atoms(0) == set())
    assert(G.atoms(1) == {p, q})
    assert(G.atoms(2) == {r})
    assert(G.atoms() == {p, q, r})


@raises(eb.EquibelGraphException)
def test_get_atoms_for_nonexistent_node():
    G = eb.EquibelGraph()
    G.add_node(0)
    G.atoms(1)


def test_clear_formulas_from_one_node():
    p, q, r = symbols('p q r')
    G = eb.EquibelGraph()
    G.add_node(0)
    G.add_formula(0, 'p & q')
    G.add_formula(0, '~r')
    assert(G.formulas(0) == { p & q, ~r })
    G.clear_formulas_from(0)
    assert(G.formulas(0) == set())


def test_clear_formulas_all_nodes():
    p, q, r = symbols('p q r')
    G = create_three_node_chain()
    G.add_formula(0, 'p & q')
    G.add_formula(0, '~r')
    G.add_formula(1, '~q -> r')
    G.clear_formulas()
    assert(G.formulas() == {0: set(), 1: set(), 2: set()})


def test_equality():
    A = create_three_node_chain()
    B = create_three_node_chain()
    assert(A == B)
    A.add_formula(0, 'p & ~q')
    B.add_formula(0, 'p & ~q')
    assert(A == B)


def test_nonequality():
    A = create_three_node_chain()
    B = create_three_node_chain()
    A.add_formula(0, 'r')
    assert(A != B)

