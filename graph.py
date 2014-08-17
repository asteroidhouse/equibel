from node import Node

class GraphError(Exception): pass

# DONE: Keep track of the atoms in use at the graph level, not just 
#       at the level of individual nodes. This is needed so that 
#       when a new node is added, it can be "loaded up" with the 
#       atoms that are in the common alphabet. So, the add_node
#       function and such MAY need to be changed.
class Graph:
     def __init__(self):
          self.nodes = dict()
          self.edges = set()
          self.atoms = set()
          self.directed = True

     #------------------------------------------------------------------------
     # Node Functions
     #------------------------------------------------------------------------

     def get_nodes(self):
          return sorted(self.nodes.keys())

     def add_node(self, node_num):
          if node_num not in self.nodes:
               new_node = Node(node_num)
               # Loads the new node with the atoms in the common alphabet.
               for atom in self.atoms:
                    new_node.add_atom(atom)
               self.nodes[node_num] = new_node

     def add_nodes(self, node_nums):
          for node_num in node_nums:
               self.add_node(node_num)

     def remove_node(self, node_num):
          if node_num in self.nodes:
               del self.nodes[node_num]
               self.__remove_associated_edges(node_num)

     def remove_nodes(self, node_nums):
          for node_num in node_nums:
               self.remove_node(node_num)

     # DONE: This method of removing edges works.
     def __remove_associated_edges(self, node_num):
          self.edges = {(start, end) for (start, end) in self.edges if start != node_num and end != node_num}


     #------------------------------------------------------------------------
     # Edge Functions
     #------------------------------------------------------------------------
          
     def get_edges(self):
          return sorted(self.edges)

     # TODO: Check how the start and end points should be passed 
     #       to the function--as separate points, or as a tuple?
     #       Changed it to a tuple, so "edge" is i.e. (1,2)
     def add_edge(self, edge):
          # TODO: Do some better error checking here to make sure that the endpoints exist.
          start_node, end_node = edge
          if start_node in self.nodes and end_node in self.nodes:
               self.edges.add(edge)
          elif start_node not in self.nodes:
               raise GraphError("Can't create edge: node {0} does not exist".format(start_node))
          else:
               raise GraphError("Can't create edge: node {0} does not exist".format(end_node))

     def add_edges(self, edge_list):
          for edge in edge_list:
               self.add_edge(edge)

     def remove_edge(self, edge):
          self.edges.discard(edge)

     def remove_edges(self, edges):
          for edge in edges:
               self.remove_edge(edge)


     #------------------------------------------------------------------------
     # Formula Functions
     #------------------------------------------------------------------------

     def get_formulas(self, node_num):
          if node_num not in self.nodes:
               raise GraphError("node {0} does not exist".format(node_num))
          return self.nodes[node_num].formulas

     # TODO: Think about where to parse the formula. -> NOT HERE
     def add_formula(self, node_num, formula):
          if node_num not in self.nodes:
               raise GraphError("node {0} does not exist".format(node_num))
          self.nodes[node_num].add_formula(formula)

          # Extracts the atoms used in the formula, and adds them to the 
          # common alphabet of the graph and each node in the graph.
          formula_atoms = formula.get_atoms()
          self.add_atoms(formula_atoms)
     

     # DONE: We are working with formulas here, not formula strings.
     def add_formulas(self, formulas):
          if node_num not in self.nodes:
               raise GraphError("node {0} does not exist".format(node_num))
          for formula in formulas:
               self.add_formula(node_num, formula)


     def remove_formula(self, node_num, formula):
          if node_num not in self.nodes:
               raise GraphError("node {0} does not exist".format(node_num))
          self.nodes[node_num].remove_formula(formula)


     def remove_formulas(self, node_num, formula_strs):
          if node_num not in self.nodes:
               raise GraphError("node {0} does not exist".format(node_num))
          for formula_str in formula_strs:
               self.remove_formula(node_num, formula_str)


     #------------------------------------------------------------------------
     # Atom Functions
     #------------------------------------------------------------------------

     def add_atom(self, atom_name):
          self.atoms.add(atom_name)
          for node in self.nodes.values():
               node.add_atom(atom_name)

     def add_atoms(self, atom_list):
          for atom in atom_list:
               self.add_atom(atom)

     def remove_atom(self, atom_name):
          self.atoms.discard(atom_name)
          for node in self.nodes.values():
               node.remove_atom(atom_name)
     
     def get_atoms(self):
          return list(self.atoms)

     
     #------------------------------------------------------------------------
     # Weight Functions
     #------------------------------------------------------------------------

     def get_weights(self, node_num):
          if node_num not in self.nodes:
               raise GraphError("node {0} does not exist".format(node_num))
          return self.nodes[node_num].weights

     # DONE: When a weight is added to one node for an atom that doesn't 
     #       exist in the common alphabet, that atom name should be entered 
     #       into the common alphabet, and all other nodes should be given 
     #       the default weight for that node.
     def add_weight(self, node_num, atom_name, weight):
          if node_num not in self.nodes:
               raise GraphError("node {0} does not exist".format(node_num))
          self.nodes[node_num].add_weight(atom_name, weight)

          # Add the atom with weight 1 to all other nodes, if it is new.
          if atom_name not in self.atoms:
               self.add_atom(atom_name)
          
     # DONE: Either set_weight or add_weight can be defined in terms of the
     #       other, since the functionality is identical.
     def set_weight(self, node_num, atom_name, weight):
          self.add_weight(node_num, atom_name, weight)
     
     def remove_weight(self, node_num, atom_name):
          if node_num not in self.nodes:
               raise GraphError("node {0} does not exist".format(node_num))
          self.nodes[node_num].remove_weight(atom_name)

