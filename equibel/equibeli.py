"""This file defines the equibeli interactive command-line interface (CLI).

"""
#    Copyright (C) 2014-2015 by
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.
from __future__ import absolute_import
from __future__ import print_function

from cmd import Cmd
from colorama import Fore, Style
import os

from subprocess import Popen, PIPE

import equibel as eb

import equibel.formatters.ASP_Formatter as ASP_Formatter
import equibel.formatters.BCF_Formatter as BCF_Formatter

from equibel.graph_manager import GraphManager
from equibel.graph import EquibelGraph

import equibel.parsers.CmdLineParser as CmdLineParser
import equibel.parsers.FormulaParserSim as FormulaParserSim
import equibel.parsers.BCF_Parser as BCF_Parser


class ArgumentError(Exception):
    pass


manager = GraphManager()
G = EquibelGraph()
manager.add('g', G)

# TODO: Add support for debugging output; for example, when the completion 
# is performed, the debug output should show how many EQ sets were generated, 
# and the size of the sets, etc.
debug = False
solving_method = eb.CONTAINMENT


class EquibelPrompt(Cmd):

    def check_silencing_terminator(self, arg_str):
        """
        Checks if arg_str ends with a 'silencing' terminator, such as
        a semicolon. If it does, this function strips off the terminator
        and returns the modified string, as well as the boolean True to
        indicate that the output should be silenced. If it does not, this
        function returns the string unmodified, as well as the boolean
        False to indicate that the output should not be silenced.
        """
        verbose = True
        arg_str = arg_str.strip()
        if arg_str.endswith(';'):
            arg_str = arg_str[:-1]
            verbose = False
        return (arg_str, verbose)


    def default(self, line):
        """
        Default behaviour if the command prefix is not recognized.
        """
        line, verbose = self.check_silencing_terminator(line)
        if line.isdigit():
            if int(line) in manager.current_context.nodes():
                print(manager.current_context.node[int(line)])
        else:
            print("\tUnrecognized command! Type \"help\" for a list of commands.")


    def do_graphs(self, arg_str):
        """
        Usage: graphs

        Prints the names of all existing graphs, and shows which graph is
        the current context.
        """
        _, verbose = self.check_silencing_terminator(arg_str)
        if verbose:
            self.print_graphs()


    def print_graphs(self):
        """Prints the names of all existing graphs."""
        print()
        print("\t", end="")
        for graph_name in manager:
            if manager[graph_name] is manager.current_context:
                print(Fore.GREEN + "--{0}--".format(graph_name) + Fore.RESET, end="  ")
            else:
                print(graph_name, end="  ")
        print("\n")


    def do_create_graph(self, arg_str):
        """
        Usage: create_graph GRAPH_NAME

        Creates a new graph with the given name, and switches to the 
        context of the new graph.

        Example: create_graph g2
        """
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        args = arg_str.split()

        graph_name = args[0]
        R = EquibelGraph()
        manager.add(graph_name, R)
        manager.set_context(graph_name)

        self.prompt = "equibeli ({0}) > ".format(graph_name)
        if verbose:
            self.print_graphs()


    def do_create_path(self, arg_str):
        """Creates a path graph."""
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        args = arg_str.split()
        graph_name = args[0]
        num_nodes_str = args[1]

        direction = None

        if len(args) > 2:
            direction = args[2]

        if not num_nodes_str.isdigit():
            raise ValueError("Error: create_path requires an integer argument!")
        else:
            num_nodes = int(num_nodes_str)

            if direction == "<->" or direction == None:
                R = eb.path_graph(num_nodes)
            elif direction == "->":
                R = eb.path_graph(num_nodes, directed=True)
            elif direction == "<-":
                R = eb.path_graph(num_nodes, directed=True).reverse()
            else:
                raise ValueError('Error: The direction specifier must be one of "<-", "<->", or "->"')
            
            manager.add(graph_name, R)
            manager.set_context(graph_name)

            self.prompt = "equibeli ({0}) > ".format(graph_name)
        if verbose:
            self.print_graphs()

    
    def do_create_star(self, arg_str):
        """Creates a star graph."""
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        args = arg_str.split()
        graph_name = args[0]
        num_nodes_str = args[1]

        if not num_nodes_str.isdigit():
            raise ValueError("Error: create_star requires an integer argument!")
        else:
            num_nodes = int(num_nodes_str)
            R = eb.star_graph(num_nodes)
            manager.add(graph_name, R)
            manager.set_context(graph_name)
            self.prompt = "equibeli ({0}) > ".format(graph_name)
        if verbose:
            self.print_graphs()


    def do_create_complete(self, arg_str):
        """Creates a complete graph."""
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        args = arg_str.split()
        graph_name = args[0]
        num_nodes_str = args[1]

        if not num_nodes_str.isdigit():
            raise ValueError("Error: create_complete requires an integer argument!")
        else:
            num_nodes = int(num_nodes_str)
            R = eb.complete_graph(num_nodes)
            manager.add(graph_name, R)
            manager.set_context(graph_name)
            self.prompt = "equibeli ({0}) > ".format(graph_name)
        if verbose:
            self.print_graphs()


    def do_delete(self, arg_str):
        """Deletes a graph."""
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        args = arg_str.split()
        graph_name = args[0]
        manager.remove(graph_name)


    def do_use(self, arg_str):
        """
        Usage: use GRAPH_NAME

        Switches the context to the graph with the specified name.
            
        Example: use g2
        """
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        args = arg_str.split()
        graph_name = args[0]
        try:
            manager.set_context(graph_name)
            self.prompt = "equibeli ({0}) > ".format(graph_name)
        except Exception as err:
            print(err)
        

    def do_nodes(self, arg_str):
        """
        Usage: nodes

        Prints the nodes in the current graph context.
        """
        _, verbose = self.check_silencing_terminator(arg_str)
        if verbose:
            self.print_nodes()


    def print_nodes(self):
        """Prints the nodes in the current context."""
        nodes = manager.current_context.nodes()

        if not nodes:
            print("\n\tnodes: []\n")
        else:
            print("\n\tnodes: {0}\n".format(nodes))
        

    def do_add_node(self, arg_str):
        """
        Usage: add_node NODE_NUM

        Adds a node to the current graph context.
        The node must be identified by an integer (for now).

        Example: add_node 1
        """
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        G = manager.current_context
        args = arg_str.split()
        if len(args) != 1:
            print("Incorrect number of arguments to add_node!")
        else:
            node_str = args[0]
            if not node_str.isdigit():
                raise ValueError("Error: add_node requires an integer argument!")
            else:
                node_id = int(node_str)
                G.add_node(node_id)
                if verbose:
                    self.print_nodes()


    def do_add_nodes(self, arg_str):
        """
        Usage: add_nodes NODE_LIST

        Adds all the nodes from a list to the current context.

        Examples:

          Add nodes 1, 3, 5, and 7:
             add_nodes [1, 3, 5, 7]
              
          Add a range of all nodes from 1 to 100, inclusive:
             add_nodes [1..100]
        """
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        graph = manager.current_context

        try:
            node_list = CmdLineParser.parse_list(arg_str)
            graph.add_nodes(node_list)

        except Exception as err:
            print(err)

        if verbose:
            self.print_nodes()

                    
    def do_remove_node(self, arg_str):
        """
        Usage: remove_node NODE_NUM

        Removes a node (if it exists) from the nodes set.

        Example: remove_node 2
        """
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
    

    def do_remove_nodes(self, arg_str):
        """
        Usage: remove_nodes NODE_LIST

        Removes all the nodes in the given list from the nodes set.

        Examples:

          Remove nodes 1, 3, 5, and 7:
             remove_nodes [1, 3, 5, 7]
          
          Remove all nodes from 1 to 10, inclusive:
             remove_nodes [1..10]
        """
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        graph = manager.current_context
        
        nodes = CmdLineParser.parse_list(arg_str)
        # choose either "remove_nodes_from" or "remove_nodes"
        graph.remove_nodes_from(nodes)

        if verbose:
            self.print_nodes()


    def do_edges(self, arg_str):
        """
        Usage: edges

        Prints the existing edges.
        """
        _, verbose = self.check_silencing_terminator(arg_str)
        if verbose:
            self.print_edges()


    def print_edges(self):
        """Prints the existing edges."""
        G = manager.current_context
        edges = G.edges()
        directed = G.is_directed()

        if not edges:
            print("\n\tedges: []\n")
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
        """
        Usage: add_edge (START_NODE, END_NODE)

        Adds an edge to the edges set.
        
        Example: add_edge (1,2)
        """
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        G = manager.current_context

        try:
            (from_node_id, to_node_id) = CmdLineParser.parse_tuple(arg_str)
            G.add_edge(from_node_id, to_node_id)

            if verbose:
                self.print_edges()
        except Exception as err:
            print(err)


    def do_add_edges(self, arg_str):
        """
        Usage: add_edges EDGE_LIST

        Adds all the edges in the given list to the edges set.

        Example: add_edges [(1,2), (2,3), (3,4)]
        """
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        G = manager.current_context

        try:
            edge_list = CmdLineParser.parse_list(arg_str)
            G.add_edges(edge_list)
            
            if verbose:
                self.print_edges()
        except Exception as err:
            print(err)

        

    def do_remove_edge(self, arg_str):
        """
        Usage: remove_edge (START_NODE, END_NODE)

        Removes an edge (if it exists) from the edges set.
           
        Example: remove_edge (1,2)
        """
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        G = manager.current_context

        try:
            (from_node_id, to_node_id) = CmdLineParser.parse_tuple(arg_str)
            G.remove_edge(from_node_id, to_node_id)
            if verbose:
                self.print_edges()
        except Exception as err:
            print(err)


    # Directed/Undirected Functions
    #------------------------------------------------------------------------
    
    def do_directed(self, arg_str):
        """
        Usage: directed

        Makes the edges in the current context directed.
        """
        _, verbose = self.check_silencing_terminator(arg_str)
        G = manager.current_context
        directed_graph = G.to_directed()
        #G.to_directed()
        manager.update_context(directed_graph)
        if verbose:
            self.print_edges()

    def do_undirected(self, arg_str):
        """
        Usage: undirected

        Makes the edges in the current context undirected.
        """
        _, verbose = self.check_silencing_terminator(arg_str)
        G = manager.current_context
        undirected_graph = G.to_undirected()
        #G.to_undirected()
        manager.update_context(undirected_graph)
        if verbose:
            self.print_edges()


    # Atom Functions
    #------------------------------------------------------------------------

    def do_add_atom(self, arg_str):
        """
        Usage: add_atom ATOM_NAME
           
        Adds an atom to the alphabet of the current graph context.

        Examples: add_atom p
                  add_atom the_sky_is_blue
        """
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        G = manager.current_context

        args = arg_str.split()
        if len(args) != 1:
            print("Expected 1 argument to add_atom!")
        else:
            atom_str = args[0]
            G.add_atom(atom_str)
            
            if verbose:
                self.print_atoms()


    def do_add_atoms(self, arg_str):
        """
        Usage: add_atoms LIST_OF_ATOMS
           
        Adds all the atoms in the list to the alphabet of the current context.

        Examples: add_atoms [p, q, r, s]
                  add_atoms [blue_sky, green_grass]
        """
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        G = manager.current_context

        try:
            atom_list = CmdLineParser.parse_list(arg_str)
            G.add_atoms(atom_list)
            
            if verbose:
                self.print_atoms()
        except Exception as err:
            print(err)

    def do_remove_atom(self, arg_str):
        """
        Usage: remove_atom ATOM_NAME 

        Removes an atom from the alphabet of the current context.

        Example: remove_atom p
        """
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        G = manager.current_context

        args = arg_str.split()
        if len(args) != 1:
            print("Expected 1 argument to remove_atom!")
        else:
            atom_str = args[0]
            G.remove_atom(atom_str)
            if verbose:
                self.print_atoms()


    def do_atoms(self, arg_str):
        """
        Usage: atoms
           
        Prints the atoms in the alphabet of the current context.
        """
        _, verbose = self.check_silencing_terminator(arg_str)
        if verbose:
            self.print_atoms()

    def print_atoms(self):
        """Prints the atoms in the alphabet of the current context."""
        G = manager.current_context
        atoms = G.atoms()
        if not atoms:
            print("\n\tatoms: {}\n")
        else:
            print("\n\tatoms: {0}\n".format(atoms))
        

    # Weight Functions
    #------------------------------------------------------------------------

    # TODO: These are sort of temporary in their current form.
    def do_add_weight(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        args = arg_str.split()
        # DONE: Finish this function, with error checking.
        if len(args) != 3:
            raise ArgumentError("Expected 3 arguments to add_weight!\
                                \nUsage: add_weight NODE_NUM ATOM WEIGHT")

        node_str, atom, weight_str = args
        if not node_str.isdigit():
            raise ArgumentError("The node identifier must be an integer: \"{0}\"".format(node_str))
        if not weight_str.isdigit():
            raise ArgumentError("The weight must be an integer: \"{0}\"".format(weight_str))

        node_id = int(node_str)
        weight = int(weight_str)

        G = manager.current_context
        G.add_weight(node_id, atom, weight)

        if verbose:
            self.print_weights(node_id)


    def print_weights(self, node_id):
        weights = manager.current_context.atom_weights(node_id)

        print()
        print("\tnode {0}:".format(node_id))
        for atom in weights:
            print("\t\t{0}: {1}".format(atom, weights[atom]))
        print()


    def print_all_weights(self):
        G = manager.current_context
        
        print()
        for node_id in G.nodes():
            print("\tnode {0}:".format(node_id))
            weights = G.atom_weights(node_id)
            for atom in weights:
                print("\t\t{0}: {1}".format(atom, weights[atom]))
        print()


    def do_weights(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        args = arg_str.split()
        
        if len(args) == 0:
            if verbose:
                self.print_all_weights()
        elif len(args) == 1:
            node_str = args[0]
            if not node_str.isdigit():
                raise ArgumentError("The node identifier must be an integer: \"{0}\"".format(node_str))
            if verbose:
                self.print_weights(int(node_str))
        else:
            raise ArgumentError("Expected 0 or 1 argument to weights!\nusage: weights [NODE_NUM]")



    # Formula Functions
    #------------------------------------------------------------------------

    def do_add_formula(self, arg_str):
        """
        Usage: add_formula NODE_NUM FORMULA
            
        Adds a formula to the specified node.
        The formula must be specified in infix notation.

        Example: add_formula 1 (p & q) -> ~r
        """
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        #args = arg_str.split(maxsplit=1)
        # Python2 version of split does not accept keywork args, so we use:
        args = arg_str.split(None, 1)

        G = manager.current_context

        if len(args) != 2:
            raise ArgumentError("Expected exactly 2 arguments to add_formula.\nusage: add_formula NODE_NUM FORMULA")

        node_str, formula_str = args

        if not node_str.isdigit():
            raise ArgumentError("The node identifier must be an integer.")

        node_id = int(node_str)
        formula = eb.parse_infix_formula(formula_str)
        G.add_formula(node_id, formula)

        if verbose:
            self.print_formulas(node_id)


    def do_remove_formula(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        # Python2 version of split does not accept keywork args, so we use:
        args = arg_str.split(None, 1)

        G = manager.current_context

        if len(args) != 2:
            raise ArgumentError("Expected exactly 2 arguments to add_formula.\nusage: add_formula NODE_NUM FORMULA")

        node_str, formula_str = args

        if not node_str.isdigit():
            raise ArgumentError("The node identifier must be an integer.")

        node_id = int(node_str)
        formula = eb.parse_infix_formula(formula_str)

        G.remove_formula(node_id, formula)

        if verbose:
            self.print_formulas(node_id)
        
    
    def do_formulas(self, arg_str):
        """
        Usage: formulas [NODE_NUM]

        If a node is specified, prints the formulas at that node.
        If no node is specified, prints the formulas at each node.
           
        Example: formulas
                 formulas 1
        """
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        args = arg_str.split()
        
        if len(args) == 0:
            if verbose:
                self.print_all_formulas()
        elif len(args) == 1:
            node_str = args[0]
            if not node_str.isdigit():
                raise ArgumentError("the node identifier must be an integer: \"{0}\"".format(node_str))
            if verbose:
                self.print_formulas(int(node_str))
        else:
            raise ArgumentError("Expected 0 or 1 argument to formulas!\nusage: formulas [NODE_NUM]")


    def print_formulas(self, node_id):
        formulas = manager.current_context.formulas(node_id)

        print()
        print("\tnode {0}:".format(node_id))
        for formula in formulas:
            print("\t\t{0}".format(repr(formula)))
        print()


    def print_all_formulas(self):
        G = manager.current_context
        
        print()
        for node_id in G.nodes():
            print("\tnode {0}:".format(node_id))
            formulas = G.formulas(node_id)
            for formula in formulas:
                print("\t\t{0}".format(repr(formula)))
        print()
            

    # ASP Functions
    # -----------------------------------------------------------------------

    def do_asp(self, arg_str):
        """
        Usage: asp

        Prints out the ASP code representing the current graph context.
        Used mainly for debugging purposes, so you can see the ASP code
        that is being passed to the solver.
        """
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        G = manager.current_context

        if verbose:
            print("\n" + ASP_Formatter.convert_to_asp(G))
        


    # Load/Store Functions
    # -----------------------------------------------------------------------

    def do_load(self, arg_str):
        """Loads a graph from a BCF file into the current context (overwriting it)."""
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        args = arg_str.split()

        if len(args) != 1:
            raise ArgumentError("Expected exactly 1 argument to load().")

        filename = args[0]
        parsed_graph = BCF_Parser.parse_bcf(filename)
        manager.update_context(parsed_graph)

        if verbose:
            print("\n\tgraph successfully loaded from \"{0}\"\n".format(filename))
        

    # DONE: Change the output format from ASP to BCF (after completing BCF_Formatter.py).
    def do_store(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        args = arg_str.split()

        graph = manager.current_context
        graph_name = manager.current_context_name

        if len(args) != 1:
            raise ArgumentError("Expected exactly 1 argument to store().")

        filename = args[0]
        if os.path.isfile(filename):
            confirm_overwrite = self.yes_or_no(("\tFile \"{0}\" already exists. Do you want to overwrite it? (y/n) ")
                                         .format(filename))

            if not confirm_overwrite:
                print("\n\t\"{0}\" left unchanged.\n".format(filename))
                return

        f = open(filename, 'w')
        f.write(BCF_Formatter.convert_to_bcf(graph))
        if verbose:
            print("\n\tSuccessfully saved graph {0} to {1}.\n".format(graph_name, filename))
        

    def yes_or_no(self, question):
        yes_answers = ['yes', 'y']
        no_answers  = ['no', 'n']

        answer = input(question)
        while answer not in (yes_answers + no_answers):
            print("\t\"{0}\" is not a valid response.".format(answer))
            answer = input(question)

        if answer in yes_answers:
            return True
        return False 




    # Belief Change Operations
    # -----------------------------------------------------------------------
    # TODO: Needs checking for EquibelGraph
    def do_completion(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        graph = manager.current_context

        new_graph = eb.completion(graph, method=solving_method)
        manager.update_context(new_graph)

        if verbose:
            print("\n\tOne-shot belief change completed:")
            print("\t---------------------------------")
            self.print_all_formulas()


    def do_cardinality(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        solving_method = eb.CARDINALITY
        if verbose:
            print("\n\tNow using cardinality-maximal EQ sets.\n")


    def do_containment(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        solving_method = eb.CONTAINMENT
        if verbose:
            print("\n\tNow using containment-maximal EQ sets.\n")


    # TODO: Needs checking for EquibelGraph
    def do_iterate(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        args = arg_str.split()

        steady_state = False

        if len(args) == 0:
            num_iterations = 1
        elif len(args) == 1:
            num_str = args[0]
            if num_str.isdigit():
                num_iterations = int(num_str)
            else:
                if num_str == 'steady':
                    steady_state = True
                else:
                    raise ArgumentError("The number of iterations must be an integer: \"{0}\"".format(num_str))
        else:
            raise ArgumentError("Expected 0 or 1 argument to iterate()!\ Usage: iterate [NUM_ITERATIONS]")

        graph = manager.current_context

        if steady_state:
            new_graph, num_iterations = eb.iterate_steady(graph)
        else:
            new_graph = eb.iterate(graph, num_iterations)

        manager.update_context(new_graph)

        if verbose:
            if num_iterations == 1:
                print("\n\t1 iteration completed:")
                print("\t----------------------")
                self.print_all_formulas()
            else:
                print("\n\t{0} iterations completed:".format(num_iterations))
                print("\t-----------------------")
                self.print_all_formulas()


    # TODO: Needs checking for EquibelGraph
    def do_e_iterate(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        args = arg_str.split()

        if len(args) == 0:
            num_iterations = 1
        elif len(args) == 1:
            num_str = args[0]
            if not num_str.isdigit():
                raise ArgumentError("The number of iterations must be an integer: \"{0}\"".format(num_str))
            num_iterations = int(num_str)
        else:
            raise ArgumentError("Expected 0 or 1 argument to iterate()!\ Usage: iterate [NUM_ITERATIONS]")

        graph = manager.current_context
        #new_graph = solver.expanding_iteration(graph, num_iterations, solver.CONTAINMENT)
        solver.expanding_iteration(graph, num_iterations, solver.CONTAINMENT)
        #manager.update_context(new_graph)

        if verbose:
            if num_iterations == 1:
                print("\n\t1 iteration completed.\n")
            else:
                print("\n\t{0} iterations completed.\n".format(num_iterations))


    # Shell Functions -- (To help locate files to load.)
    # -----------------------------------------------------------------------

    def do_shell(self, arg_str):
        proc = Popen(arg_str, shell=True, stdout=PIPE, universal_newlines=True)
        for line in proc.stdout:
            line = line.strip()
            print(line)

    
    def do_quit(self, args):
        """Quits the program."""
        print("Bye!")
        raise SystemExit


def cli():
    print("Equibel Version 0.9.1 (Alpha)")

    print(Fore.GREEN + Style.BRIGHT)

    print("""
                                       ..                    ..
                                       ||                    ||
   ______     _______   ..      ..  ** ||_____      ______   || **
 //`````\\\\   //`````\\\\  ||      ||  || ||````\\\\   //`````\\\\  || ||
||_______|| ||       || ||      ||  || ||     || ||_______|| || ||
||````````  ||       || ||      ||  || ||     || ||````````  || ||
 \\\\______    \\\\_____//|  \\\\____//|  || ||____//   \\\\______   || ||
  ```````     ```````||   `````` \\\\ `` ```````     ```````   `` ``
                     ||
                      \\\\
                       ``
    """)

    print(Fore.RESET + Style.RESET_ALL)

    prompt = EquibelPrompt(completekey='tab')
    prompt.prompt = "equibeli (g) > "

    while True:
        try:
            prompt.cmdloop()
        except Exception as err:
            print(err)


if __name__ == '__main__':
    cli()
