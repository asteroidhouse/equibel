import sys
import equibel.FormulaExtractor as FormulaExtractor
import equibel.ASP_Parser as ASP_Parser

from equibel.simbool.simplify import *

if __name__ == '__main__':
     if len(sys.argv) < 2:
          print('usage: python3 FormulaExtractorTest.py filename')
          sys.exit(1)

     filename = sys.argv[1]

     f = open(filename, 'r')
     text = f.read()

     try:
          models = ASP_Parser.parse_asp(text)
          disjunctions = FormulaExtractor.combined_formulas(models)
          for node_num in disjunctions:
               print("Node {0}:".format(node_num))
               print("\tOriginal: {0}".format(repr(disjunctions[node_num])))
               print("\tSimplified: {0}".format(repr(simplify(disjunctions[node_num]))))
     except Exception as err:
          print(err)
     
