import Equibel_Parser_AST as Parser
from runtime_simple import *

code = """a = 3\nprint "hello" 3\nadd_node 3\n"""

nodes = Parser.parse_equibel(code)
nodes.evaluate(Runtime)
