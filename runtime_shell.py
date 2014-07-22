import Equibel_Parser_AST2 as Parser
from runtime_simple import *

while True:
     code = input("> ")
     
     if code == 'info':
          for key in Runtime.locals:
               print(key)
               value = Runtime.locals[key]
               print(value.python_value)
     elif code == 'nodes':
          print(nodes_list)
     else:
          code += "\n"
     
          try:
               nodes = Parser.parse_equibel(code)
               nodes.evaluate(Runtime)
          except Exception as err:
               print(err)
