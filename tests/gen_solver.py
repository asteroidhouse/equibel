from __future__ import absolute_import
from __future__ import print_function

import time
import subprocess

from timeit import timeit

import matplotlib.pyplot as plt

import formulagen
from solver_profile5 import completion

import equibel as eb


def completion_test(G):
    start_time = time.clock()
    R = completion(G)
    end_time = time.clock()
    return end_time - start_time


def generate_graph(graph_gen_func, 
                   formula_gen_func,
                   graph_gen_args={"n": 10},
                   formula_gen_args={"num_vars": 5}):
    G = graph_gen_func(**graph_gen_args)
    for node_id in G.nodes():
        formula = formula_gen_func(**formula_gen_args)
        G.add_formula(node_id, formula)
    return G


def run_test(test_func, graph_gen_func, formula_gen_func, graph_gen_args, formula_gen_args):
    G = generate_graph(graph_gen_func, formula_gen_func, graph_gen_args, formula_gen_args)
    data = test_func(G)
    return data
    

def run_tests(test_func=completion_test,
              start_num_nodes=5, 
              end_num_nodes=50, 
              step_size=5, 
              repetitions=1,
              graph_gen_func=eb.path_graph,
              formula_gen_func=formulagen.literal_conj,
              num_vars=5):
    data = dict()
    for num_nodes in range(start_num_nodes, end_num_nodes+1, step_size):
        for rep in range(repetitions):
            print("Running tests on {0} nodes, rep {1}...".format(num_nodes, rep+1))
            current_data = run_test(test_func, graph_gen_func, formula_gen_func, 
                                    graph_gen_args={"n": num_nodes}, 
                                    formula_gen_args={"num_vars": num_vars})
            if num_nodes in data:
                data[num_nodes].append(current_data)
            else:
                data[num_nodes] = [current_data]

    return data


def line_graph(data):
    averages = {key: (sum(value)/len(value)) for (key,value) in data.items()}
    plt.plot(averages.keys(), averages.values(), 'ro-')
    plt.title("Clingo Solving Times for Path Graphs with 5-Variable Formulas")
    plt.ylabel("Solving Time (seconds)")
    plt.xlabel("Number of Nodes")
    plt.show()


def histogram(data):
    vals = data.values()
    flattened_vals = [x for lst in vals for x in lst]
    plt.hist(flattened_vals, 30, color='g', normed=True)
    plt.title("Completion Time Histogram: 10-Node Star Graph with 4-Variable Formulas")
    plt.ylabel("Frequency")
    plt.xlabel("Completion Time")
    plt.show()
    


if __name__ == '__main__':
    data = run_tests(test_func=completion_test,
                     start_num_nodes=5,
                     end_num_nodes=10,
                     step_size=1,
                     repetitions=5,
                     graph_gen_func=eb.path_graph,
                     formula_gen_func=formulagen.literal_conj,
                     num_vars=10)

    print(data)
    
    line_graph(data)
    #histogram(data)
