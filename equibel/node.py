class Node:
    def __init__(self, num):
        self.num = num
        self.weights = dict()
        self.formulas = set()

    def get_atoms(self):
        return sorted(self.weights.keys())

    def add_atom(self, atom_name, weight=1):
        if atom_name not in self.weights:
            self.weights[atom_name] = weight

    def add_atoms(self, atoms):
        for atom in atoms:
            self.add_atom(atom)

    # TODO: What about formulas using the atom to be removed?
    #      Should they automatically be removed? Or should an
    #      exception be raised, like FormulaDependencyError?
    #      Or should the user be prompted to choose whether 
    #      all formulas that use the atom should be deleted?
    def remove_atom(self, atom_name):
        if atom_name in self.weights:
            del self.weights[atom_name]

    def add_weight(self, atom_name, weight):
        self.weights[atom_name] = weight

    # Resets the weight to the default (in this case, 1)
    def remove_weight(self, atom_name):
        if atom_name in self.weights:
            self.weights[atom_name] = 1 

    # DONE: Now it extracts and adds the atoms used in the 
    #      formula here, for lower coupling.
    #      Should this extract the atoms used in the formula
    #      and add them to the weights list if they are not 
    #      already there? Currently, this is done from the 
    #      Graph class, but should it be separated out for 
    #      lower coupling?
    def add_formula(self, formula):
        self.formulas.add(formula)
        self.__add_atoms_from_formula(formula)

    def __add_atoms_from_formula(self, formula):
        formula_atoms = formula.get_atoms()
        self.add_atoms(formula_atoms)

    def remove_formula(self, formula):
        self.formulas.discard(formula)
