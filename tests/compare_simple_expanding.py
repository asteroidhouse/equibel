from sympy.logic.inference import entails
import equibel as eb

def strictly_stronger(S,T):
    """Returns True if every formula in S entails the corresponding formula in T."""
    for node in S:
        s_formula = S.formula_conj(node)
        t_formula = T.formula_conj(node)
        if not entails(t_formula, [s_formula]):
            return False
    return True


def test_simple_expanding_noncomparable():
    G = eb.path_graph(6)
    G.add_formula(0, '~x3')
    G.add_formula(2, '~x1 | x3')
    G.add_formula(3, '(x1 | x2) & x3')
    G.add_formula(5, '~x2')
    R_simple, num_simple_iterations = eb.iterate_simple_fixpoint(G, method=eb.SYNTACTIC, simplify=True)
    R_expanding, num_expanding_iterations = eb.iterate_expanding_fixpoint(G, method=eb.SYNTACTIC, simplify=True)
    assert(R_simple != R_expanding)
    assert(not strictly_stronger(R_expanding, R_simple))
    assert(not strictly_stronger(R_simple, R_expanding))


if __name__ == '__main__':
    test_simple_expanding_noncomparable()
