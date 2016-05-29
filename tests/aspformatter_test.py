import equibel as eb
from equibel import aspformatter

def test_aspformatter1():
    G = eb.path_graph(3)
    G.add_formula(0, "p & q")
    G.add_formula(2, "~r")

    expected_result = \
"""node(0).
node(1).
node(2).
edge(0,1).
edge(1,0).
edge(1,2).
edge(2,1).
formula(0,and(p,q)).
formula(2,neg(r)).
atom(p).
atom(r).
atom(q).
"""
    actual_result = eb.to_asp(G)
    assert(actual_result == expected_result)

if __name__ == '__main__':
    test_aspformatter()