import networkx as nx
from equibel.EquibelGraph import EquibelGraph

if __name__ == '__main__':
    G = EquibelGraph(nx.path_graph(10))
    length = nx.all_pairs_shortest_path_length(G)
    print(length)
    for from_node_id in length:
        dists = length[from_node_id]
        for to_node_id in dists:
            distance = dists[to_node_id]
            print("dist({0},{1},{2}).".format(from_node_id, to_node_id, distance))

