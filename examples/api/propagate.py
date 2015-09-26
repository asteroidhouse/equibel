import equibel
G = equibel.path_graph(5)
G.add_formula(0, 'p')
G.add_formula(2, '~p')
G.add_formula(4, 'p | q')
R = equibel.completion(G, method=equibel.CONTAINMENT)
print(R.formulas())
