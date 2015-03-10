import networkx as nx
from equibel.EquibelGraph import EquibelGraph

if __name__ == '__main__':
	G = EquibelGraph(nx.path_graph(10))
	length = nx.all_pairs_shortest_path_length(G)
	print(length)
