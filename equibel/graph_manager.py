"""Manage multiple graphs during an interactive session.

The GraphManager class keeps track of graph objects by 
associating them with names. This makes it easy to manage 
multiple graphs w.r.t switching between them and maintaining 
which is the current interactive context.
"""
#    Copyright (C) 2014-2015 by
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.


class GraphManagerError(Exception):
    pass


class GraphManager:
    """
    The GraphManager class is used to manage multiple
    graphs during an interactive session, and to keep
    track of which graph is the current context for
    commands issued at the prompt.

    Example
    -------
    Create two graphs:

    >>> g = Graph()
    >>> g2 = Graph()

    Create a GraphManager and add the two graphs to it:

    >>> manager = GraphManager()
    >>> manager.add('g', g)
    >>> manager.add('g2', g2)

    Retrieve the name of the current context. Note that
    the first graph added to the manager (graph 'g' above)
    automatically becomes the current context:

    >>> manager.current_context_name
    'g'

    Retrieve the current context graph, perform an operation
    on it to obtain a modified graph, and update the current
    context to reflect the changes:

    >>> context_graph = manager.current_context
    >>> completion_graph = equibel.completion(context_graph)
    >>> manager.update_context(completion_graph)
    """
    def __init__(self):
        self.graphs = dict()
        self.current_context = None
        self.current_context_name = None


    def __iter__(self):
        """
        Returns an iterator over the graphs.
        """
        return iter(self.graphs)


    def __getitem__(self, key):
        """
        Finds a graph by name. If the graph is not in
        the graph manager, returns None.

        Example
        -------
        >>> g2 = Graph()
        >>> manager = GraphManager()
        >>> manager.add('g2', g2)

        At any time, the graph can be accessed by:

        >>> manager['g2']
        """
        return self.graphs.get(key, None)


    def add(self, graph_name, graph):
        """
        Adds a graph object to this manager. The given
        graph name is used as the key to access the graph
        object later.

        Example
        -------
        Create a graph and a manager, and add the graph to
        the manager:

        >>> g2 = Graph()
        >>> manager = GraphManager()
        >>> manager.add('g2', g2)
        """
        self.graphs[graph_name] = graph
        # The first graph added to the manager becomes the
        # current context automatically.
        if not self.current_context:
            self.current_context = graph
            self.current_context_name = graph_name


    def update_context(self, graph):
        """
        Overwrites the graph in the current context with
        the given graph (to reflect changes to the context).
        That is, this associates the current context name
        with a new graph.

        Example
        -------
        >>> manager = GraphManager()
        >>> manager.add('g', Graph())

        Retrieve graph 'g' and perform an operation on it,
        creating a new graph:

        >>> working_graph = manager['g']
        >>> updated_graph = equibel.completion(working_graph)

        Update the context, associating the name 'g' with
        the updated_graph, and losing the reference to the
        working_graph:

        >>> manager.update_context(updated_graph)
        """
        self.graphs[self.current_context_name] = graph
        self.current_context = graph


    def remove(self, graph_name):
        """
        Removes a graph from the graph manager. Note that
        if the manager contains the only reference to the
        graph in question, then the graph will be lost.

        Example
        -------
        >>> manager.remove('g2')
        """
        if graph_name not in self.graphs:
            raise GraphManagerError("Graph \"{0}\" does not exist".format(graph_name))
        del self.graphs[graph_name]


    def set_context(self, graph_name):
        """
        Sets the current context to the graph identified by
        the given name.

        Example
        -------
        >>> manager = GraphManager()
        >>> manager.add('g', Graph())
        >>> manager.add('g2', Graph())
        >>> manager.current_context_name
        'g'
        >>> manager.set_context('g2')
        >>> manager.current_context_name
        'g2'
        """
        if graph_name not in self.graphs:
            raise GraphManagerError("Graph \"{0}\" does not exist".format(graph_name))
        self.current_context = self.graphs[graph_name]
        self.current_context_name = graph_name
