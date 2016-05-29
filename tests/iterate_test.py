from sympy import pprint, satisfiable, to_cnf, simplify
import networkx as nx
import equibel as eb

def print_formulas(G):
    for node in G.nodes():
        print("Node {}:".format(node))
        pprint(G.formula_conj(node))
        #pprint(simplify(G.formula_conj(node)))
        #pprint(to_cnf(G.formula_conj(node), simplify=True))
    print("\n")
        

if __name__ == '__main__':
    G = eb.path_graph(5)
    G.add_formula(2, '(x1 & ~x4) | (x4 & ~x1) | ~x5')
    G.add_formula(3, 'x4 | ~x2 | ~x3')
    G.add_formula(4, '~x3 & (x4 | ~x5) & (x5 | ~x4)')

    print_formulas(G)

    G, num_iterations = eb.iterate_steady(G)
    print_formulas(G)

    print(G.formula_conj(0))
    for model in satisfiable(G.formula_conj(0), all_models=True):
        print(model)

    print("Num iterations = {}".format(num_iterations))