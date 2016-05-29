"""Equibel wrappers for NetworkX graph generator functions.

This file contains wrapper functions for several networkx graph 
generators. The wrappers return EquibelGraph objects that contain 
the corresponding NetworkX graphs.
"""
#    Copyright (C) 2016
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.
from __future__ import absolute_import

import networkx as nx

from equibel.graph import EquibelGraph


##############################################################
### Classic Graph Generators -- Line, Star, Complete, etc. ###
##############################################################

def path_graph(n):
    """Create an undirected line graph on n nodes, numbered using 
    the integers 0 to n-1, inclusive.

    Parameters
    ----------
    n : The desired number of nodes for the line graph.

    Returns
    -------
    G : An ``EquibelGraph`` representing a path graph on ``n`` nodes.

    Examples
    --------
    Create an undirected path graph 0 <-> 1 <-> 2 <-> 3:

    >>> G = eb.path_graph(4)
    """
    return nx.path_graph(n, create_using=EquibelGraph())


def complete_graph(n):
    """Create an undirected complete graph on n nodes.

    Parameters
    ----------
    n : The desired number of nodes for the complete graph.

    Returns
    -------
    G : An ``EquibelGraph`` containing a complete graph on ``n`` nodes.

    Examples
    --------
    >>> G = eb.complete_graph(5)
    """
    return nx.complete_graph(n, create_using=EquibelGraph())


def star_graph(n):
    """Create an undirected star graph on n+1 nodes, with one 
    central node, and n outer nodes.

    Parameters
    ----------
    n : The desired number of outer nodes for the star graph.
        The generated graph will have a central node numbered 
        ``0``, and ``n`` outer nodes numbered from ``1`` to ``n``.

    Returns
    -------
    G : An ``EquibelGraph`` containing a star graph on ``n+1`` nodes.

    Examples
    --------
    >>> G = eb.star_graph(5)
    """
    return nx.star_graph(n, create_using=EquibelGraph())


################################################################
### Random Graph Generators -- Waxman, Barabasi-Albert, etc. ###
################################################################

def waxman_graph(n, alpha=0.4, beta=0.1, L=None, domain=(0,0,1,1)):
    return EquibelGraph(nx.waxman_graph(n, alpha, beta, L, domain))

def erdos_renyi_graph(n, p, seed=None, directed=False):
    return EquibelGraph(nx.erdos_renyi_graph(n, p, seed, directed))

def gnm_random_graph(n, m, seed=None, directed=False):
    return EquibelGraph(nx.gnm_random_graph(n, m, seed=None, directed=False))

def petersen_graph():
    return EquibelGraph(nx.petersen_graph())

def connected_watts_strogatz_graph(n=10, k=4, p=0.5, tries=100, seed=None):
    return EquibelGraph(nx.connected_watts_strogatz_graph(n,k,p,tries,seed))
