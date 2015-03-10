import networkx as nx
from equibel.EquibelGraph import EquibelGraph

def line_graph(n):
    return EquibelGraph(nx.line_graph(n))

def complete_graph(n):
    return EquibelGraph(nx.complete_graph(n))

def star_graph(n):
    return EquibelGraph(nx.star_graph(n))
