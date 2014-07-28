import Simplified_Parser4 as Parser
from runtime_simple import *
from builtin_functions import *

while True:
     code = input("equibel> ")
     
     if code == 'info':
          for key in Runtime.locals:
               print(key)
               value = Runtime.locals[key]
               print(value.python_value)
     else:
          try:
               nodes = Parser.parse_equibel(code)
               result = nodes.evaluate(Runtime)
               print("\n\t", result, "\n")
          except Exception as err:
               print(err)
