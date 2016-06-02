Graph Generators
----------------

Equibel includes a number of functions that *wrap* around NetworkX graph generators; these
functions invoke certain NetworkX functions, and convert the resulting NetworkX ``Graph`` 
objects to ``EquibelGraph`` objects.

Classic Graph Generators
~~~~~~~~~~~~~~~~~~~~~~~~

Equibel includes the following generators for classic graph topologies:

+----------------------+---------------------------+
|    Type of Graph     |    Generator Function     |
+======================+===========================+
|      Path Graph      |    ``eb.path_graph(n)``   |
+----------------------+---------------------------+
|    Complete Graph    | ``eb.complete_graph(n)``  |
+----------------------+---------------------------+
|      Star Graph      |    ``eb.star_graph(n)``   |
+----------------------+---------------------------+

``eb.path_graph(n)`` creates an undirected path graph on ``n`` nodes, numbered using
the integers ``0`` to ``n - 1``, inclusive. The following invocation creates the path graph
0 <-> 1 <-> 2 <-> 3:

.. code:: python

    >>> G = eb.path_graph(4)

We can inspect the nodes and edges in this path graph as follows:

.. code:: python

    >>> G.nodes()
    [0, 1, 2, 3]
    >>> G.edges()
    [(0, 1), (1, 2), (2, 3)]

To create an undirected complete graph on ``n`` nodes, use:

.. code:: python

    >>> G = eb.complete_graph(4)

Again, we inspect the nodes and edges to see what was produced by the generator:

.. code:: python

    >>> G.nodes()
    [0, 1, 2, 3]
    >>> G.edges()
    [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

Following the convention used by NetworkX, the function ``star_graph(n)`` creates an
undirected star graph on ``n + 1`` nodes, with one central node numbered 0, and ``n`` outer nodes
numbered by the integers ``1`` to ``n``, inclusive:

.. code:: python

    >>> G = eb.star_graph(4)

When inspecting the nodes and edges produced by ``star_graph(4)``, note that there are 5 nodes, 
numbered from 0 to 4, inclusive, and that node 0 is the central node of the star gtaph:

.. code:: python

    >>> G.nodes()
    [0, 1, 2, 3, 4]
    >>> G.edges()
    [(0, 1), (0, 2), (0, 3), (0, 4)]

In addition to the graph generators provided with Equibel, you can also use any of the graph
generators included with NetworkX, which are 
`documented here <http://networkx.readthedocs.io/en/networkx-1.11/reference/generators.html>`__, 
via the method described next.
The majority of the generator functions in NetworkX have an optional keyword argument
called ``create_using``, which enables them to return an object of any type that is a subclass of
the NetworkX ``Graph`` class. Thus, if you include the argument ``create_using=EquibelGraph()``
when calling a NetworkX generator function, the output will be an ``EquibelGraph`` object with 
the desired graph topology.

In fact, the graph generators in Equibel are implemented using this method. For example, the 
``eb.star_graph()`` function is equivalent to the following NetworkX call:

.. code:: python

    >>> import networkx as nx
    >>> G = nx.star_graph(5, create_using=EquibelGraph())

Alternatively, you can *initialize* an ``EquibelGraph`` object from an existing ``Graph`` *or* 
``EquibelGraph`` object; this creates a new ``EquibelGraph`` by copying the nodes and edges from
the existing graph. Thus, you can generate any type of (undirected) NetworkX graph and pass it to
the ``EquibelGraph`` constructor as follows:

.. code:: python

    >>> G = EquibelGraph(nx.complete_graph(5))
