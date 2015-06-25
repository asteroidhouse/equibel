Equibel
=======

Introduction
------------

*Note: This project is still under construction. More documentation will
be available soon.*

| Equibel is a toolkit for working with equivalence-based belief change.
| It can be used in two ways:

#. Programmatically, via the **equibel** Python module, or
#. Interactively, via the **equibeli** command-line interface

Currently Supported Platforms
-----------------------------

-  OS X with Python 2.7.x
-  Linux (32-bit & 64-bit) with Python 2.7.x

Installation
------------

| The following steps assume that you have the ``pip`` Python package
  manager
| installed. If you don't have ``pip``, you can get it
  `here <https://pip.pypa.io/en/latest/installing.html>`__.

#. | It is recommended that you install Equibel into a *virtual
     environment*.
   |  To create a virtual environment, you first need to install
     ``virtualenv``:

   ::

       $ pip install virtualenv

#. Then, create a project directory and a virtual environment within it:

   ::

       $ mkdir try_equibel
       $ cd try_equibel
       $ virtualenv venv --python=python2.7

#. Activate the virtual environment:

   ::

       $ source venv/bin/activate

#. Install Equibel using pip:

   ::

       (venv)$ pip install equibel

For more installation details, see the tutorial at
docs/EquibelTutorial.pdf.

Quickstart
----------

Using the Interactive CLI
~~~~~~~~~~~~~~~~~~~~~~~~~

| You can start the interactive CLI by typing **equibeli** in your
  terminal. The
| following is an example interactive session that creates a path graph
  on four
| nodes, adds formulas to the first and last nodes, and performs a
  one-shot belief
| sharing operation:

::

    $ equibeli
    Equibel version 0.8.7 (Alpha)
    equibel (g) > add_nodes [1,2,3,4]

        nodes: [1, 2, 3, 4]

    equibel (g) > add_edges [(1,2), (2,3), (3,4)]

        edges:
            1 <-> 2
            2 <-> 3
            3 <-> 4

    equibel (g) > add_formula 1 p&q&r

        node 1:
            (q & p) & r

    equibel (g) > add_formula 4 ~p&~q

        node 4:
            ~p & ~q

    equibel (g) > formulas

        node 1:
            (q & p) & r
        node 2:
        node 3:
        node 4:
            ~p & ~q

    equibel (g) > one_shot

        One-shot belief change completed:
        ---------------------------------

        node 1:
            q & p & r
        node 2:
            r
        node 3:
            r
        node 4:
            ~p & ~q & r

Using the Python API
~~~~~~~~~~~~~~~~~~~~

| To use Equibel within a Python program, you need to import the
  **equibel**
| module. The following is a script that does the same thing as the
  interactive
| session -- it creates a path graph, assigns formulas to nodes, find
  the
| completion, and prints the resulting formulas at each node:

.. code:: python

    import equibel as eb

    if __name__ == '__main__':
        G = eb.EquibelGraph()

        # Create nodes:
        G.add_nodes([1, 2, 3, 4])

        # Create edges:
        G.add_edges([(1,2), (1,3), (3,4), (2,4)]) 

        # Add formulas to nodes:
        G.add_formula(1, "p & q & r")
        G.add_formula(4, "~p & ~q")

        # Find the completion of the G-scenario:
        R = eb.completion(G)

        # Print the resulting formulas at each node:
        for node_id in R.nodes():
            print("Node {0}: {1}".format(node_id, R.formulas(node_id)))
