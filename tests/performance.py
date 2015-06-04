#!/usr/bin/python

import random
import time

import equibel as eb

def generate_formula(num_variables):
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"

    variables = ALPHABET[:num_variables]
    atoms = [eb.Prop(variable) for variable in variables]
    
    formula = eb.Prop(True)
    add_pos = lambda x: formula & x
    add_neg = lambda x: formula & ~x
    no_change = lambda x: formula
    functions = [add_pos, add_neg, no_change]

    for atom in atoms:
        formula = random.choice(functions)(atom)
    
    #return eb.simplify(formula)
    return formula
    

def populate_formulas(G, num_variables):
    # Generate formulas for each node according to certain parameters
    for node_id in G:
        formula = generate_formula(num_variables)
        G.add_formula(node_id, formula)
        print("{0}: {1}".format(node_id, formula))


def run_trial(num_nodes, num_variables):
    G = eb.path_graph(num_nodes)
    populate_formulas(G, num_variables)

    start_time = time.clock()
    S = eb.completion(G)
    end_time = time.clock()

    elapsed_time = end_time - start_time
    return elapsed_time
    

def run_perf_tests(start_num_nodes=10, end_num_nodes=100, step_size=10, num_trials=10, num_variables=3):
    d = dict()

    for num_nodes in range(start_num_nodes, end_num_nodes + 1, step_size):
        for trial in range(num_trials):
            print("running trial")
            elapsed_time = run_trial(num_nodes, num_variables)
            if num_nodes in d:
                d[num_nodes].append(elapsed_time)
            else:
                d[num_nodes] = [elapsed_time]


if __name__ == '__main__':
    run_perf_tests(2, 10, 2, 3)
