import equibel as eb


def test_graph_eq():
    G1 = eb.path_graph(3)
    G1.add_formula(0, 'p & q')
    G1.add_formula(1, 'q | r')
    G2 = eb.path_graph(3)
    G2.add_formula(0, 'p & q')
    G2.add_formula(1, 'r | q')
    assert(G1 == G2)


def test_graph_ne():
    G1 = eb.path_graph(3)
    G1.add_formula(0, 'p & q')
    G1.add_formula(1, 'q | r')
    G2 = eb.path_graph(3)
    G2.add_formula(0, 'p & q')
    assert(G1 != G2)


def test_graph_copy_nodes():
    G = eb.path_graph(3)
    C = G.copy()
    assert(G.nodes() == [0, 1, 2])
    assert(C.nodes() == [0, 1, 2])
    C.add_node(3)
    assert(G.nodes() == [0, 1, 2])
    assert(C.nodes() == [0, 1, 2, 3])


def test_graph_copy_edges():
    G = eb.path_graph(3)
    C = G.copy()
    assert(G.edges() == [(0, 1), (1, 2)])
    assert(C.edges() == [(0, 1), (1, 2)])
    C.add_edge(2,3)
    assert(G.edges() == [(0, 1), (1, 2)])
    assert(C.edges() == [(0, 1), (1, 2), (2, 3)])


def test_graph_copy_formulas():
    p,q,r,s = [eb.Prop(atom) for atom in 'pqrs']
    G = eb.path_graph(3)
    G.add_formula(0, p & q | ~r)
    G.add_formula(0, s)
    G.add_formula(1, p | q)
    C = G.copy()
    assert(G.formulas() == {0: set([(q & p) | ~r, s]), 1: set([q | p]), 2: set([])})
    assert(C.formulas() == {0: set([(q & p) | ~r, s]), 1: set([q | p]), 2: set([])})
    C.add_formula(1, ~s | q)
    assert(G.formulas() == {0: set([(q & p) | ~r, s]), 1: set([q | p]), 2: set([])})
    assert(C.formulas() == {0: set([(q & p) | ~r, s]), 1: set([q | ~s, q | p]), 2: set([])})


def test_graph_nodes():
    G = eb.EquibelGraph()
    G.add_nodes([1,2,3])
    assert(G.nodes() == [1,2,3])


def test_graph_add_node():
    G = eb.EquibelGraph()
    G.add_node(1)
    assert(G.nodes() == [1])
    assert(G.nodes() != [])


def test_graph_add_nodes():
    G = eb.EquibelGraph()
    G.add_nodes([1,2,3])
    assert(G.nodes() == [1,2,3])
    s = {4, 5, 6}
    G.add_nodes(s)
    assert(G.nodes() == [1,2,3,4,5,6])


def test_graph_remove_node():
    G = eb.EquibelGraph()
    G.add_nodes([1,2,3])
    G.remove_node(1)
    assert(G.nodes() == [2,3])


def test_graph_remove_nodes_from():
    G = eb.EquibelGraph()
    G.add_nodes([1,2,3,4])
    G.remove_nodes_from([1,2])
    assert(G.nodes() == [3,4])


def test_graph_remove_nodes_from_ignore():
    G = eb.EquibelGraph()
    G.add_nodes([1,2,3,4])
    G.remove_nodes_from([4,5,6])
    assert(G.nodes() == [1,2,3])


def test_graph_edges():
    G = eb.path_graph(4)
    assert(G.edges() == [(0,1), (1,2), (2,3)])


def test_graph_add_edge_existing_nodes():
    G = eb.EquibelGraph()
    G.add_nodes([1,2])
    G.add_edge(1,2)
    assert(G.edges() == [(1,2)])


def test_graph_add_edge_auto_add_nodes():
    G = eb.EquibelGraph()
    G.add_edge(1,2)
    assert(G.edges() == [(1,2)])
    assert(G.nodes() == [1,2])


def test_graph_add_edges():
    G = eb.EquibelGraph()
    G.add_edges([(1,2), (2,3), (3,4)])
    assert(G.edges() == [(1,2), (2,3), (3,4)])
    assert(G.nodes() == [1,2,3,4])


def test_graph_remove_edge():
    G = eb.EquibelGraph()
    G.add_edges([(1,2), (1,3), (1,4)])
    assert(G.edges() == [(1,2), (1,3), (1,4)])
    assert(G.nodes() == [1,2,3,4])
    G.remove_edge(1,4)
    assert(G.edges() == [(1,2), (1,3)])
    assert(G.nodes() == [1,2,3,4])


def test_graph_to_directed():
    G = eb.EquibelGraph()
    G.add_edges([(1,2), (2,3)])
    assert(G.edges() == [(1,2), (2,3)])
    D = G.to_directed()
    assert(D.edges() == [(1,2), (2,1), (2,3), (3,2)])


def test_graph_to_undirected():
    G = eb.EquibelGraph()
    G.add_edges([(1,2), (2,3)])
    assert(G.edges() == [(1,2), (2,3)])
    D = G.to_directed()
    assert(D.edges() == [(1,2), (2,1), (2,3), (3,2)])
    R = D.to_undirected()
    assert(R.edges() == [(1,2), (2,3)])


def test_graph_is_directed():
    G = eb.path_graph(4)
    assert(G.edges() == [(0, 1), (1, 2), (2, 3)])
    assert(G.is_directed() == False)
    D = G.to_directed()
    assert(D.edges() == [(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2)])
    assert(D.is_directed() == True)


def test_graph_reverse_directed():
    D = eb.path_graph(4, directed=True)
    assert(D.edges() == [(0, 1), (1, 2), (2, 3)])
    R = D.reverse()
    assert(R.edges() == [(1, 0), (2, 1), (3, 2)])


def test_graph_reverse_undirected():
    G = eb.path_graph(4)
    R = G.reverse()
    assert(G == R)








