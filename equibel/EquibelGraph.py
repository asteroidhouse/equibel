import networkx as nx

ATOMS_KEY    = "atoms"
WEIGHTS_KEY  = "weights"
FORMULAS_KEY = "formulas"


class EquibelGraph:

    def __init__(self):
        self.graph = nx.Graph()
        self.graph.graph[ATOMS_KEY] = set()

    # ================================================
    #                NODE METHODS
    # ================================================

    # ROUTING to G.nodes()
    def nodes(self):
        return self.graph.nodes()

    def add_node(self, node_id):
        self.graph.add_node(node_id)
        self.graph.node[node_id][WEIGHTS_KEY]  = dict()
        self.graph.node[node_id][FORMULAS_KEY] = set()
        self.__add_atoms_to_new_node(node_id)

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def remove_node(self, node_id):
        self.graph.remove_node(node_id)

    # Perhaps this could be called "remove_nodes"
    def remove_nodes_from(self, nodes):
        self.graph.remove_nodes_from(nodes)

    # ================================================
    #                 EDGE METHODS
    # ================================================

    # ROUTING to G.edges()
    def edges(self):
        return self.graph.edges()

    def add_edge(self, from_node_id, to_node_id):
        if from_node_id not in self.graph:
            self.add_node(from_node_id)
        if to_node_id not in self.graph:
            self.add_node(to_node_id)

        self.graph.add_edge(from_node_id, to_node_id)

    def add_edges(self, edges):
        for (from_node_id, to_node_id) in edges:
            self.add_edge(from_node_id, to_node_id)

    def remove_edge(self, from_node_id, to_node_id):
        self.graph.remove_edge(from_node_id, to_node_id)

    # ROUTING to G.to_directed()
    def to_directed(self):
        self.graph.to_directed()

    # ROUTING to G.to_undirected()
    def to_undirected(self):
        self.graph.to_undirected()

    # ROUTING to G.is_directed()
    def is_directed(self):
        return self.graph.is_directed()

    # ================================================
    #             ATOM and WEIGHT METHODS
    # ================================================

    # Instead of G.graph[ATOMS_KEY], use G.atoms()
    def atoms(self):
        return self.graph.graph[ATOMS_KEY]

    # Instead of G.node[node_id][WEIGHTS_KEY], use G.atom_weights(node_id)
    def atom_weights(self, node_id):
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
        if node_id not in self.nodes():
            for atom in self.atoms():
                self.set_atom_weight(node_id, atom, 1)

    def set_atom_weight(self, node_id, atom, weight):
        self.graph.node[node_id][WEIGHTS_KEY][atom] = weight
        if atom not in self.atoms():
            self.add_atom(atom)

    # For convenience:
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
        self.graph.node[node_id][FORMULAS_KEY].add(formula)
        self.__add_formula_atoms(formula)

    def __add_formula_atoms(self, formula):
        for atom in formula.get_atoms():
            if atom not in self.atoms():
                self.add_atom(atom)

    def remove_formula(self, node_id, formula):
        self.graph.node[node_id][FORMULAS_KEY].discard(formula)
