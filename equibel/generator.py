"""Equibel wrappers for networkx graph generator functions.

This file contains wrapper functions for several networkx graph 
generators. The wrappers return EquibelGraph objects that contain 
the corresponding networkx graphs.
"""
#    Copyright (C) 2014-2015 by
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    BSD license.
from __future__ import absolute_import
from __future__ import print_function

import networkx as nx
import sys
print sys.path
from equibel.EquibelGraph import EquibelGraph

def line_graph(n, directed=False):
	"""Create a directed or undirected line graph on n nodes, 
	numbered using the integers 1 to n, inclusive.

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
    Create an undirected line graph 1 <-> 2 <-> 3 <-> 4:
    >>> G = line_graph(4)

    Create a directed line graph 1 -> 2 -> 3 -> 4:
    >>> D = line_graph(4, directed=True)
    """
    if directed:
    	return EquibelGraph(nx.line_graph(n, create_using=nx.DiGraph()))
    else:
		return EquibelGraph(nx.line_graph(n))

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
	"""Create an undirected star graph on n nodes.
	"""
    return EquibelGraph(nx.star_graph(n))

