from runtime_simple import *

#---------------------------------------------------------------------------------
#                        Printing Functions
#---------------------------------------------------------------------------------
def print_function(receiver, arguments):
     if len(arguments) > 0:
          for arg in arguments:
               print(arg.python_value)
     return None


Runtime["Object"].methods["print"] = print_function


def show_graphs():
     # print the names of all the existing graphs, and show which is the 
     # current context:
     # 
     #    g, --g2-- (context)
     pass



#---------------------------------------------------------------------------------
#                        Addition Functions
#---------------------------------------------------------------------------------
def add_numbers(receiver, arguments):
     result = receiver.python_value + arguments[0].python_value
     return Runtime["Number"].new_value(result)

def add_strings(receiver, arguments):
     result = receiver.python_value + arguments[0].python_value
     return Runtime["String"].new_value(result)

def add_sets(receiver, arguments):
     result = receiver.python_value.union(arguments[0].python_value)
     return Runtime["Set"].new_value(result)

Runtime["Number"].methods["+"] = add_numbers
Runtime["String"].methods["+"] = add_strings
Runtime["Set"].methods["+"] = add_sets



#---------------------------------------------------------------------------------
#                        Subtraction Functions
#---------------------------------------------------------------------------------
def set_difference(receiver, arguments):
     result = receiver.python_value.difference(arguments[0].python_value)
     return Runtime["Set"].new_value(result)
     
def subtract_numbers(receiver, arguments):
     result = receiver.python_value - arguments[0].python_value
     return Runtime["Number"].new_value(result)


Runtime["Number"].methods["-"] = subtract_numbers
Runtime["Set"].methods["-"] = set_difference



#---------------------------------------------------------------------------------
#              In-Place Addition (Mod Addition) Functions
#---------------------------------------------------------------------------------
def mod_add_numbers(receiver, argument):
     result = receiver.python_value + argument.python_value
     return Runtime["Number"].new_value(result)

def mod_add_strings(receiver, argument):
     result = receiver.python_value + argument.python_value
     return Runtime["String"].new_value(result)

def mod_set_union(receiver, argument):
     if receiver == Runtime.locals['nodes']:
          print("Should change graph structure.")
     result = receiver.python_value.union(argument.python_value)
     return Runtime["Set"].new_value(result)

     
Runtime["Number"].methods["mod_add"] = mod_add_numbers
Runtime["String"].methods["mod_add"] = mod_add_strings
Runtime["Set"].methods["mod_add"] = mod_set_union



#---------------------------------------------------------------------------------
#           In-Place Subtraction (Mod Subtraction) Functions
#---------------------------------------------------------------------------------
def mod_subtract_numbers(receiver, argument):
     result = receiver.python_value - argument.python_value
     return Runtime["Number"].new_value(result)

def mod_set_difference(receiver, argument):
     if receiver == Runtime.locals['nodes']:
          print("Should change graph structure.")
     result = receiver.python_value.difference(argument.python_value)
     return Runtime["Set"].new_value(result)
     
Runtime["Number"].methods["mod_subtract"] = mod_subtract_numbers
Runtime["Set"].methods["mod_subtract"] = mod_set_difference









Runtime.locals['edges'] = Runtime["Set"].new_value(set())
Runtime.locals['nodes'] = Runtime["Set"].new_value(set())





def add_node_function(receiver, arguments):
     if len(arguments) == 1:
          argument = arguments[0]
          if isinstance(argument.python_value, int):
               Runtime.locals['nodes'].python_value.add(argument.python_value)
               return Runtime.locals['nodes']
          else:
               raise Exception("Argument to add_node must be an integer.")
     else:
          raise Exception("Incorrect number of arguments to add_node.")


def add_nodes_function(receiver, arguments):
     if len(arguments) == 1:
          arg_list = arguments[0].python_value
          if isinstance(arg_list, set):
               if all(isinstance(item, int) for item in arg_list):
                    for item in arg_list:
                         Runtime.locals['nodes'].python_value.add(item)
                    return Runtime.locals['nodes']
               else:
                    raise Exception("All items in the list passed to add_nodes must be integers.")
          else:
               raise Exception("Argument to add_nodes must be a set.")
     else:
          raise Exception("Incorrect number of arguments to add_nodes.")


def remove_node_function(receiver, arguments):
     if len(arguments) == 1:
          argument = arguments[0]
          if isinstance(argument.python_value, int):
               Runtime.locals['nodes'].python_value.discard(argument.python_value)
               return Runtime.locals['nodes']
          else:
               raise Exception("Argument to remove_node must be an integer.")
     else:
          raise Exception("Incorrect number of arguments to add_node")


Runtime["Object"].methods["add_node"] = add_node_function
Runtime["Object"].methods["add_nodes"] = add_nodes_function
Runtime["Object"].methods["remove_node"] = remove_node_function

