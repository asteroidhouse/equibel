import sys
import tempfile
import copy
import re

from subprocess import Popen, PIPE

import equibel.FormulaExtractor as FormulaExtractor

import equibel.ASP_Formatter as ASP_Formatter
import equibel.ASP_Parser as ASP_Parser


OPT_VALUE_TEMPLATE = "gringo eq_sets.lp transitive.lp translate.lp {0} | clasp --quiet=2,1 --verbose=0"
OPT_MODEL_TEMPLATE = "gringo eq_sets.lp transitive.lp translate.lp {0} | clasp --quiet=0,2 --verbose=0 --opt-all={1}"
CONTAINMENT_TEMPLATE = "gringo equibel/eq_sets.lp equibel/transitive.lp equibel/translate.lp {0} | hclasp-1.1.5 -e record 0 --verbose=0"

class UnsatisfiableError(Exception): pass

def run_one_shot(filename):
     proc = Popen(CONTAINMENT_TEMPLATE.format(filename), shell=True, stdout=PIPE, universal_newlines=True)
     return proc.stdout.read()

def one_shot(graph):
     # Returns a modified copy of the graph, incorporating the 
     # new formulas obtained from running the ASP solver.

     #temp_file = tempfile.NamedTemporaryFile(mode='w')
     temp_file = open('temp_asp_file', 'w')
     asp_str = ASP_Formatter.convert_to_asp(graph)

     temp_file.write(asp_str)
     temp_file.close()

     output = run_one_shot(temp_file.name)

     models = ASP_Parser.parse_asp(output)
     node_formulas = FormulaExtractor.combined_formulas(models)
     new_graph = updated_graph(graph, node_formulas)
     return new_graph


def updated_graph(graph, node_formulas):
     new_graph = copy.deepcopy(graph)
     for node_num in node_formulas:
          formula = node_formulas[node_num]
          new_graph.add_formula(node_num, formula)
     return new_graph






# TODO: URGENT: Test these functions out.
def find_opt_value(filename):
     proc = Popen(OPT_VALUE_TEMPLATE.format(filename), shell=True, stdout=PIPE, universal_newlines=True)
     output = proc.stdout.read()
     return extract_opt_value(output)

def extract_opt_value(text):
     if text.startswith('UNSATISFIABLE'):
          raise UnsatisfiableError()

     m = re.match(r'Optimization: ([0-9]+)', text)

     if m:
          return int(m.group(1))
     else:
          raise FormatError("Unknown optimization format.")

def get_opt_models(filename):
     opt_value = find_opt_value(filename)
     proc = Popen(OPT_MODEL_TEMPLATE.format(filename, opt_value), shell=True, stdout=PIPE, universal_newlines=True)
     output = proc.stdout.read()
     return ASP_Parser.parse_asp(output)

