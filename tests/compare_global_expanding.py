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


def test_global_expanding_noncomparable():
    G = eb.path_graph(3)
    G.add_formula(0, 'x3 & (x1 | ~x2) & (x2 | ~x1)')
    G.add_formula(1, '(x2 & x3) | (~x2 & ~x3)')
    G.add_formula(2, '~x3')
    R_completion = eb.global_completion(G, simplify=True)
    R_expanding = eb.iterate_expanding(G, simplify=True)
    assert(R_completion != R_expanding)
    assert(not strictly_stronger(R_expanding, R_completion))
    assert(not strictly_stronger(R_completion, R_expanding))


if __name__ == '__main__':
    test_global_expanding_noncomparable()