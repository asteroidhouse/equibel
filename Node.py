class Node:
     def __init__(self, num):
          self.num = num
          self.weights = dict()
          self.formulas = set()

     def add_formula(self, formula):
          self.formulas.add(formula)

     def remove_formula(self, formula):
          self.formulas.discard(formula)

     def add_atom(self, atom, weight=1):
          self.weights[atom] = weight

     def remove_atom(self, atom):
          if atom in self.weights:
               del self.weights[atom]

     def set_atom_weight(self, atom, weight=1):
          self.weights[atom] = weight


     def __repr__(self):
          return "Node({0})".format(self.num)


     def __str__(self):
          result_str = "Node {0}:\n".format(self.num)
          
          if self.weights:
               result_str += "\tAtoms\n"
               result_str += "\t------------------------------\n"
               for atom in self.weights:
                    weight = self.weights[atom]
                    result_str += "\t{0}: {1}\n".format(atom, weight)
          
          if self.formulas:
               result_str += "\n\tFormulas\n"
               result_str += "\t------------------------------\n"
               for formula in self.formulas:
                    result_str += "\t{0}\n".format(formula)

          return result_str
