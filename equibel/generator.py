"""Equibel wrappers for networkx graph generator functions.

This file contains wrapper functions for several networkx graph 
generators. The wrappers return EquibelGraph objects that contain 
the corresponding networkx graphs.
"""
#    Copyright (C) 2014-2015 by
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.
from __future__ import absolute_import
from __future__ import print_function

import sys

import networkx as nx

from equibel.graph import EquibelGraph


# ======================================================
# 
# Classic Graph Generators -- Line, Star, Complete, etc.
# 
# ======================================================

def path_graph(n, directed=False):
    """Create a directed or undirected line graph on n nodes, 
    numbered using the integers 0 to n-1, inclusive.

    Parameters
    ----------
    n        : int
               The desired number of nodes for the line graph.
    directed : boolean
               If set to True, then the edges of the line graph 
               will be directed in order of increasing node number.

    Returns
    -------
    G : EquibelGraph
        An EquibelGraph representing a line graph.

    Examples
    --------
    Create an undirected line graph 0 <-> 1 <-> 2 <-> 3:

    >>> G = line_graph(4)

    Create a directed line graph 0 -> 1 -> 2 -> 3:
    
    >>> D = line_graph(4, directed=True)
    """
    if directed:
        return EquibelGraph(nx.path_graph(n, create_using=nx.DiGraph()))
    else:
        return EquibelGraph(nx.path_graph(n))

def complete_graph(n):
    """Create an undirected complete graph on n nodes.

    Parameters
    ----------
    n : int
        The desired number of nodes for the complete graph.

    Returns
    -------
    G : EquibelGraph
        An EquibelGraph containing a complete graph on n nodes.

    Examples
    --------
    >>> G = complete_graph(5)
    """
    return EquibelGraph(nx.complete_graph(n))

def star_graph(n):
    """Create an undirected star graph on n+1 nodes, with one 
    central node, and n outer nodes.

    Parameters
    ----------
    n : int
        The desired number of outer nodes for the star graph.
        The generated graph will have a central node numbered 
        0, and n outer nodes numbered from 1 to n.

    Returns
    -------
    G : EquibelGraph
        An EquibelGraph containing a star graph on n+1 nodes.

    Examples
    --------
    >>> G = star_graph(5)
    """
    return EquibelGraph(nx.star_graph(n))


# ========================================================
# 
# Random Graph Generators -- Waxman, Barabasi-Albert, etc.
# 
# ========================================================

def waxman_graph(n, alpha=0.4, beta=0.1, L=None, domain=(0,0,1,1)):
    """
    """
    return EquibelGraph(nx.waxman_graph(n, alpha, beta, L, domain))

def erdos_renyi_graph(n, p, seed=None, directed=False):
    """
    """
    return EquibelGraph(nx.erdos_renyi_graph(n, p, seed, directed))
