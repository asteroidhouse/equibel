from sympy import pprint, simplify, satisfiable
import equibel as eb

if __name__ == '__main__':
    formula = eb.random_formula(num_atoms=6, num_connectives=10)
    pprint(formula)

    for model in satisfiable(formula, all_models=True):
        print(model)

    simplified = simplify(formula)
    pprint(simplified)