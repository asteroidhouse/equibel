import sys
import tempfile
import copy

from subprocess import Popen, PIPE

import FormulaExtractor

sys.path.append("..")
import ASP_Formatter
import ASP_Parser


#COMMAND_TEMPLATE = "gringo eq_sets.lp transitive.lp translate.lp {0} | clasp --quiet=0,2 --verbose=0"
COMMAND_TEMPLATE = "gringo eq_sets.lp transitive.lp translate.lp {0} | clasp --quiet=1,2 --verbose=0"

def run_one_shot(filename):
     proc = Popen(COMMAND_TEMPLATE.format(filename), shell=True, stdout=PIPE, universal_newlines=True)
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
