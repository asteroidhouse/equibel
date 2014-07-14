class Node:
	def __init__(self, num):
		self.__num = num
		self.__atom_weights = {}
		self.__formulas = []
	
	def __repr__(self):
		return "Node({0})".format(self.__num)
	
	@property
	def num(self):
		return self.__num
	
	@num.setter
	def num(self, new_num):
		if new_num >= 0:
			self.__num = new_num
	
	def add_atom(self, atom):
		if atom not in self.__atom_weights:
			self.__atom_weights[atom] = 1

	def set_atom_weight(self, atom, weight):
		self.__atom_weights[atom] = weight
	
	@property
	def atoms(self):
		return self.__atom_weights
	
	def add_formula(self, formula):
		if formula not in self.__formulas:
			self.__formulas.append(formula)
	
	def remove_formula(self, formula):
		if formula in self.__formulas:
			del self.__formulas[self.__formulas.index(formula)]

	@property
	def formulas(self):
		return self.__formulas


def formulas(node):
	return node.formulas

def atoms(node):
	return node.atoms
