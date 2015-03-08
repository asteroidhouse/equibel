import equibel.format.BCF_Formatter as BCF_Formatter
from equibel.EquibelGraph import EquibelGraph

def test_bcf_formatter():
	G = EquibelGraph()
	G.add_nodes([1,2,3])
	G.add_edges([(1,2), (2,3)])
	G.add_atom('a')
	G.add_weight(1, 'b', 4)

	print(BCF_Formatter.convert_to_bcf(G))

	expected_result = \
"""t undirected
n 1
n 2
n 3
a a
a b
e 1 2
e 2 1
e 2 3
e 3 2
w 1 a 1
w 1 b 4
w 2 a 1
w 2 b 1
w 3 a 1
w 3 b 1
"""
	
	actual_result = BCF_Formatter.convert_to_bcf(G)
	assert(actual_result == expected_result)

if __name__ == '__main__':
	test_bcf_formatter()