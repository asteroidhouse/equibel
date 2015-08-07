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

    # TODO: Possibly replace this with iter(self.graph)
    def __iter__(self):
        return iter(self.graph.nodes())

    def __getitem__(self, value):
        return self.graph[value]

    # ================================================
    #                NODE METHODS
    # ================================================

    def nodes(self):
        """Return the list of nodes.
        """
        return self.graph.nodes()

    def add_node(self, node_id):
        """Add a node to the graph.
        
        Parameters
        ----------
        node_id : any type, usually an int

        Examples
        --------
        Create a graph:
        >>> G = Graph()

        Add a node:
        >>> G.add_node(1)
        """
        self.graph.add_node(node_id)
        self.graph.node[node_id][WEIGHTS_KEY]  = dict()
        self.graph.node[node_id][FORMULAS_KEY] = set()
        self.__add_atoms_to_new_node(node_id)

    def add_nodes(self, nodes):
        """Add all nodes from an iterable container.

        Parameters
        ----------
        nodes : any iterable container

        Example
        -------
        
        """
        for node in nodes:
            self.add_node(node)

    def remove_node(self, node_id):
        """Remove a node from the graph.

        Parameters
        ----------
        node_id : any type, usually an int

        Example
        -------
        >>> G = Graph()
        >>> G.add_nodes([1,2,3])
        >>> G.remove_node(1)
        >>> G.nodes()
        [2,3]
        """
        self.graph.remove_node(node_id)

    # Perhaps this could be called "remove_nodes"
    def remove_nodes_from(self, nodes):
        """Remove nodes specified in an iterable container.

        Parameters
        ----------
        nodes : any iterable container

        Example
        -------
        >>> G = Graph()
        >>> G.add_nodes([1,2,3,4])
        >>> G.nodes()
        [1,2,3,4]
        >>> G.remove_nodes_from([1,2])
        >>> G.nodes()
        [2,4]

        Nodes in the iterable that are not in the graph 
        are ignored:

        >>> G.add_nodes([3,4])
        >>> G.nodes()
        [1,2,3,4]
        >>> G.remove_nodes_from([4,5,6])
        >>> G.nodes()
        [1,2,3]
        """
        self.graph.remove_nodes_from(nodes)

    # ================================================
    #                 EDGE METHODS
    # ================================================

    # ROUTING to G.edges()
    def edges(self):
        """Returns a list of edges of the graph.

        Example
        -------
        >>> G = equibel.path_graph(4)
        >>> G.edges()
        [(1,2), (2,3), (3,4)]
        """
        return self.graph.edges()

    def add_edge(self, from_node_id, to_node_id):
        """Adds an edge to the graph. If an endpoint
        of the edge is not already in the graph, it 
        is added as a new node automatically. So, an 
        easy way to create a graph is to just add 
        the desired edges; the necessary nodes will 
        be created for you.

        Parameters
        ----------
        from_node_id : any type, usually an int
        to_node_id   : any type, usually an int

        Examples
        -------
        >>> G = Graph()
        >>> G.add_edge(1,2)
        >>> G.add_edge(1,3)
        >>> G.edges()
        [(1,2), (2,3)]
        >>> G.nodes()
        [1,2,3]
        """
        if from_node_id not in self.graph:
            self.add_node(from_node_id)
        if to_node_id not in self.graph:
            self.add_node(to_node_id)

        self.graph.add_edge(from_node_id, to_node_id)

    def add_edges(self, edges):
        """Adds edges to the graph from an iterable container.
        Any endpoint of an edge that is not already in the list 
        of nodes will be automatically added as a node.

        Parameters
        ----------
        edges : any iterable consisting of pairs (2-tuples)

        Examples
        --------
        >>> G = Graph()
        >>> G.add_edges([(1,2), (2,3), (3,4)])
        >>> G.edges()
        [(1,2), (2,3), (3,4)]
        >>> G.nodes()
        [1,2,3,4]
        """
        for (from_node_id, to_node_id) in edges:
            self.add_edge(from_node_id, to_node_id)

    def remove_edge(self, from_node_id, to_node_id):
        """Removes an edge from the graph, if it exists. 
        Otherwise, does nothing. This does not remove 
        any nodes that were added by the add_edge or 
        add_edges functions.

        Parameters
        ----------
        from_node_id : any type, usually an int
        to_node_id   : any type, usually an int

        Examples
        --------
        >>> G = Graph()
        >>> G.add_edges([(1,2), (1,3), (1,4)])
        >>> G.edges()
        [(1,2), (1,3), (1,4)]
        >>> G.nodes()
        [1,2,3,4]
        >>> G.remove_edge(1,4)
        >>> G.edges()
        [(1,2), (1,3)]
        >>> G.nodes()
        [1,2,3,4]
        """
        self.graph.remove_edge(from_node_id, to_node_id)

    def to_directed(self):
        """Creates a directed copy of this graph.

        """
        return EquibelGraph(self.graph.to_directed())

    def to_undirected(self):
        """Creates an undirected copy of this graph.
        """
        return EquibelGraph(self.graph.to_undirected())

    def is_directed(self):
        """Checks whether this graph is directed.

        Example
        -------
        >>> G = Graph()
        >>> 
        """
        return self.graph.is_directed()

    # TODO: What if the graph is undirected? 
    def reverse(self):
        """Creates a copy of this graph with the directions 
        of all edges reversed.

        """
        return EquibelGraph(self.graph.reverse())

    # ================================================
    #             ATOM and WEIGHT METHODS
    # ================================================

    # Instead of G.graph[ATOMS_KEY], use G.atoms()
    def atoms(self):
        """Returns a list of atoms that appear somewhere 
        in the graph. That is, this returns a list of atoms 
        used by at least one formula of one node in the graph.

        Example
        -------
        >>> G = Graph()
        >>> G.add_node(1)
        >>> G.add_formula(1, "p & q")
        >>> G.atoms()
        ['p', 'q']
        """
        # TODO: Is this how atoms are returned? Strings?
        return self.graph.graph[ATOMS_KEY]

    # Instead of G.node[node_id][WEIGHTS_KEY], use G.atom_weights(node_id)
    def atom_weights(self, node_id):
        """
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
