class EquibelObject:
     def __init__(self, runtime_class, python_value=None):
          if python_value is None:
               python_value = self
          
          self.runtime_class = runtime_class
          self.python_value = python_value

     def call(self, method, arguments):
          return self.runtime_class.lookup(method)(self, arguments)

     # For results at the interactive prompt.
     def __str__(self):
          return str(self.python_value)
     
class EquibelClass(EquibelObject):
     def __init__(self):
          super().__init__(EquibelObject)
          self.methods = {}

     def lookup(self, method_name):
          try:
               method = self.methods[method_name]
               return method
          except Exception as err:
               print(err)

     def new(self):
          return EquibelObject(self)

     def new_value(self, value):
          return EquibelObject(self, value)

class EquibelMethod:
     def __init__(self, params, body):
          self.params = params
          self.body = body

     def call(self, receiver, arguments):
          self.body.evaluate(Context(receiver))

class EvalContext:
     constants = {}

     def __init__(self, current_self, current_class=None):
          if current_class is None:
               current_class = current_self.runtime_class

          self.locals = {}
          self.current_self = current_self
          self.current_class = current_class

     def __getitem__(self, name):
          return EvalContext.constants[name]
     
     def __setitem__(self, name, value):
          EvalContext.constants[name] = value


# Bootstrap the runtime
equibel_class = EquibelClass()
equibel_class.runtime_class = equibel_class
object_class = EquibelClass()
object_class.runtime_class = equibel_class

Runtime = EvalContext(object_class.new())

Runtime["Class"]  = equibel_class
Runtime["Object"] = object_class

Runtime["Number"]        = EquibelClass()
Runtime["String"]        = EquibelClass()
Runtime["OrderedPair"]   = EquibelClass()
Runtime["List"]          = EquibelClass()

def print_function(receiver, arguments):
     #print("Print arguments: ", arguments)
     if len(arguments) > 0:
          for arg in arguments:
               print(arg.python_value)
     return None

nodes_list = []
def add_node_function(receiver, arguments):
     if len(arguments) == 1:
          arg = arguments[0].python_value
          if isinstance(arg, int):
               nodes_list.append(arg)
          else:
               raise Exception("Argument to add_node must be an integer.")
          print(nodes_list)
     else:
          raise Exception("Incorrect number of arguments to add_node.")

def add_nodes_function(receiver, arguments):
     if len(arguments) == 1:
          arg_list = arguments[0].python_value
          if isinstance(arg_list, list):
               for item in arg_list:
                    if isinstance(item, int):
                         nodes_list.append(item)
                    else:
                         raise Exception("All items in the list passed to add_nodes must be integers.")
          else:
               raise Exception("Argument to add_node must be a list.")
          print(nodes_list)
     else:
          raise Exception("Incorrect number of arguments to add_node.")

def remove_node_function(receiver, arguments):
     if len(arguments) == 1:
          arg = arguments[0].python_value
          if isinstance(arg, int):
               nodes_list.remove(arg)
          else:
               raise Exception("Argument to remove_node must be an integer.")
          print(nodes_list)
     else:
          raise Exception("Incorrect number of arguments to add_node")



Runtime["Class"].methods["new"] = lambda receiver, arguments: receiver.new()

Runtime["Object"].methods["print"] = print_function
Runtime["Object"].methods["add_node"] = add_node_function
Runtime["Object"].methods["add_nodes"] = add_nodes_function
Runtime["Object"].methods["remove_node"] = remove_node_function





def add_numbers(receiver, arguments):
     #print("reciever: {0}, arguments: {1}".format(receiver, arguments[0]))
     result = receiver.python_value + arguments[0].python_value
     #print("RESULT", result)
     return Runtime["Number"].new_value(result)

def add_strings(receiver, arguments):
     result = receiver.python_value + arguments[0].python_value
     return Runtime["String"].new_value(result)

def add_lists(receiver, arguments):
     result = list(set(receiver.python_value + arguments[0].python_value))
     return Runtime["List"].new_value(result)

Runtime["Number"].methods["+"] = add_numbers
Runtime["String"].methods["+"] = add_strings
Runtime["List"].methods["+"] = add_lists


def subtract_numbers(receiver, arguments):
     result = receiver.python_value - arguments[0].python_value
     return Runtime["Number"].new_value(result)

Runtime["Number"].methods["-"] = subtract_numbers
