from sympy.logic.boolalg import *

import equibel as eb


def test_global_completion_cardinality():
    G = eb.star_graph(3)
    G.add_formula(1, 'p')
    G.add_formula(2, 'p')
    G.add_formula(3, '~p')
    R_semantic = eb.global_completion(G, method=eb.SEMANTIC, opt_type=eb.CARDINALITY, simplify=True)
    assert(R_semantic.formula_conj(0) == eb.parse_formula('p'))
    
    R_syntactic = eb.global_completion(G, method=eb.SYNTACTIC, opt_type=eb.CARDINALITY, simplify=True)
    assert(R_syntactic == R_semantic)


def test_global_completion_two_nodes():
    G = eb.path_graph(2)
    G.add_formula(0, 'p')
    atoms = G.atoms()
    R_semantic = eb.global_completion(G, method=eb.SEMANTIC, simplify=True)
    print(R_semantic.formulas())
    assert(R_semantic.formulas() == {0: atoms, 1: atoms})

    R_syntactic = eb.global_completion(G, method=eb.SYNTACTIC, simplify=True)
    assert(R_semantic == R_syntactic)


def test_global_completion_chain_1():
    p = eb.parse_formula('p')
    G = eb.path_graph(5)
    G.add_formula(0, p)
    G.add_formula(4, ~p)
    R_semantic = eb.global_completion(G, method=eb.SEMANTIC, simplify=True)
    print(R_semantic.formulas())
    assert(R_semantic.formulas() == {0: set([p]), 1: set([]), 2: set([]), 3: set([]), 4: set([~p])})

    R_syntactic = eb.global_completion(G, method=eb.SYNTACTIC, simplify=True)
    assert(R_semantic == R_syntactic)


def test_global_completion_chain_2():
    p = eb.parse_formula('p')
    q = eb.parse_formula('q')
    G = eb.path_graph(4)
    G.add_formula(0, p & q)
    G.add_formula(3, ~p)
    R_semantic = eb.global_completion(G, simplify=True)
    assert(R_semantic.formulas() == {0: set([p & q]), 1: set([q]), 2: set([q]), 3: set([~p & q])})

    R_syntactic = eb.global_completion(G, method=eb.SYNTACTIC, simplify=True)
    assert(R_semantic == R_syntactic)


def test_global_completion_big_chain():
    p = eb.parse_formula('p')
    q = eb.parse_formula('q')
    G = eb.path_graph(10)
    G.add_formula(0, 'p & q')
    G.add_formula(9, '~p & ~q')
    R_semantic = eb.global_completion(G, simplify=True)
    for node in range(1,9):
        assert(R_semantic.formulas(node) == set([]))
    assert(R_semantic.formulas(0) == set([p & q]))
    assert(R_semantic.formulas(9) == set([~p & ~q]))

    R_syntactic = eb.global_completion(G, method=eb.SYNTACTIC, simplify=True)
    assert(R_semantic == R_syntactic)


if __name__ == '__main__':
    test_global_completion_cardinality()
    test_global_completion_two_nodes()
    test_global_completion_chain_1()
    test_global_completion_chain_2()
    test_global_completion_big_chain()
