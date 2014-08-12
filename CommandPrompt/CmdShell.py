from cmd import Cmd
import readline
from ply import lex
from ply import yacc

import ASP_Formatter
import Simplified_Parser4 as Parser
from runtime_simple import *
from builtin_functions import *

class EdgeError(Exception): pass

def parse(text):
     tokens = ("STRING", "INTEGER", "COMMA", "DOT", "LPAREN", "RPAREN", "LSQUARE", "RSQUARE")

     t_STRING = r'\w+'
     t_COMMA = r','
     t_DOT = r'\.'
     t_LPAREN = r'\('
     t_RPAREN = r'\)'
     t_LSQUARE = r'\['
     t_RSQUARE = r'\]'

     t_ignore = " \t\n"


     def t_INTEGER(t):
          r"0|[1-9][0-9]*"
          t.value = int(t.value)
          return t

     def t_NEWLINE(t):
          r"\n+"
          t.lexer.lineno += len(t.value)
          return t

     def t_error(t):
          line = t.value.lstrip()
          i = line.find("\n")
          line = line if i == -1 else line[:i]
          raise ValueError("Syntax error, line {0}: {1}".format(t.lineno + 1, line))

     def p_LIST_OR_TUPLE(p):
          """LIST_OR_TUPLE : LIST
                           | TUPLE"""
          p[0] = p[1]

     def p_LIST(p):
          """LIST : LSQUARE ITEMS RSQUARE
                  | LSQUARE RANGE RSQUARE
                  | LSQUARE RSQUARE"""
          p[0] = [] if len(p) == 3 else p[2]

     def p_RANGE(p):
          """RANGE : INTEGER DOT DOT INTEGER"""
          p[0] = list(range(p[1], p[4] + 1))

     def p_ITEMS(p):
          """ITEMS : ITEM
                   | ITEM COMMA ITEMS"""
          p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]
     
     def p_ITEM(p):
          """ITEM : INTEGER
                  | STRING
                  | TUPLE"""
          p[0] = p[1]

     def p_TUPLE(p):
          """TUPLE : LPAREN INTEGER COMMA INTEGER RPAREN"""
          p[0] = (int(p[2]), int(p[4]))

     def p_error(p):
          if p is None:
               raise ValueError("Unknown error")
          raise ValueError("Syntax error, line {0}: {1}".format(p.lineno + 1, p.type))

     lexer = lex.lex()
     parser = yacc.yacc()
     
     try:
          return parser.parse(text, lexer=lexer)
     except ValueError as err:
          print(err)



class ManagerError(Exception): pass

class GraphManager:
     def __init__(self):
          self.graphs = dict()
          self.current_context = None

     def __iter__(self):
          return iter(self.graphs)

     def add(self, graph_name, graph):
          self.graphs[graph_name] = graph
          if not self.current_context:
               self.current_context = graph

     def __getitem__(self, key):
          return self.graphs.get(key, None)
     
     def remove(self, graph_name):
          if graph_name not in self.graphs:
               raise ManagerError("graph \"{0}\" does not exist".format(graph_name))
          del self.graphs[graph_name]

     def set_context(self, graph_name):
          if graph_name not in self.graphs:
               raise ManagerError("graph \"{0}\" does not exist".format(graph_name))
          self.current_context = self.graphs[graph_name]
     
manager = GraphManager()
g = Graph()
manager.add('g', g)

