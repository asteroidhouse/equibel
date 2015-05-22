"""The graph class used to represent networks of agents in Equibel.
"""
#    Copyright (C) 2014-2015 by
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.
from __future__ import absolute_import
from __future__ import print_function

import networkx as nx
import equibel

ATOMS_KEY    = "atoms"
WEIGHTS_KEY  = "weights"
FORMULAS_KEY = "formulas"

class EquibelGraph:

    def __init__(self, G=None):
        if G:
            self.graph = G.copy()
            self.graph.graph[ATOMS_KEY] = set()
            for node_id in G.nodes():
                self.graph.node[node_id][WEIGHTS_KEY] = dict()
                self.graph.node[node_id][FORMULAS_KEY] = set()
        else:
            self.graph = nx.Graph()
            self.graph.graph[ATOMS_KEY] = set()

    def __iter__(self):
        return iter(self.graph.nodes())

    def __getitem__(self, value):
        return self.graph[value]

    # ================================================
    #                NODE METHODS
    # ================================================

    # ROUTING to G.nodes()
    def nodes(self):
        return self.graph.nodes()

    def add_node(self, node_id):
        self.graph.add_node(node_id)
        self.graph.node[node_id][WEIGHTS_KEY]  = dict()
        self.graph.node[node_id][FORMULAS_KEY] = set()
        self.__add_atoms_to_new_node(node_id)

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def remove_node(self, node_id):
        self.graph.remove_node(node_id)

    # Perhaps this could be called "remove_nodes"
    def remove_nodes_from(self, nodes):
        self.graph.remove_nodes_from(nodes)

    # ================================================
    #                 EDGE METHODS
    # ================================================

    # ROUTING to G.edges()
    def edges(self):
        return self.graph.edges()

    def add_edge(self, from_node_id, to_node_id):
        if from_node_id not in self.graph:
            self.add_node(from_node_id)
        if to_node_id not in self.graph:
            self.add_node(to_node_id)

        self.graph.add_edge(from_node_id, to_node_id)

    def add_edges(self, edges):
        for (from_node_id, to_node_id) in edges:
            self.add_edge(from_node_id, to_node_id)

    def remove_edge(self, from_node_id, to_node_id):
        self.graph.remove_edge(from_node_id, to_node_id)

    # (not quite) ROUTING to G.to_directed()
    def to_directed(self):
        return EquibelGraph(self.graph.to_directed())

    # (not quite) ROUTING to G.to_undirected()
    def to_undirected(self):
        return EquibelGraph(self.graph.to_undirected())

    # ROUTING to G.is_directed()
    def is_directed(self):
        return self.graph.is_directed()

    def reverse(self):
        return EquibelGraph(self.graph.reverse())

    # ================================================
    #             ATOM and WEIGHT METHODS
    # ================================================

    # Instead of G.graph[ATOMS_KEY], use G.atoms()
    def atoms(self):
        return self.graph.graph[ATOMS_KEY]

    # Instead of G.node[node_id][WEIGHTS_KEY], use G.atom_weights(node_id)
    def atom_weights(self, node_id):
        return self.graph.node[node_id][WEIGHTS_KEY]

    def weight(self, node_id, atom):
        return self.graph.node[node_id][WEIGHTS_KEY][atom]

    def add_atom(self, atom):
        self.graph.graph[ATOMS_KEY].add(atom)
        self.__add_new_atom_to_nodes(atom)

    def add_atoms(self, atoms):
        for atom in atoms:
            self.add_atom(atom)

    def __add_new_atom_to_nodes(self, atom):
        for node_id in self.nodes():
            if atom not in self.atom_weights(node_id):
                self.set_atom_weight(node_id, atom, 1)

    def __add_atoms_to_new_node(self, node_id):
        for atom in self.atoms():
            self.set_atom_weight(node_id, atom, 1)

    def set_atom_weight(self, node_id, atom, weight):
        self.graph.node[node_id][WEIGHTS_KEY][atom] = weight
        if atom not in self.atoms():
            self.add_atom(atom)

    # For convenience:
    def add_weight(self, node_id, atom, weight):
        self.set_atom_weight(node_id, atom, weight)

    def remove_atom(self, atom):
        self.graph.graph[ATOMS_KEY].discard(atom)
        self.__remove_atom_from_nodes(atom)

    def __remove_atom_from_nodes(self, atom):
        for node_id in self.nodes():
            weights = self.atom_weights(node_id)
            if atom in weights:
                del weights[atom]

    # ================================================
    #               FORMULA METHODS
    # ================================================

    # Instead of G.node[node_id][FORMULAS_KEY], use G.formulas(node_id)
    def formulas(self, node_id):
        return self.graph.node[node_id][FORMULAS_KEY]

    def add_formula(self, node_id, formula):
        if isinstance(formula, str):
            parsed_formula = equibel.parse_infix_formula(formula)
            self.graph.node[node_id][FORMULAS_KEY].add(parsed_formula)
            self.__add_formula_atoms(parsed_formula)
        else:
            self.graph.node[node_id][FORMULAS_KEY].add(formula)
            self.__add_formula_atoms(formula)

    def __add_formula_atoms(self, formula):
        for atom in formula.get_atoms():
            if atom not in self.atoms():
                self.add_atom(atom)

    def set_formulas(self, node_id, formula_list):
        self.clear_formulas_from(node_id)
        for formula in formula_list:
            self.graph.node[node_id][FORMULAS_KEY].add(formula)

    def clear_formulas_from(self, node_id):
        self.graph.node[node_id][FORMULAS_KEY].clear()

    def clear_formulas(self):
        for node_id in self.nodes():
            self.graph.node[node_id][FORMULAS_KEY].clear()

    def remove_formula(self, node_id, formula):
        self.graph.node[node_id][FORMULAS_KEY].discard(formula)
