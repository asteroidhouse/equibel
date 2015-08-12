import random
import equibel as eb

__all__ = ['literal_conj', 'literal']

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
atoms = [eb.Prop(variable) for variable in ALPHABET]
sorted_atoms = sorted(atoms, key=lambda item: item.name)

conj_pos = lambda formula, x: formula & x
conj_neg = lambda formula, x: formula & ~x
no_change = lambda formula, x: formula
conj_functions = [conj_pos, conj_neg, no_change]

def literal_conj(num_vars):
    variables = sorted_atoms[:num_vars]
    
    formula = eb.Prop(True)

    for variable in variables:
        formula = random.choice(conj_functions)(formula, variable)
    
    return eb.simplify(formula)


negate = lambda x: ~x
identity = lambda x: x
literal_functions = [negate, identity]

def literal(num_vars):
    variables = sorted_atoms[:num_vars]
    formula = random.choice(literal_functions)(random.choice(variables))
    return formula
