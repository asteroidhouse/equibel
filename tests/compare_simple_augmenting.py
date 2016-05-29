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


def test_simple_augmenting_fixpoints_noncomparable():
    G = eb.path_graph(5)
    G.add_formula(0, 'x1 & x3')
    G.add_formula(1, 'x1')
    G.add_formula(2, 'x4')
    G.add_formula(3, '~x3 | x4')
    G.add_formula(4, '~x4')
    R_augmenting, num_augmenting_iterations = eb.iterate_augmenting_fixpoint(G, simplify=True)
    R_simple, num_simple_iterations = eb.iterate_simple_fixpoint(G, simplify=True)
    assert(R_simple != R_augmenting)
    assert(not strictly_stronger(R_augmenting, R_simple))
    assert(not strictly_stronger(R_simple, R_augmenting))


if __name__ == '__main__':
    test_simple_augmenting_fixpoints_noncomparable()