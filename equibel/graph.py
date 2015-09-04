"""The graph class used to represent networks of agents in Equibel.
"""
#    Copyright (C) 2014-2015 by
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.
from __future__ import absolute_import
from __future__ import print_function

import copy

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
        return iter(self.graph)

    def __getitem__(self, value):
        return self.graph[value]
    
    def __eq__(self, other):
        """Tests this graph for equality with other. Two graphs are equal
        if they have the same nodes, edges, and formulas at each node. An 
        important note is that formulas are only tested for syntactic 
        equivalence, so if formulas do not look exactly the same, they will 
        not be recognized as equivalent. This is due to efficiency concerns; 
        one way to check whether formulas are equivalent at a deeper level is 
        to first simplify all the formulas, and test the simplified forms for 
        equivalence.

        Parameters
        ----------
        other : an object to test for equality with the current EquibelGraph

        Examples
        --------
        Create the first graph:

        >>> G1 = eb.path_graph(4)
        >>> G1.add_formula(0, 'p & q')
        >>> G1.add_formula(1, 'q | r')

        Create the second graph:

        >>> G2 = eb.path_graph(4)
        >>> G2.add_formula(0, 'p & q')

        Now the graphs are not equal:

        >>> G1 == G2
        False

        We can add a formula to G2 to make it equal to G1:

        >>> G2.add_formula(1, 'q | r')
        >>> G1 == G2
        True
        """
        if not isinstance(other, self.__class__):
            return False
        if set(self.nodes()) != set(other.nodes()):
            return False
        if set(self.edges()) != set(other.edges()):
            return False
        if self.formulas() != other.formulas():
            return False
        return True

    def __ne__(self, other):
        """Tests for non-equality. Negates the result of equality testing."""
        return not self.__eq__(other)

    def copy(self):
        """Creates a copy of this graph.

        Examples
        --------
        Create a graph:

        >>> G = eb.path_graph(3)

        Create a copy of the graph:

        >>> C = G.copy()

        The copy is independently modifiable:

        >>> C.add_edge(2,3)
        >>> C.edges()
        [(0, 1), (1, 2), (2, 3)]
        >>> G.edges()
        [(0, 1), (1, 2)]
        """
        return copy.deepcopy(self)

    # ================================================
    #                NODE METHODS
    # ================================================

    def nodes(self):
        """Return the list of nodes.

        Examples
        --------
        >>> G = EquibelGraph()
        >>> G.add_nodes([1,2,3])
        >>> G.nodes()
        [1,2,3]
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

        >>> G = EquibelGraph()

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

        Examples
        --------
        Create an empty graph:

        >>> G = EquibelGraph()

        Add all nodes from the given list:

        >>> G.add_nodes([1,2,3])
        >>> G.nodes()
        [1,2,3]

        You can also add nodes from other iterables, 
        like sets:

        >>> s = {4,5,6}
        >>> s
        set([4, 5, 6])
        >>> G.add_nodes(s)
        >>> G.nodes()
        [1,2,3,4,5,6]
        """
        for node in nodes:
            self.add_node(node)

    def remove_node(self, node_id):
        """Remove a node from the graph.

        Parameters
        ----------
        node_id : any type, usually an int

        Examples
        --------
        >>> G = EquibelGraph()
        >>> G.add_nodes([1,2,3])
        >>> G.remove_node(1)
        >>> G.nodes()
        [2,3]
        """
        self.graph.remove_node(node_id)

    def remove_nodes_from(self, nodes):
        """Remove nodes specified in an iterable container.

        Parameters
        ----------
        nodes : any iterable container

        Examples
        --------
        >>> G = EquibelGraph()
        >>> G.add_nodes([1,2,3,4])
        >>> G.nodes()
        [1,2,3,4]
        >>> G.remove_nodes_from([1,2])
        >>> G.nodes()
        [3,4]

        Nodes in the iterable that are not in the graph 
        are ignored:

        >>> G.add_nodes([1,2])
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

    def edges(self):
        """Returns a list of the edges in the graph.

        Examples
        --------
        >>> G = eb.path_graph(4)
        >>> G.edges()
        [(0,1), (1,2), (2,3)]
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
        --------
        >>> G = EquibelGraph()
        >>> G.add_edge(1,2)
        >>> G.add_edge(1,3)
        >>> G.edges()
        [(1,2), (2,3)]

        Note that the endpoints of the edges were 
        automatically added as nodes:

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
        Any endpoint of an edge that is not already a node will 
        be automatically added as a new node.

        Parameters
        ----------
        edges : any iterable consisting of pairs (2-tuples)

        Examples
        --------
        >>> G = EquibelGraph()
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
        >>> G = EquibelGraph()
        >>> G.add_edges([(1,2), (1,3), (1,4)])
        >>> G.edges()
        [(1,2), (1,3), (1,4)]
        >>> G.nodes()
        [1,2,3,4]
        >>> G.remove_edge(1,4)
        >>> G.edges()
        [(1,2), (1,3)]

        No nodes are removed by remove_edge, even though 
        node 4 is no longer an endpoint of any edge:

        >>> G.nodes()
        [1,2,3,4]
        """
        self.graph.remove_edge(from_node_id, to_node_id)

    def to_directed(self):
        """Creates a directed copy of this graph. Converting 
        an undirected graph to a directed graph involves 
        creating two edges--in each direction--for every 
        undirected edge.

        Examples
        --------
        >>> G = eb.EquibelGraph()
        >>> G.add_edges([(1,2), (2,3)])
        >>> G.edges()
        [(1, 2), (2, 3)]

        Create a directed copy:

        >>> D = G.to_directed()
        >>> D.edges()
        [(1, 2), (2, 1), (2, 3), (3, 2)]
        """
        return EquibelGraph(self.graph.to_directed())

    def to_undirected(self):
        """Creates an undirected copy of this graph.

        Examples
        --------
        >>> G = eb.EquibelGraph()
        >>> G.add_edges([(1,2), (2,3)])
        >>> G.edges()
        [(1, 2), (2, 3)]

        Create a directed copy:

        >>> D = G.to_directed()
        >>> D.edges()
        [(1, 2), (2, 1), (2, 3), (3, 2)]

        Create an undirected copy:

        >>> R = D.to_undirected()
        >>> R.edges()
        [(1, 2), (2, 3)]
        """
        return EquibelGraph(self.graph.to_undirected())

    def is_directed(self):
        """Checks whether this graph is directed. By 
        default, graphs in Equibel are undirected.

        Examples
        --------
        Create an undirected path graph:

        >>> G = eb.path_graph(4)
        >>> G.edges()
        [(0, 1), (1, 2), (2, 3)]
        >>> G.is_directed()
        False

        Create a directed version of the graph:

        >>> D = G.to_directed()
        >>> D.edges()
        [(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2)]
        >>> D.is_directed()
        True
        """
        return self.graph.is_directed()

    def reverse(self):
        """Creates a copy of this graph with the directions 
        of all edges reversed.

        Example
        -------

        """
        if self.is_directed():
            return EquibelGraph(self.graph.reverse())
        else:
            return self.copy()

    # ================================================
    #             ATOM and WEIGHT METHODS
    # ================================================

    # Returns a list of atoms that appear _somewhere_
    # in the graph. That is, this returns a list of atoms 
    # used by at least one formula of one node in the graph.
    def atoms(self):
        """Returns a list of atoms in the global alphabet of 
        the graph.

        Examples
        --------
        >>> G = Graph()
        >>> G.add_node(1)
        >>> G.add_formula(1, "p & q")
        >>> G.atoms()
        ['p', 'q']
        """
        return self.graph.graph[ATOMS_KEY]

    def atom_weights(self, node_id):
        """Returns a dictionary of (atom, weight) mappings at
        a specific node.

        Parameters
        ----------
        node_id : the ID of the desired node; any type, usually an int

        Examples
        --------
        >>> G = eb.EquibelGraph()
        >>> G.add_nodes([1,2])
        >>> G.add_formula(1, "p & q")
        >>> G.atom_weights(1)
        {'q': 1, 'p': 1}
        """
        return self.graph.node[node_id][WEIGHTS_KEY]

    def weight(self, node_id, atom):
        """Returns the weight of a specific atom at a specific node.

        Parameters
        ----------
        node_id : the ID of the desired node; any type, usually an int
        atom    : the name of the desired atom, as a string

        Examples
        --------
        >>> G = eb.EquibelGraph()
        >>> G.add_nodes([1,2])
        >>> G.add_formula(1, "p & q")
        >>> G.atoms()
        set(['q', 'p'])
        >>> G.weight(1, 'p')
        1
        """
        return self.graph.node[node_id][WEIGHTS_KEY][atom]

    def add_atom(self, atom):
        """Adds an atom to the global alphabet of the graph.

        Parameters
        ----------
        atom : a string representing an atom

        Examples
        --------
        >>> G = eb.EquibelGraph()
        >>> G.add_atom('p')
        >>> G.atoms()
        set(['p'])
        """
        self.graph.graph[ATOMS_KEY].add(atom)
        self.__add_new_atom_to_nodes(atom)

    def add_atoms(self, atoms):
        """Adds multiple atoms to the global alphabet of the graph, 
        from an iterable container.

        Parameters
        ----------
        atoms : an iterable containing objects that can be used to 
                represent atoms; usually strings

        Examples
        --------
        >>> G = eb.EquibelGraph()
        >>> G.add_atoms(['p', 'q', 'r', 's'])
        >>> G.atoms()
        set(['q', 'p', 's', 'r'])
        """
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
        """Removes an atom from the global alphabet of the graph."""
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

    def formulas(self, node_id=None):
        """Returns all the formulas of a specific node, or, if no node_id
        is provided, returns a dictionary of (node_id, formula_set) mappings.

        Parameters
        ----------
        node_id : the ID of the desired node; usually an int

        Examples
        --------
        >>> G = eb.path_graph(4)
        >>> G.add_formula(0, "p & q")
        >>> G.add_formula(1, 'p | ~r')

        Get the formulas at a specific node:

        >>> G.formulas(0)
        set([q & p])

        Get a dictionary showing the formulas at every node:

        >>> G.formulas()
        {0: set([q & p]), 1: set([p | ~r]), 2: set([]), 3: set([])}
        """
        if node_id is not None:
            return self.graph.node[node_id][FORMULAS_KEY]
        else:
            return nx.get_node_attributes(self.graph, FORMULAS_KEY)

    def add_formula(self, node_id, formula):
        """Adds a formula to the set of formulas belonging to a node.

        Parameters
        ----------
        node_id : the ID of the desired node; usually an int
        formula : this can be either a eb.Prop object, or a string 
                  representing a formua in infix notation

        Examples
        --------
        >>> G = eb.EquibelGraph()
        >>> G.add_node(1)

        Create an eb.Prop object and add it as a formula:

        >>> form = eb.Prop('p') & eb.Prop('q')
        >>> G.add_formula(1, form)
        >>> G.formulas(1)

        Add a formula using a string with infix notation:

        >>> G.add_formula(1, "q | ~r")
        >>> G.formulas(1)
        set([q & p, q | ~r])
        """
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

    def set_formulas(self, node_id, formulas):
        self.clear_formulas_from(node_id)
        for formula in formulas:
            self.graph.node[node_id][FORMULAS_KEY].add(formula)

    def clear_formulas_from(self, node_id):
        """Removes all formulas from a node. Thus, resets a node to a 
        blank slate.

        Parameters
        ----------
        node_id : the ID of the desired node; usually an int

        Examples
        --------
        >>> G = eb.EquibelGraph()
        >>> G.add_node(1)
        >>> G.add_formula(1, 'p & q | r')
        >>> G.formulas(1)
        set([(q & p) | r])

        Clear the formulas from node 1:

        >>> G.clear_formulas_from(1)
        >>> G.formulas(1)
        set([])
        """
        self.graph.node[node_id][FORMULAS_KEY].clear()

    def clear_formulas(self):
        """Removes all formulas from all nodes in the graph.

        Examples
        --------
        >>> G = eb.path_graph(4)
        >>> G.add_formula(1, 'p | (q & r)')
        >>> G.add_formula(2, '~p')
        >>> G.add_formula(3, 'q | r')
        >>> G.formulas()
        {0: set([]), 1: set([p | (q & r)]), 2: set([~p]), 3: set([q | r])}

        Now clear all formulas:

        >>> G.clear_formulas()
        >>> G.formulas()
        {0: set([]), 1: set([]), 2: set([]), 3: set([])}
        """
        for node_id in self.nodes():
            self.graph.node[node_id][FORMULAS_KEY].clear()

    def remove_formula(self, node_id, formula):
        """
        """
        self.graph.node[node_id][FORMULAS_KEY].discard(formula)
