Working with Graphs and Scenarios
---------------------------------

The primary data structure used in Equibel is a class called ``EquibelGraph``. An ``EquibelGraph`` object 
represents a graph and an associated scenario. Each approach to belief change in
Equibel takes as input an ``EquibelGraph``, and produces a new ``EquibelGraph`` as output.

The ``EquibelGraph`` class is a subclass of the NetworkX `undirected Graph class <http://networkx.readthedocs.io/en/networkx-1.11/reference/classes.html>`__, 
so it inherits all of the methods of ``Graph``. In addition, ``EquibelGraph`` extends the standard ``Graph`` 
functionality by adding the ability to associate propositional formulas with nodes.

In this section, we describe the API used by ``EquibelGraph`` through examples.

Creating a Graph
~~~~~~~~~~~~~~~~

Create an empty graph and scenario, with no nodes and no edges:

.. code:: python

    >>> import equibel as eb
    >>> G = eb.EquibelGraph()

Nodes
~~~~~

All the methods for manipulating nodes in a graph are inherited from the NetworkX ``Graph`` class;
these methods are summarized here.

Individual nodes can be added via the method ``add_node()``:

.. code:: python

    >>> G.add_node(1)

Multiple nodes can be added simultaneously via the method ``add_nodes_from()``, which adds all
nodes from an iterable container (a ``list``, ``set``, etc.):

.. code:: python

    >>> G.add_nodes_from([2,3,4])

You can see which nodes are currently in the graph by calling the
``nodes()`` method:

.. code:: python

    >>> G.nodes()
    [1,2,3,4]

The ``remove_node()`` and ``remove_nodes_from()`` methods similarly remove an individual node and
all nodes from an iterable container, respectively:

.. code:: python

    >>> G.remove_node(2)
    >>> G.nodes()
    [1, 3, 4]

.. code:: python

    >>> G.remove_nodes_from([3,4])
    >>> G.nodes()
    [1]

Edges
~~~~~

As with nodes, edges can be added individually:

.. code:: python

    >>> G.add_edge(1,2)

Or multiple edges from an iterable container can be added simultaneously:

.. code:: python

    >>> G.add_edges_from([(1,2), (2,3), (3,4)])

You can see which edges are currently in the graph by calling the ``edges()`` method:

.. code:: python

    >>> G.edges()
    [(1,2), (2,3), (3,4)]

Edges can be removed individually or in groups by the ``remove_edge()`` and ``remove_edges_from()``
methods, respectively:

.. code:: python

    >>> G.remove_edge(3,4)
    >>> G.edges()
    [(1,2), (2,3)]

.. code:: python

    >>> G.remove_edges_from([(1,2), (2,3)])
    >>> G.edges()
    []

Note that removing edges does not affect the nodes in the graph:

.. code:: python

    >>> G.nodes()
    [1, 2, 3, 4]

You can also add an edge whose endpoints are *not* in the graph; in this case, the
endpoints will be automatically added as nodes:

.. code:: python

    >>> G = eb.EquibelGraph()
    >>> G.nodes()
    []
    >>> G.edges()
    []
    >>> G.add_edge(1,2) # Endpoints 1 and 2 are automatically added as nodes
    >>> G.nodes()
    [1, 2]

Working with Formulas
~~~~~~~~~~~~~~~~~~~~~

Each node in an ``EquibelGraph`` is associatd with a set of formulas, where each formula is
represented by a Sympy formula object. By default, a node is associated with an empty
set of formulas.

The ``add_formula()`` method adds a formula to the set of formulas associated with a node.
The argument to ``add_formula()`` can be either a *Sympy formula object*, or a *string*
representing a formula in infix notation.

The following line creates a graph by invoking a *graph generator* (described in more detail in 
the Graph Generators section):

.. code:: python

    >>> G = eb.path_graph(3) # Creates a path graph on nodes [0, 1, 2]

The following creates a Sympy formula object by parsing a string via the Equibel ``parse_formula`` function,
and associates it with node 1:

.. code:: python

    >>> formula_object = eb.parse_formula('p & q')
    >>> G.add_formula(0, formula_object)
    >>> G.formulas(0)
    set([And(p, q)])

Alternatively, one can simply pass a formula string to the ``add_formula()`` method, and it will
be automatically parsed as above:

.. code:: python

    >>> G.add_formula(0, 'q | ~r')
    >>> G.formulas(0)
    set([Or(Not(r), q), And(p, q)])

Formula strings use the following notation for logical connectives:

+--------------+------------------+
|  Connective  | Equibel Notation |
+==============+==================+
|   negation   |       ``~``      |
+--------------+------------------+
|  conjunction |       ``&``      |
+--------------+------------------+
|  disjunction |       ``|``      |
+--------------+------------------+
|  implication |      ``->``      |
+--------------+------------------+
|  equivalence |       ``=``      |
+--------------+------------------+

