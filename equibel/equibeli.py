from __future__ import absolute_import
from __future__ import print_function

import sys
import os
import readline
from cmd import Cmd
from subprocess import Popen, PIPE

import equibel.ASP_Formatter as ASP_Formatter
import equibel.BCF_Formatter as BCF_Formatter
import equibel.Simplified_Parser4 as Parser

from equibel.graph import Graph

import equibel.CmdLineParser as CmdLineParser
import equibel.FormulaParserSim as FormulaParserSim

import equibel.BCF_Parser as BCF_Parser

from equibel.simbool.proposition import *
from equibel.simbool.simplify import *

import equibel.SolverInterface as SolverInterface
from equibel.graph_manager import GraphManager

class ArgumentError(Exception): pass
    
manager = GraphManager()
g = Graph()
manager.add('g', g)

cardinality_maximal = False

class EquibelPrompt(Cmd):


    def check_silencing_terminator(self, arg_str):
        """Checks if arg_str ends with a 'silencing' terminator, such as 
           a semicolon. If it does, this function strips off the terminator 
           and returns the modified string, as well as the boolean True to 
           indicate that the output should be silenced. If it does not, this 
           function returns the string unmodified, as well as the boolean 
           False to indicate that the output should not be silenced."""
        verbose = True
        arg_str = arg_str.strip()
        if arg_str.endswith(';'):
            arg_str = arg_str[:-1]
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

    # TODO: Not finished.
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
            print("\n\tnodes: []\n")
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
                raise ValueError("add_node requires an integer argument!")
            else:
                graph.add_node(int(node_str))
                if verbose:
                    self.print_nodes()


    def do_add_nodes(self, arg_str):
        """Adds all the nodes from a list to the current context."""
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        graph = manager.current_context

        try:
            node_list = CmdLineParser.parse_list(arg_str)
            for node_num in node_list:
                graph.add_node(node_num)
        except Exception as err:
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
    

    def do_remove_nodes(self, arg_str):
        """Removes all the nodes in a list from the nodes set."""
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        graph = manager.current_context
        
        nodes = CmdLineParser.parse_list(arg_str)
        graph.remove_nodes(nodes)

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
        """Adds an edge to the edges set."""
        arg_str, verbose = self.check_silencing_terminator(arg_str)

        try:
            edge = CmdLineParser.parse_tuple(arg_str)
            self.add_edge(edge)
            if verbose:
                self.print_edges()
        except Exception as err:
            print(err)


    def do_add_edges(self, arg_str):
        """Adds all the edges in a list to the edges set."""
        arg_str, verbose = self.check_silencing_terminator(arg_str)

        try:
            edge_list = CmdLineParser.parse_list(arg_str)
            for edge in edge_list:
                self.add_edge(edge)
            
            if verbose:
                self.print_edges()
        except Exception as err:
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
            edge = CmdLineParser.parse_tuple(arg_str)
            graph.remove_edge(edge)
            if verbose:
                self.print_edges()
        except Exception as err:
            print(err)


    # Directed/Undirected Functions
    #--------------------------------------------------------------------------------
    
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
    #--------------------------------------------------------------------------------

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
            atom_list = CmdLineParser.parse_list(arg_str)
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
        """Prints the atoms in the alphabet of the current context."""
        atoms = manager.current_context.get_atoms()
        if not atoms:
            print("\n\tatoms: {}\n")
        else:
            print("\n\tatoms: {0}\n".format(atoms))
        

    # Weight Functions
    #--------------------------------------------------------------------------------

    # TODO: These are sort of temporary in their current form.
    def do_add_weight(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        args = arg_str.split()
        # DONE: Finish this function, with error checking.
        if len(args) != 3:
            raise ArgumentError("Expected 3 arguments to add_weight!\nusage: add_weight NODE_NUM ATOM WEIGHT")

        node_str, atom, weight_str = args
        if not node_str.isdigit():
            raise ArgumentError("The node identifier must be an integer: \"{0}\"".format(node_str))
        if not weight_str.isdigit():
            raise ArgumentError("The weight must be an integer: \"{0}\"".format(weight_str))

        node = int(node_str)
        weight = int(weight_str)
        manager.current_context.add_weight(node, atom, weight)

        if verbose:
            self.print_weights(node)


    def print_weights(self, node_num):
        weights = manager.current_context.get_weights(node_num)
        
        print()
        print("\tnode {0}:".format(node_num))
        for atom in weights:
            print("\t\t{0}: {1}".format(atom, weights[atom]))
        print()


    def print_all_weights(self):
        nodes = manager.current_context.get_nodes()
        
        print()
        for node in nodes:
            print("\tnode {0}:".format(node))
            weights = manager.current_context.get_weights(node)
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
                raise ArgumentError("the node identifier must be an integer: \"{0}\"".format(node_str))
            if verbose:
                self.print_weights(int(node_str))
        else:
            raise ArgumentError("Expected 0 or 1 argument to weights!\nusage: weights [NODE_NUM]")


    # Formula Functions
    #--------------------------------------------------------------------------------

    def do_add_formula(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        #args = arg_str.split(maxsplit=1)
        # Python2 version of split does not accept keywork args, so we use:
        args = arg_str.split(None, 1)

        if len(args) != 2:
            raise ArgumentError("Expected exactly 2 arguments to add_formula.\nusage: add_formula NODE_NUM FORMULA")

        node_str, formula_str = args

        if not node_str.isdigit():
            raise ArgumentError("The node identifier must be an integer.")

        node_num = int(node_str)
        formula = FormulaParserSim.parse_formula(formula_str)
        manager.current_context.add_formula(node_num, formula)

        if verbose:
            self.print_formulas(node_num)

    def do_remove_formula(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        #args = arg_str.split(maxsplit=1)
        # Python2 version of split does not accept keywork args, so we use:
        args = arg_str.split(None, 1)

        if len(args) != 2:
            raise ArgumentError("Expected exactly 2 arguments to add_formula.\nusage: add_formula NODE_NUM FORMULA")

        node_str, formula_str = args

        if not node_str.isdigit():
            raise ArgumentError("The node identifier must be an integer.")

        node_num = int(node_str)
        formula = FormulaParserSim.parse_formula(formula_str)
        manager.current_context.remove_formula(node_num, formula)

        if verbose:
            self.print_formulas(node_num)
        
    
    def do_formulas(self, arg_str):
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

    def print_formulas(self, node_num):
        formulas = manager.current_context.get_formulas(node_num)
        
        print()
        print("\tnode {0}:".format(node_num))
        for formula in formulas:
            print("\t\t{0}".format(repr(formula)))
        print()


    def print_all_formulas(self):
        nodes = manager.current_context.get_nodes()
        
        print()
        for node in nodes:
            print("\tnode {0}:".format(node))
            formulas = manager.current_context.get_formulas(node)
            for formula in formulas:
                print("\t\t{0}".format(repr(formula)))
        print()
            
    # ASP Functions
    #--------------------------------------------------------------------------------

    def do_asp(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        graph = manager.current_context

        if verbose:
            print("\n" + ASP_Formatter.convert_to_asp(graph))
        


    # Load/Store Functions
    #--------------------------------------------------------------------------------
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
    #--------------------------------------------------------------------------------
    def do_one_shot(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        graph = manager.current_context
        new_graph = SolverInterface.one_shot(graph, cardinality_maximal)
        manager.update_context(new_graph)
        if verbose:
            print("\n\tOne-shot belief change completed.\n")


    def do_cardinality(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        cardinality_maximal = True
        if verbose:
            print("\n\tone_shot will use cardinality-maximal EQ sets.\n")

    def do_containment(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        cardinality_maximal = False
        if verbose:
            print("\n\tone_shot will use containment-maximal EQ sets.\n")
        

    def do_iterate(self, arg_str):
        arg_str, verbose = self.check_silencing_terminator(arg_str)
        args = arg_str.split()

        if len(args) == 0:
            num_iterations = 1
        elif len(args) == 1:
            num_str = args[0]
            if not num_str.isdigit():
                raise ArgumentError("the number of iterations must be an integer: \"{0}\"".format(num_str))
            num_iterations = int(num_str)
        else:
            raise ArgumentError("Expected 0 or 1 argument to iterate()!\nusage: iterate [NUM_ITERATIONS]")

        graph = manager.current_context
        new_graph = SolverInterface.iterate(graph, num_iterations, cardinality_maximal)
        manager.update_context(new_graph)

        if verbose:
            if num_iterations == 1:
                print("\n\t1 iteration completed.\n")
            else:
                print("\n\t{0} iterations completed.\n".format(num_iterations))

        

        
        

        



    # Shell Functions -- (To help locate files to load.)
    #--------------------------------------------------------------------------------

    def do_shell(self, arg_str):
        proc = Popen(arg_str, shell=True, stdout=PIPE, universal_newlines=True)
        for line in proc.stdout:
            line = line.strip()
            print(line)

    
    def do_quit(self, args):
        """Quits the program."""
        print("Bye!")
        raise SystemExit


if __name__ == '__main__':
    print("Equibel version 0.8.2")

    prompt = EquibelPrompt(completekey='tab')
    prompt.prompt = "equibel> "

    while True:
        try:
            prompt.cmdloop()
        except Exception as err:
            print(err)
