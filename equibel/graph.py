"""The EquibelGraph class represents a graph $G$ together with an associated 
$G$-scenario $\sigma$. It extends the NetworkX ``Graph`` class and adds the 
ability to associate propositional formulas with nodes. Such formulas are 
represented using Sympy formula objects, from the ``logic`` module of the 
Sympy package for symbolic mathematics.
"""
#    Copyright (C) 2016
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.

from sympy.logic.boolalg import simplify_logic, true

import copy

import networkx as nx
import equibel as eb


class EquibelGraphException(Exception):
    pass


class EquibelGraph(nx.Graph):
    def __init__(self, data=None, **attr):
        nx.Graph.__init__(self, data, **attr)
    

    def __eq__(self, other):
        """Tests this graph for equality with ``other``. Two graphs are equal
        if they contain the same nodes, edges, and formulas at each node.

        This operation can be expensive, since it check whether formulas are 
        equivalent by first simplifying the formulas, and then testing the 
        simplified representations for equivalence.

        Parameters
        ----------
        other : An object to test for equality with the current Graph

        Returns
        -------
        ``True`` if ``self`` and ``other`` represent the same graph and scenario; 
        ``False`` otherwise.

        Examples
        --------
        Create the first graph:

        >>> G1 = eb.path_graph(4)
        >>> G1.add_formula(0, 'p & q')
        >>> G1.add_formula(1, 'q | r')

        Create the second graph:

        >>> G2 = eb.path_graph(4)
        >>> G2.add_formula(0, 'p & q')

        These graphs are not equal:

        >>> G1 == G2
        False

        But we can add a formula to G2 to make it equal to G1:

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
        for node in self.nodes():
            try:
                if not simplify_logic(self.formula_conj(node)).equals(simplify_logic(other.formula_conj(node))):
                    return False
            except Exception:
                return False
        return True


    def __ne__(self, other):
        """Tests for non-equality. Negates the result of equality testing."""
        return not self.__eq__(other)


    def copy(self):
        """Creates a deep copy of this graph.

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



    def add_formula(self, node_id, formula):
        """Adds a formula to the set of formulas associated with a node.

        Parameters
        ----------
        node_id : The identifier of the desired node (usually an int)
        formula : This can be either a *Sympy formula object*, or a *string*
                  representing a formua in infix notation

        Examples
        --------
        >>> G = eb.EquibelGraph()
        >>> G.add_node(1)

        Create a Sympy formula object and associate it with node 1:

        >>> form = eb.parse_formula('p & q')
        >>> G.add_formula(1, form)
        >>> G.formulas(1)
        set([And(p, q)])

        Add a formula using a formula string expressed in infix notation:

        >>> G.add_formula(1, 'q | ~r')
        >>> G.formulas(1)
        set([Or(Not(r), q), And(p, q)])
        """
        if node_id not in self.nodes():
            raise EquibelGraphException("Node {} does not exist.".format(node_id))
        
        if isinstance(formula, str):
            formula = eb.parse_formula(formula)
        
        if 'formulas' not in self.node[node_id]:
            self.node[node_id]['formulas'] = set([formula])
        else:
            self.node[node_id]['formulas'].add(formula)
    

    def formulas(self, node_id=None):
        """Returns the set of formulas associated with ``node_id``, or, 
        if ``node_id`` is ``None``, returns a dictionary of 
        (``node_id``, ``formula_set``) mappings.

        Parameters
        ----------
        node_id : The identifier of the desired node (usually an integer)

        Examples
        --------
        >>> G = eb.path_graph(4)
        >>> G.add_formula(0, 'p & q')
        >>> G.add_formula(1, 'p | ~r')

        Get the formulas at a specific node:

        >>> G.formulas(0)
        set([And(p, q)])

        Get a dictionary showing the formulas at every node:

        >>> G.formulas()
        {0: set([And(p, q)]), 1: set([Or(Not(r), p)]), 2: set([]), 3: set([])}
        """
        if node_id is not None:
            if node_id not in self.nodes():
                raise EquibelGraphException("Node {} does not exist.".format(node_id))
            return self.node[node_id].get('formulas', set())
        else:
            return { node: self.node[node].get('formulas', set()) for node in self }
            #return nx.get_node_attributes(self, 'formulas')
    

    def formula_conj(self, node_id):
        """Returns the conjunction of all formulas associated with a given node.

        Parameters
        ----------
        node_id : The identifier of the desired node (usually an int)

        Example
        -------
        >>> G = eb.EquibelGraph()
        >>> G.add_node(1)
        >>> G.add_formula(1, 'p & q')
        >>> G.add_formula(1, 'r -> s')
        >>> G.formula_conj(1)
        And(Implies(r, s), p, q)
        """
        f = true
        for formula in self.formulas(node_id):
            f &= formula
        return f


    def clear_formulas_from(self, node_id):
        """Removes all formulas from a node. Thus, resets a node to a blank slate.

        Parameters
        ----------
        node_id : The identifier of the desired node (usually an int)

        Examples
        --------
        >>> G = eb.EquibelGraph()
        >>> G.add_node(1)
        >>> G.add_formula(1, 'p & q | r')
        >>> G.formulas(1)
        set([Or(And(p, q), r)])

        Clear the formulas from node 1:

        >>> G.clear_formulas_from(1)
        >>> G.formulas(1)
        set([])
        """
        if node_id not in self.nodes():
            raise EquibelGraphException("Node {} does not exist.".format(node_id))
        self.node[node_id].get('formulas', set()).clear()


    def clear_formulas(self):
        """Removes all formulas from all nodes in the graph.

        Examples
        --------
        >>> G = eb.path_graph(4)
        >>> G.add_formula(1, 'p | (q & r)')
        >>> G.add_formula(2, '~p')
        >>> G.add_formula(3, 'q | r')
        >>> G.formulas()
        {1: set([Or(And(q, r), p)]), 2: set([Not(p)]), 3: set([Or(q, r)])}

        Now clear all formulas:

        >>> G.clear_formulas()
        >>> G.formulas()
        {0: set([]), 1: set([]), 2: set([]), 3: set([])}
        """
        for node_id in self.nodes():
            self.clear_formulas_from(node_id)


    def atoms(self, node_id=None):
        """Returns either the set of atoms used by a specific node in the graph, or 
        the set of all atoms used by *any* node in the graph.

        If ``node_id`` is not ``None``, then this function returns the set of 
        atoms used by the formula at ``node_id``; if ``node_id`` is ``None``, then 
        this function returns the set of all atoms used by formulas of *any* node 
        in the graph.

        Parameters
        ----------
        node_id : The identifier of the desired node (usually an int)

        Examples
        --------
        >>> G = eb.path_graph(2)
        >>> G.add_formula(0, 'p -> q')
        >>> G.add_formula(1, 'q | ~r')
        >>> G.atoms(0)
        set([p, q])
        >>> G.atoms(1)
        set([r, q])
        >>> G.atoms()
        set([p, r, q])
        """
        if node_id is not None:
            return self.formula_conj(node_id).atoms()
        else:
            return set.union(*[self.atoms(node_id) for node_id in self])


    #####################################################
    ###            CONVENIENCE METHODS                ###
    #####################################################

    def to_asp(self, atoms=None):
        """Returns the ASP encoding of this EquibelGraph object.

        Parameters
        ----------
        atoms : An iterable container of Sympy atoms 

        Example
        -------
        >>> G = eb.complete_graph(3)
        >>> G.add_formula(0, 'p & q')
        >>> G.add_formula(1, '~q | r')
        >>> G.add_formula(2, 'p -> ~r')
        >>> print(G.to_asp())
        node(0).
        node(1).
        node(2).
        edge(0,1).
        edge(1,0).
        edge(0,2).
        edge(2,0).
        edge(1,2).
        edge(2,1).
        formula(0,and(p,q)).
        formula(1,or(r,neg(q))).
        formula(2,implies(p,neg(r))).
        atom(p).
        atom(r).
        atom(q).
        """
        return eb.to_asp(self, atoms)
