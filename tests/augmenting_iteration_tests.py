import equibel as eb


def test_augmenting_iteration_chain():
    p, q, r = [eb.parse_formula(letter) for letter in "pqr"]
    G = eb.path_graph(5)
    G.add_formula(0, p & q)
    G.add_formula(4, ~p & ~q)
    R_semantic, num_augmenting_iterations = eb.iterate_augmenting_fixpoint(G, method=eb.SEMANTIC, simplify=True)
    print(R_semantic.formulas())
    assert(R_semantic.formulas() == {0: set([p & q]), 1: set([p & q]), 2: set([]), 3: set([~p & ~q]), 4: set([~p & ~q])})

    R_syntactic, num_augmenting_iterations = eb.iterate_augmenting_fixpoint(G, method=eb.SYNTACTIC, simplify=True)
    print(R_syntactic.formulas())
    assert(R_semantic == R_syntactic)


if __name__ == '__main__':
    test_augmenting_iteration_chain()