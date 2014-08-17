class Node:
     def __init__(self, num):
          self.num = num
          self.weights = dict()
          self.formulas = set()

     def add_atom(self, atom_name, weight=1):
          if atom_name not in self.weights:
               self.weights[atom_name] = weight

     def remove_atom(self, atom_name):
          if atom_name in self.weights:
               del self.weights[atom_name]
     

     def add_weight(self, atom_name, weight):
          self.weights[atom_name] = weight

     # Resets the weight to the default (in this case, 1)
     def remove_weight(self, atom_name):
          if atom_name in self.weights:
               self.weights[atom_name] = 1 


     def add_formula(self, formula):
          self.formulas.add(formula)

     def remove_formula(self, formula):
          self.formulas.discard(formula)
