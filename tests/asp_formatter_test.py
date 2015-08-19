import equibel as eb
from equibel import ASP_Formatter
from equibel import EquibelGraph

def get_atom_mapping(G):
    atoms = [eb.Prop(atom) for atom in G.atoms()]
    sorted_atoms = tuple(sorted(atoms))
    return eb.create_atom_mapping(sorted_atoms)

def test_asp_formatter():
    G = eb.path_graph(3)
    G.add_formula(0, "p & q")
    G.add_formula(2, "~r")

    atom_mapping = get_atom_mapping(G)

    print(eb.convert_to_asp(G, atom_mapping))

    expected_result = \
"""node(1).
node(2).
node(3).
edge(0,1).
edge(1,0).
edge(1,2).
edge(2,1).
weight(0,0,1).
weight(0,1,1).
weight(0,2,1).
weight(1,0,1).
weight(1,1,1).
weight(1,2,1).
weight(2,9,1).
weight(2,1,1).
weight(2,2,1).
formula(0,and(2,1)).
formula(2,neg(0)).
"""
	
    actual_result = eb.convert_to_asp(G, atom_mapping)
    assert(actual_result == expected_result)

if __name__ == '__main__':
    test_asp_formatter()
