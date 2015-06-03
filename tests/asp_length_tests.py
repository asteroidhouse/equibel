#!/usr/bin/python

from __future__ import absolute_import
from __future__ import print_function

import random
import time

from subprocess import Popen, PIPE
import matplotlib.pyplot as plt
import equibel as eb


PATH = 'path'
STAR = 'star'
COMPLETE = 'complete'
graph_types = [PATH, STAR, COMPLETE]


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
        #print("{0}: {1}".format(node_id, repr(formula)))


def generate_graph(num_nodes, graph_type):
    if graph_type == PATH:
        return eb.path_graph(num_nodes)
    elif graph_type == STAR:
        return eb.star_graph(num_nodes)
    elif graph_type == COMPLETE:
        return eb.complete_graph(num_nodes)
    else:
        raise Exception("Unknown graph type!")


def write_graph(graph, filename):
    f = open(filename, 'w')
    asp_str = eb.convert_to_asp(graph)
    f.write(asp_str)
    f.close()

def count_lines(start_num_nodes, end_num_nodes, step_size, graph_type, num_variables=4):
    prefix = "../equibel/asp"
    counts = dict()

    for num_nodes in range(start_num_nodes, end_num_nodes+1, step_size):
        G = generate_graph(num_nodes, PATH)
        populate_formulas(G, num_variables)

        filename = "temp_asp_file"
        write_graph(G, filename)

        proc = Popen("gringo {0} | wc -l".format(filename), shell=True, stdout=PIPE, universal_newlines=True)
        graph_lines = int(proc.stdout.read())

        proc = Popen("gringo {0} {pre}/eq_sets.lp | wc -l".format(filename, pre=prefix), 
                     shell=True, stdout=PIPE, universal_newlines=True)
        graph_eq_lines = int(proc.stdout.read())

        proc = Popen("gringo {0} {pre}/eq_sets.lp {pre}/transitive.lp | wc -l".format(filename, pre=prefix), 
                     shell=True, stdout=PIPE, universal_newlines=True)
        graph_eq_trans_lines = int(proc.stdout.read())

        proc = Popen("gringo {0} {pre}/eq_sets.lp {pre}/transitive.lp {pre}/translate.lp | wc -l".format(filename, pre=prefix), 
                     shell=True, stdout=PIPE, universal_newlines=True)
        graph_eq_t2_lines = int(proc.stdout.read())

        counts[num_nodes] = (graph_lines, graph_eq_lines, graph_eq_trans_lines, graph_eq_t2_lines)
        
        print("--------------------------------------------------")
        print("# Nodes = {0}".format(num_nodes))
        print("GRAPH = {0}".format(graph_lines))
        print("GRAPH + EQ = {0}".format(graph_eq_lines))
        print("GRAPH + EQ + TRANSITIVE = {0}".format(graph_eq_trans_lines))
        print("GRAPH + EQ + TRANSITIVE + TRANSLATE = {0}".format(graph_eq_t2_lines))

    return counts

if __name__ == '__main__':
    start_num_nodes = 5
    end_num_nodes = 35
    step_size = 5

    counts = count_lines(start_num_nodes, end_num_nodes, step_size, COMPLETE)
    plt.plot(range(start_num_nodes, end_num_nodes+1, step_size), [counts[val][0] for val in counts], 'go-')
    plt.plot(range(start_num_nodes, end_num_nodes+1, step_size), [counts[val][1] for val in counts], 'bo-')
    plt.plot(range(start_num_nodes, end_num_nodes+1, step_size), [counts[val][2] for val in counts], 'ro-')
    plt.plot(range(start_num_nodes, end_num_nodes+1, step_size), [counts[val][3] for val in counts], 'ro-')
    plt.show()