The precedence and right/left associativity rules of the conectives are as follows:

#. Negation has the highest precendence, and is right-associative.
#. Conjunction has the next highest precedence, and is left-associative.
#. Disjunction is next, is left-associative.
#. Implication comes next, and is right-associative.
#. Finally, equivalence is last, and is right-associative.

Parentheses can also be used for grouping, or to overwrite the default precedence rules.
With the default rules, the following formulas are equivalent:

-  ``p & q | r   ==   (p & q) | r``
-  ``p & q -> r   ==   (p & q) -> r``
-  ``p | ~r = q   ==   (p | (~r)) = q``
-  ``~p | ~q & r   ==   ((~p) | (~q)) & r``

In order to obtain the set of formulas associated with a node, use the ``formulas()`` method,
passing the node as an argument:

.. code:: python

    >>> G.formulas(0)
    set([Or(Not(r), q), And(p, q)])

Calling ``formulas()`` with no arguments yields a *dictionary* that maps each node in the graph
to a set of formulas:

.. code:: python

    >>> G.formulas()
    {0: set([Or(Not(r), q), And(p, q)]), 1: set([]), 2: set([])}
    >>> G.add_formula(1, 'p | q')
    >>> G.formulas()
    {0: set([Or(Not(r), q), And(p, q)]), 1: set([Or(p, q)]), 2: set([])}
    >>> G.add_formula(2, 'p -> q')
    >>> G.formulas()
    {0: set([Or(Not(r), q), And(p, q)]), 1: set([Or(p, q)]), 2: set([Implies(p, q)])}

The ``formula_conj()`` method returns the *conjunction* of all formulas associated with a
given node. This is handy because it is often useful to obtain a single formula representing the
information at a node, rather than a set of formulas.

.. code:: python

    >>> G.formula_conj(0)
    And(Implies(r, s), p, q)

To clear all formulas from a node, use ``clear_formulas_form()`` as follows:

.. code:: python

    >>> G.clear_formulas_from(0)
    >>> G.formulas()
    {0: set([]), 1: set([Or(p, q)]), 2: set([Implies(p, q)])}

To clear all formulas from *all nodes in the graph*, use ``clear_formulas()``:

.. code:: python

    >>> G.clear_formulas()
    >>> G.formulas()
    {0: set([]), 1: set([]), 2: set([])}

The ``atoms()`` method returns the set of atoms used by a specific node in the graph:

.. code:: python

    >>> G = eb.path_graph(2)
    >>> G.add_formula(0, 'p -> q')
    >>> G.add_formula(1, 'q | ~r')
    >>> G.atoms(0)
    set([p, q])
    >>> G.atoms(1)
    set([r, q])

Alternatively, if ``atoms()`` is called without any arguments, it returns the set of atoms
that appear in *any* formula of *any* node in the graph:

.. code:: python

    >>> G.atoms()
    set([p, r, q])

Equality Testing
~~~~~~~~~~~~~~~~

``EquibelGraph`` objects can be tested for equality via the ``==`` operator.
Two graphs are *equal* if they contain the same nodes, edges, *and formulas at each node*.

Equality testing can be expensive, since it checks whether formulas are equivalent by first
simplifying the formulas, and then testing the simplified representations for equivalence.
That is, it performs *semantic* equivalence checks for formulas, rather than *syntactic* checks.

We now present an example of this. We create the first graph as follows:

.. code:: python

    >>> G1 = eb.path_graph(4)
    >>> G1.add_formula(0, 'p & q')
    >>> G1.add_formula(1, 'q | r')

Then, we create the second graph:

.. code:: python

    >>> G2 = eb.path_graph(4)
    >>> G2.add_formula(0, 'p & q')

These graphs are not equal:

.. code:: python

    >>> G1 == G2
    False

But we can add a formula to G2 to make it equal to G1:

.. code:: python

    >>> G2.add_formula(1, 'q | r')
    >>> G1 == G2
    True

Convenience Methods
~~~~~~~~~~~~~~~~~~~

You can obtain the Answer Set Programming (ASP) representation of an ``EquibelGraph`` by calling the
``to_asp()`` convenience method:

.. code:: python

    >>> G = eb.path_graph(3)
    >>> G.add_formula(0, 'p')
    >>> G.add_formula(1, 'p -> (q & r)')
    >>> G.add_formula(2, '~p | ~r')
    >>> print(G.to_asp())
    node(0).
    node(1).
    node(2).
    edge(0,1).
    edge(1,0).
    edge(1,2).
    edge(2,1).
    formula(0,p).
    formula(1,implies(p,and(q,r))).
    formula(2,or(neg(p),neg(r))).
    atom(p).
    atom(r).
    atom(q).

Note that ``G.to_asp()`` is shorthand for ``eb.to_asp(G)``.
