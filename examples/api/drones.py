import equibel
G = equibel.complete_graph(3)
G.add_formula(0, 'a & b')
G.add_formula(1, '~a | ~b')
G.add_formula(2, 'c')
R = equibel.completion(G)
print(R.formulas())
