import equibel as eb


def test_path_graph():
    G = eb.path_graph(4)
    assert(G.nodes() == [0,1,2,3])
    assert(G.edges() == [(0,1), (1,2), (2,3)])
    assert(G.formulas() == {0: set(), 1: set(), 2: set(), 3: set()})


def test_complete_graph():
    G = eb.complete_graph(4)
    assert(G.nodes() == [0,1,2,3])
    assert(G.edges() == [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
    assert(G.formulas() == {0: set(), 1: set(), 2: set(), 3: set()})


def test_star_graph():
    G = eb.star_graph(4)
    assert(G.nodes() == [0, 1, 2, 3, 4])
    assert(G.edges() == [(0, 1), (0, 2), (0, 3), (0, 4)])
