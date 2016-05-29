import equibel as eb


def test_simple_iteration_chain_1():
    p = eb.parse_formula('p')
    G = eb.path_graph(5)
    G.add_formula(0, p)
    G.add_formula(4, ~p)
    R_semantic = eb.iterate_simple(G, method=eb.SEMANTIC, simplify=True)
    print(R_semantic.formulas())
    assert(R_semantic.formulas() == {0: set([p]), 1: set([p]), 2: set([]), 3: set([~p]), 4: set([~p])})

    R_syntactic = eb.iterate_simple(G, method=eb.SYNTACTIC, simplify=True)
    print(R_syntactic.formulas())
    assert(R_syntactic == R_semantic)


def test_simple_iteration_chain_2():
    p = eb.parse_formula('p')
    G = eb.path_graph(5)
    G.add_formula(0, p)
    G.add_formula(4, ~p)
    H = eb.iterate_simple(G, simplify=True)
    R = eb.iterate_simple(H, simplify=True)
    print(R.formulas())
    assert(R.formulas() == {0: set([p]), 1: set([p]), 2: set([]), 3: set([~p]), 4: set([~p])})

if __name__ == '__main__':
    test_simple_iteration_chain_1()
    test_simple_iteration_chain_2()
