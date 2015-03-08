import equibel.format.ASP_Formatter as ASP_Formatter
from equibel.EquibelGraph import EquibelGraph

def test_asp_formatter():
	G = EquibelGraph()
	G.add_nodes([1,2,3])
	G.add_edges([(1,2), (2,3)])
	G.add_atom('a')
	G.add_weight(1, 'b', 4)

	print(ASP_Formatter.convert_to_asp(G))

	expected_result = \
"""node(1).
node(2).
node(3).
atom(a).
atom(b).
edge(1,2).
edge(2,1).
edge(2,3).
edge(3,2).
weight(1,a,1).
weight(1,b,4).
weight(2,a,1).
weight(2,b,1).
weight(3,a,1).
weight(3,b,1).
"""
	
	actual_result = ASP_Formatter.convert_to_asp(G)
	assert(actual_result == expected_result)

if __name__ == '__main__':
	test_asp_formatter()