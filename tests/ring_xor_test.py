from sympy import pprint, satisfiable, to_cnf, simplify
import equibel as eb


def test_xor_augmenting_fixpoint():
    G = eb.path_graph(4)
    p, q = [eb.parse_formula(letter) for letter in "pq"]
    G.add_formula(0, (p & ~q) | (~p & q))
    G.add_formula(1, p)
    G.add_formula(3, ~p)
    R_augmenting, num_iterations = eb.iterate_augmenting_fixpoint(G, method=eb.SEMANTIC, simplify=True)
    assert(R_augmenting.formulas() == {0: set([p & ~q]), 1: set([p & ~q]), 2: set([~q]), 3: set([~p & ~q])})

    R_augmenting_syntactic, num_iterations = eb.iterate_augmenting_fixpoint(G, method=eb.SYNTACTIC, simplify=True)
    assert(R_augmenting_syntactic == R_augmenting)


def test_xor_expanding_fixpoint():
    G = eb.path_graph(4)
    p, q = [eb.parse_formula(letter) for letter in "pq"]
    G.add_formula(0, (p & ~q) | (~p & q))
    G.add_formula(1, p)
    G.add_formula(3, ~p)
    R_expanding, num_iterations = eb.iterate_expanding_fixpoint(G, method=eb.SEMANTIC, simplify=True)
    assert(R_expanding.formulas() == {0: set([p & ~q]), 1: set([p & ~q]), 2: set([~q]), 3: set([~p & ~q])})

    R_expanding_syntactic, num_iterations = eb.iterate_expanding_fixpoint(G, method=eb.SYNTACTIC, simplify=True)
    assert(R_expanding_syntactic == R_expanding)


def test_xor_global_completion():
    G = eb.path_graph(4)
    p, q = [eb.parse_formula(letter) for letter in "pq"]
    G.add_formula(0, (p & ~q) | (~p & q))
    G.add_formula(1, p)
    G.add_formula(3, ~p)
    R_completion = eb.global_completion(G, method=eb.SEMANTIC, simplify=True)
    assert(R_completion.formulas() == {0: set([p & ~q]), 1: set([p & ~q]), 2: set([~q]), 3: set([~p & ~q])})

    R_completion_syntactic = eb.global_completion(G, method=eb.SYNTACTIC, simplify=True)
    assert(R_completion_syntactic == R_completion)



def test_xor_simple_fixpoint():
    G = eb.path_graph(4)
    p, q = [eb.parse_formula(letter) for letter in "pq"]
    G.add_formula(0, (p & ~q) | (~p & q))
    G.add_formula(1, p)
    G.add_formula(3, ~p)
    R_simple, num_simple_iterations = eb.iterate_simple_fixpoint(G, method=eb.SEMANTIC, simplify=True)
    assert(R_simple.formulas() == {0: set([p & ~q]), 1: set([p & ~q]), 2: set([~q]), 3: set([~p & ~q])})

    R_simple_syntactic, num_simple_iterations = eb.iterate_simple_fixpoint(G, method=eb.SYNTACTIC, simplify=True)
    assert(R_simple_syntactic == R_simple)


def test_xor_ring_first_iteration():
    G = eb.path_graph(4)
    p, q = [eb.parse_formula(letter) for letter in "pq"]
    G.add_formula(0, (p & ~q) | (~p & q))
    G.add_formula(1, p)
    G.add_formula(3, ~p)
    R_ring = eb.iterate_ring(G, method=eb.SEMANTIC, simplify=True)
    assert(R_ring.formulas() == {0: set([p & ~q]), 1: set([p & ~q]), 2: set([(p & ~q) | (~p & q)]), 3: set([~p & q])})

    R_ring_syntactic = eb.iterate_ring(G, method=eb.SYNTACTIC, simplify=True)
    assert(R_ring_syntactic == R_ring)


def test_xor_ring_fixpoint():
    G = eb.path_graph(4)
    p, q = [eb.parse_formula(letter) for letter in "pq"]
    G.add_formula(0, (p & ~q) | (~p & q))
    G.add_formula(1, p)
    G.add_formula(3, ~p)
    R_ring, num_ring_iterations = eb.iterate_ring_fixpoint(G, method=eb.SEMANTIC, simplify=True)
    assert(R_ring.formulas() == {0: set([p & ~q]), 1: set([p & ~q]), 2: set([p & ~q]), 3: set([~p & q])})

    R_ring_syntactic, num_ring_iterations = eb.iterate_ring_fixpoint(G, method=eb.SYNTACTIC, simplify=True)
    assert(R_ring_syntactic == R_ring)


def print_formulas(G, label=None):
    if label:
        print("{}".format(label))
        print("----------------------")
    for node in G.nodes():
        print("Node {}:".format(node))
        pprint(G.formula_conj(node))
    print("\n")

if __name__ == '__main__':
    G = eb.path_graph(4)
    G.add_formula(0, '(p & ~q) | (~p & q)')
    G.add_formula(1, 'p')
    G.add_formula(3, '~p')

    R, num_iterations = eb.iterate_augmenting_fixpoint(G, simplify=True)
    R2, num_expanding_iterations = eb.iterate_expanding_fixpoint(G, simplify=True)
    R3 = eb.global_completion(G, simplify=True)
    R4, num_simple_iterations = eb.iterate_simple_fixpoint(G, simplify=True)
    R5, num_ring_iterations = eb.iterate_ring_fixpoint(G, simplify=True)

    """
    R= eb.iterate_augmenting(G)
    R2= eb.iterate_expanding(G)
    R3 = eb.completion(G)
    R4= eb.iterate_simple(G)
    R5= eb.iterate_ring(G)
    """

    print_formulas(R, label="Augmenting")
    print_formulas(R2, label="Expanding2")
    print_formulas(R3, label="Global Completion")
    print_formulas(R4, label="Simple")
    print_formulas(R5, label="Ring")

    R6 = eb.iterate_ring(G, simplify=True)
    print_formulas(R6)
