import sys

import SolverInterface

sys.path.append("..")
from Graph import Graph

sys.path.append("../simbool")
from simbool.simplify import *

if __name__ == '__main__':
     if len(sys.argv) < 2:
          print('usage: python3 SolverInterfaceTest.py filename')
          sys.exit(1)
     
     filename = sys.argv[1]

     #output = SolverInterface.run_one_shot(filename)
     #print(output)
     
     g = Graph()
     g.add_nodes([1,2,3,4])
     g.add_formula(1, Prop('q'))
     g.add_edge((1,2))
     print(g)

     new_graph = SolverInterface.one_shot(g)
     for node in new_graph.nodes:
          print("Node {0}:".format(node))
          print("Formulas: {0}".format(new_graph.get_formulas(node)))
