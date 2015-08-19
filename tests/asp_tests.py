#!/usr/bin/python

from __future__ import absolute_import
from __future__ import print_function

import sys
import tempfile
import copy
import re
import random
import time

from subprocess import Popen, PIPE

import equibel as eb
import equibel.FormulaExtractor as FormulaExtractor
import equibel.formatters.ASP_Formatter as ASP_Formatter
import equibel.parsers.ASP_Parser as ASP_Parser

from equibel.simbool.simplify import simplify


ASP_DIR = "../equibel/asp"

CARDINALITY_TEMPLATE = "clingo {d}/eq_sets.lp {d}/cardinality_max.lp {d}/transitive.lp {d}/translate.lp {f} --opt-mode=optN --quiet=1,2 --verbose=0"
CONTAINMENT_TEMPLATE = "clingo {d}/eq_sets.lp {d}/transitive.lp {d}/translate.lp {f} 0 --heuristic=domain --enum-mode=domRec --verbose=0"

class UnsatisfiableError(Exception): pass

@profile
def run_one_shot_cardinality(filename):
    proc = Popen(CARDINALITY_TEMPLATE.format(d=ASP_DIR, f=filename), shell=True, stdout=PIPE, universal_newlines=True)
    return proc.stdout.read()

@profile
def one_shot(graph):
    temp_file = open('asp_graph_file', 'w')
    asp_str = eb.convert_to_asp(graph)
    temp_file.write(asp_str)
    temp_file.close()

    output = run_one_shot_cardinality(temp_file.name)

    models = eb.parse_asp(output)
    node_formulas = FormulaExtractor.combine_formulas(models)
    new_graph = updated_graph(graph, node_formulas)
    return new_graph


@profile
def generate_formula(num_variables):
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"

    variables = ALPHABET[:num_variables]
    atoms = [eb.Prop(variable) for variable in variables]
    
    formula = eb.Prop(True)
    functions = [lambda x: formula & x, lambda x: formula & ~x, lambda x: formula]

    for atom in atoms:
        formula = random.choice(functions)(atom)
    
    return formula
    

@profile
def populate_formulas(G, num_variables):
    # Generate formulas for each node according to certain parameters
    for node_id in G:
        formula = generate_formula(num_variables)
        G.add_formula(node_id, formula)
        print("{0}: {1}".format(node_id, formula))


@profile
def run_trial(num_nodes, num_variables):
    G = eb.path_graph(num_nodes)
    populate_formulas(G, num_variables)
    S = one_shot(G)
    

@profile
def run_perf_tests(start_num_nodes=10, end_num_nodes=100, step_size=10, num_trials=10, num_variables=3):
    d = dict()

    for num_nodes in range(start_num_nodes, end_num_nodes + 1, step_size):
        for trial in range(num_trials):
            print("running trial")
            elapsed_time = run_trial(num_nodes, num_variables)


if __name__ == '__main__':
    run_perf_tests(10, 10, 1, 1)
