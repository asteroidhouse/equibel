import equibel as eb


def test_expanding_cardinality():
    G = eb.star_graph(3)
    G.add_formula(1, 'p')
    G.add_formula(2, 'p')
    G.add_formula(3, '~p')
    R_semantic, num_expanding_iterations = eb.iterate_expanding_fixpoint(G, method=eb.SEMANTIC, opt_type=eb.CARDINALITY, simplify=True)
    assert(R_semantic.formula_conj(0) == eb.parse_formula('p'))

    R_syntactic, num_expanding_iterations = eb.iterate_expanding_fixpoint(G, method=eb.SYNTACTIC, opt_type=eb.CARDINALITY, simplify=True)
    assert(R_syntactic == R_semantic)


def test_expanding_iteration_chain_semantic():
    p = eb.parse_formula('p')
    G = eb.path_graph(5)
    G.add_formula(0, p)
    G.add_formula(4, ~p)
    R_semantic, num_expanding_iterations = eb.iterate_expanding_fixpoint(G, method=eb.SEMANTIC, simplify=True)
    assert(R_semantic.formulas() == {0: set([p]), 1: set([p]), 2: set([]), 3: set([~p]), 4: set([~p])})


def test_expanding_iteration_chain_syntactic():
    p = eb.parse_formula('p')
    G = eb.path_graph(5)
    G.add_formula(0, p)
    G.add_formula(4, ~p)
    R_syntactic, num_expanding_iterations = eb.iterate_expanding_fixpoint(G, method=eb.SYNTACTIC, simplify=True)
    assert(R_syntactic.formulas() == {0: set([p]), 1: set([p]), 2: set([]), 3: set([~p]), 4: set([~p])})


def test_expanding_iteration_medium_chain():
    p, q, r = [eb.parse_formula(letter) for letter in "pqr"]
    f = p & q & r
    g = ~p & ~q & ~r
    G = eb.path_graph(10)
    G.add_formula(0, f)
    G.add_formula(9, g)

    R_semantic, num_expanding_iterations = eb.iterate_expanding_fixpoint(G, method=eb.SEMANTIC, simplify=True)
    print(R_semantic.formulas())
    for node in range(0, 5):
        assert(R_semantic.formula_conj(node) == f)
    for node in range(5,10):
        assert(R_semantic.formula_conj(node) == g)

    R_syntactic, num_expanding_iterations = eb.iterate_expanding_fixpoint(G, method=eb.SYNTACTIC, simplify=True)
    assert(R_semantic == R_syntactic)

"""
def test_expanding_iteration_big_chain():
    p, q, r = [eb.parse_formula(letter) for letter in "pqr"]
    f = p & q & r
    g = ~p & ~q & ~r
    G = eb.path_graph(20)
    G.add_formula(0, f)
    G.add_formula(19, g)

    R_semantic, num_expanding_iterations = eb.iterate_expanding_fixpoint(G, method=eb.SEMANTIC, simplify=True)
    print(R_semantic.formulas())
    for node in range(0, 10):
        assert(R_semantic.formula_conj(node) == f)
    for node in range(11,20):
        assert(R_semantic.formula_conj(node) == g)

    R_syntactic, num_expanding_iterations = eb.iterate_expanding_fixpoint(G, method=eb.SYNTACTIC, simplify=True)
    assert(R_semantic == R_syntactic)
"""

if __name__ == '__main__':
    #test_expanding_iteration_chain()
    test_expanding_iteration_medium_chain()
    #test_expanding_iteration_big_chain()
