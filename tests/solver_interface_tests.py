import sys

import equibel.SolverInterface
from equibel.graph import Graph

from equibel.simbool.simplify import *

if __name__ == '__main__':
     if len(sys.argv) < 2:
          print('usage: python3 SolverInterfaceTest.py filename')
          sys.exit(1)
     
     filename = sys.argv[1]

     #output = SolverInterface.run_one_shot(filename)
     #print(output)
     
     g = Graph()
     g.add_nodes([1,2,3,4])
     g.add_edge((1,2))
     g.add_edge((1,3))
     g.add_edge((3,4))
     g.add_edge((2,4))
     g.add_formula(1, Prop('p'))
     g.add_formula(2, ~Prop('p'))
     g.add_formula(2, Prop('q'))
     print(g)

     print(SolverInterface.get_opt_models(g))
     """
     new_graph = SolverInterface.one_shot(g)
     for node in new_graph.nodes:
          print("Node {0}:".format(node))
          print("Formulas: {0}".format(new_graph.get_formulas(node)))
     """
