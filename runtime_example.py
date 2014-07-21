import Equibel_Parser_AST as Parser
from runtime_simple import *

code = """a = 3\nprint a\n"""

nodes = Parser.parse_equibel(code)
nodes.evaluate(Runtime)
