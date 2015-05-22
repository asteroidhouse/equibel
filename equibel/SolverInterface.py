from __future__ import absolute_import
from __future__ import print_function

import sys
import tempfile
import copy
import re

from subprocess import Popen, PIPE

import equibel.FormulaExtractor as FormulaExtractor
import equibel.formatters.ASP_Formatter as ASP_Formatter
import equibel.parsers.ASP_Parser as ASP_Parser

from equibel.simbool.simplify import simplify

CARDINALITY_TEMPLATE = "clingo equibel/eq_sets.lp equibel/cardinality_max.lp equibel/transitive.lp equibel/translate.lp {0} --opt-mode=optN --quiet=1,2 --verbose=0"
CONTAINMENT_TEMPLATE = "clingo equibel/eq_sets.lp equibel/transitive.lp equibel/translate.lp {0} 0 --heuristic=domain --enum-mode=domRec --verbose=0"

class UnsatisfiableError(Exception): pass

def run_one_shot_cardinality(filename):
    proc = Popen(CARDINALITY_TEMPLATE.format(filename), shell=True, stdout=PIPE, universal_newlines=True)
    return proc.stdout.read()

def run_one_shot_containment(filename):
    proc = Popen(CONTAINMENT_TEMPLATE.format(filename), shell=True, stdout=PIPE, universal_newlines=True)
    return proc.stdout.read()

def one_shot(graph, cardinality_maximal=False):
    # Returns a modified copy of the graph, incorporating the 
    # new formulas obtained from running the ASP solver.

    #temp_file = tempfile.NamedTemporaryFile(mode='w')
    temp_file = open('temp_asp_file', 'w')
    asp_str = ASP_Formatter.convert_to_asp(graph)
    #print("INPUT:\n", asp_str)

    temp_file.write(asp_str)
    temp_file.close()

    if cardinality_maximal:
        output = run_one_shot_cardinality(temp_file.name)
    else:
        output = run_one_shot_containment(temp_file.name)
    #print("OUTPUT:\n", output)

    models = ASP_Parser.parse_asp(output)
    node_formulas = FormulaExtractor.combined_formulas(models)
    new_graph = updated_graph(graph, node_formulas)
    return new_graph



ITERATE_CARD_TEMPLATE = "clingo equibel/eq_sets.lp equibel/cardinality_max.lp equibel/translate.lp {0} --opt-mode=optN --quiet=1,2 --verbose=0"
ITERATE_CONT_TEMPLATE = "clingo equibel/eq_sets.lp equibel/translate.lp {0} 0 --heuristic=domain --enum-mode=domRec --verbose=0"

def run_iterate_cardinality(filename):
    proc = Popen(ITERATE_CARD_TEMPLATE.format(filename), shell=True, stdout=PIPE, universal_newlines=True)
    return proc.stdout.read()

def run_iterate_containment(filename):
    #print("FILENAME: ", filename)
    proc = Popen(ITERATE_CONT_TEMPLATE.format(filename), shell=True, stdout=PIPE, universal_newlines=True)
    return proc.stdout.read()
    

def iterate(graph, num_iterations=1, cardinality_maximal=False):
    resultant_graph = graph

    for i in range(num_iterations):
        resultant_graph = iterate_once(resultant_graph, cardinality_maximal)

    return resultant_graph

def iterate_steady(graph, cardinality_maximal=False):
    old_graph = graph
    resultant_graph = iterate_once(old_graph, cardinality_maximal)

    while resultant_graph != old_graph:
        old_graph = resultant_graph
        resultant_graph = iterate_once(old_graph, cardinality_maximal)
    
    return resultant_graph


def iterate_once(graph, cardinality_maximal=False):
    #print("ITERATION")

    temp_file = open('temp_asp_file', 'w')
    asp_str = ASP_Formatter.convert_to_asp(graph)

    #print("Iteration input:\n", asp_str)
    temp_file.write(asp_str)
    temp_file.close()

    if cardinality_maximal:
        output = run_iterate_cardinality(temp_file.name)
    else:
        output = run_iterate_containment(temp_file.name)
    #print("Iteration output:\n", output)

    models = ASP_Parser.parse_asp(output)
    node_formulas = FormulaExtractor.combined_formulas(models)
    new_graph = updated_graph(graph, node_formulas)
    return new_graph


def updated_graph(graph, node_formulas):
    new_graph = copy.deepcopy(graph)
    for node_num in node_formulas:
        formula = node_formulas[node_num]

        # NOTE: This makes it so that true propositions are not added as new formulas.
        if not formula.is_true():
            new_graph.add_formula(node_num, formula)
    return new_graph