class EquibelPrompt(Cmd):

     def check_silencing_terminator(self, arg_str):
          """Checks if arg_str ends with a 'silencing' terminator, such as 
             a semicolon. If it does, this function strips off the terminator 
             and returns the modified string, as well as the boolean True to 
             indicate that the output should be silenced. If it does not, this 
             function returns the string unmodified, as well as the boolean 
             False to indicate that the output should not be silenced."""
          verbose = True
          if arg_str.strip().endswith(';'):
               arg_str = arg_str.strip()[:-1]
               verbose = False
          return (arg_str, verbose)


     def default(self, line):
          """Default behaviour if the command prefix is not recognized."""
          line, verbose = self.check_silencing_terminator(line)
          try:
               nodes = Parser.parse_equibel(line)
               result = nodes.evaluate(Runtime)
               if verbose:
                    print("\n\t{0}\n".format(result))
          except Exception as err:
               print(err)


     def do_graphs(self, arg_str):
          """Prints the names of all existing graphs."""
          _, verbose = self.check_silencing_terminator(arg_str)
          if verbose:
               self.print_graphs()


     def print_graphs(self):
          """Prints the names of all existing graphs."""
          print("\t", end="")
          for graph in manager:
               if manager[graph] is manager.current_context:
                    print("--{0}-- (context)".format(graph), end="  ")
               else:
                    print(graph, end="  ")
          print()
          
     
     def do_create_graph(self, arg_str):
          """Creates a new graph with the given name."""
          arg_str, verbose = self.check_silencing_terminator(arg_str)
          args = arg_str.split()
          graph_name = args[0]
          manager.add(graph_name, Graph())
          manager.set_context(graph_name)
          if verbose:
               self.print_graphs()

     def do_create_chain(self, arg_str):
          """Creates a chain graph."""
          arg_str, verbose = self.check_silencing_terminator(arg_str)
          args = arg_str.split()
          if verbose:
               self.print_graphs()


     def do_use(self, arg_str):
          """Switches the graph context."""
          arg_str, verbose = self.check_silencing_terminator(arg_str)
          args = arg_str.split()
          graph_name = args[0]
          try:
               manager.set_context(graph_name)
               if verbose:
                    self.print_graphs()
          except Exception as err:
               print(err)
          

     def do_nodes(self, arg_str):
          """Prints the nodes in the current context."""
          _, verbose = self.check_silencing_terminator(arg_str)
          if verbose:
               self.print_nodes()


     def print_nodes(self):
          """Prints the nodes in the current context."""
          nodes = manager.current_context.get_nodes()
          if not nodes:
               print("\n\tnodes: {}\n")
          else:
               print("\n\tnodes: {0}\n".format(nodes))
          

     def do_add_node(self, arg_str):
          """Adds a node to the current context."""
          arg_str, verbose = self.check_silencing_terminator(arg_str)
          graph = manager.current_context
          args = arg_str.split()
          if len(args) != 1:
               print("Incorrect number of arguments to add_node!")
          else:
               node_str = args[0]
               if not node_str.isdigit():
                    print("add_node requires an integer argument!")
               else:
                    graph.add_node(int(node_str))
                    if verbose:
                         self.print_nodes()


     def do_add_nodes(self, arg_str):
          """Adds all the nodes from a list to the current context."""
          arg_str, verbose = self.check_silencing_terminator(arg_str)
          graph = manager.current_context

          try:
               node_list = parse(arg_str)
               for node_num in node_list:
                    graph.add_node(node_num)
          except EdgeError as err:
               print(err)

          if verbose:
               self.print_nodes()

                         
     def do_remove_node(self, arg_str):
          """Removes a node (if it exists) from the nodes set."""
          arg_str, verbose = self.check_silencing_terminator(arg_str)
          graph = manager.current_context

          args = arg_str.split()
          if len(args) != 1:
               print("Incorrect number of arguments to remove_node!")
          else:
               node_str = args[0]
               if not node_str.isdigit():
                    print("remove_node requires an integer argument!")
               else:
                    graph.remove_node(int(node_str))
                    if verbose:
                         self.print_nodes()


     def do_edges(self, arg_str):
          """Prints the existing edges."""
          _, verbose = self.check_silencing_terminator(arg_str)
          if verbose:
               self.print_edges()


     def print_edges(self):
          """Prints the existing edges."""
          edges = manager.current_context.get_edges()
          directed = manager.current_context.directed
          if not edges:
               print("\n\tedges: {}\n")
          else:
               if directed:
                    arrow = '->'
               else:
                    arrow = '<->'
               print("\n\tedges:")
               for edge in edges:
                    print("\t\t{0} {1} {2}".format(edge[0], arrow, edge[1]))
               print()
          

     def do_add_edge(self, arg_str):
          """Adds an edge to the edges set."""
          arg_str, verbose = self.check_silencing_terminator(arg_str)

          try:
               edge = parse(arg_str)
               self.add_edge(edge)
               if verbose:
                    self.print_edges()
          except EdgeError as err:
               print(err)


     def do_add_edges(self, arg_str):
          """Adds all the edges in a list to the edges set."""
          arg_str, verbose = self.check_silencing_terminator(arg_str)

          try:
               edge_list = parse(arg_str)
               for edge in edge_list:
                    self.add_edge(edge)
               
               if verbose:
                    self.print_edges()
          except EdgeError as err:
               print(err)


     def add_edge(self, edge):
          # Adds the start and end nodes to the nodes set, if they don't 
          # already exist.
          graph = manager.current_context
          start, end = edge
          graph.add_node(start)
          graph.add_node(end)
          graph.add_edge(edge)
          

     def do_remove_edge(self, arg_str):
          """Removes an edge (if it exists) from the edges set."""
          arg_str, verbose = self.check_silencing_terminator(arg_str)
          graph = manager.current_context

          try:
               edge = parse(arg_str)
               graph.remove_edge(edge)
               if verbose:
                    self.print_edges()
          except EdgeError as err:
               print(err)


     # Directed/Undirected Functions
     #---------------------------------------------------------------------
     
     def do_directed(self, arg_str):
          """Makes the edges in the current context directed."""
          _, verbose = self.check_silencing_terminator(arg_str)
          manager.current_context.directed = True
          if verbose:
               print("\n\tedges are now directed\n")

     def do_undirected(self, arg_str):
          """Makes the edges in the current context undirected."""
          _, verbose = self.check_silencing_terminator(arg_str)
          manager.current_context.directed = False
          if verbose:
               print("\n\tedges are now undirected\n")


     # Atom Functions
     #---------------------------------------------------------------------

     def do_add_atom(self, arg_str):
          """Adds an atom to the alphabet of the current context."""
          arg_str, verbose = self.check_silencing_terminator(arg_str)
          graph = manager.current_context

          args = arg_str.split()
          if len(args) != 1:
               print("Expected 1 argument to add_atom!")
          else:
               atom_str = args[0]
               graph.add_atom(atom_str)
               if verbose:
                    self.print_atoms()

     def do_add_atoms(self, arg_str):
          """Adds all the atoms in a list to the alphabet of the current context."""
          arg_str, verbose = self.check_silencing_terminator(arg_str)
          graph = manager.current_context

          try:
               atom_list = parse(arg_str)
               for atom in atom_list:
                    graph.add_atom(atom)
               
               if verbose:
                    self.print_atoms()
          except Exception as err:
               print(err)

     def do_remove_atom(self, arg_str):
          """Removes an atom from the alphabet of the current context."""
          arg_str, verbose = self.check_silencing_terminator(arg_str)
          graph = manager.current_context

          args = arg_str.split()
          if len(args) != 1:
               print("Expected 1 argument to remove_atom!")
          else:
               atom_str = args[0]
               graph.remove_atom(atom_str)
               if verbose:
                    self.print_atoms()

          
     def do_atoms(self, arg_str):
          """Prints the atoms in the alphabet of the current context."""
          _, verbose = self.check_silencing_terminator(arg_str)
          if verbose:
               self.print_atoms()

     def print_atoms(self):
          atoms = manager.current_context.get_atoms()
          if not atoms:
               print("\n\tatoms: {}\n")
          else:
               print("\n\tatoms: {0}\n".format(atoms))
          

     # Weight Functions
     #---------------------------------------------------------------------

     # TODO: These are sort of temporary in their current form.
     def do_add_weight(self, arg_str):
          arg_str, verbose = self.check_silencing_terminator(arg_str)
          args = arg_str.split()
          # TODO: Finish this function, with error checking.
          



     # ASP Functions
     #---------------------------------------------------------------------

     def do_asp(self, arg_str):
          arg_str, verbose = self.check_silencing_terminator(arg_str)
          graph = manager.current_context

          if verbose:
               print("\n" + ASP_Formatter.convert_to_asp(graph))
          
     
     def do_quit(self, args):
          """Quits the program."""
          print("Bye!")
          raise SystemExit


if __name__ == '__main__':
     prompt = EquibelPrompt(completekey='tab')
     prompt.prompt = "equibel> "
     prompt.cmdloop("Equibel version 0.8.2")
