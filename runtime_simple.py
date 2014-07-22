class AwesomeObject:
     def __init__(self, runtime_class, python_value=None):
          if python_value is None:
               python_value = self
          
          self.runtime_class = runtime_class
          self.python_value = python_value

     def call(self, method, arguments):
          self.runtime_class.lookup(method)(self, arguments)
     
class AwesomeClass(AwesomeObject):
     def __init__(self):
          super().__init__(AwesomeObject)
          self.methods = {}

     def lookup(self, method_name):
          try:
               method = self.methods[method_name]
               return method
          except Exception as err:
               print(err)

     def new(self):
          return AwesomeObject(self)

     def new_value(self, value):
          return AwesomeObject(self, value)

class AwesomeMethod:
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
awesome_class = AwesomeClass()
awesome_class.runtime_class = awesome_class
object_class = AwesomeClass()
object_class.runtime_class = awesome_class

Runtime = EvalContext(object_class.new())

Runtime["Class"]  = awesome_class
Runtime["Object"] = object_class

Runtime["Number"] = AwesomeClass()
Runtime["String"] = AwesomeClass()
Runtime["OrderedPair"] = AwesomeClass()
Runtime["List"] = AwesomeClass()

def print_function(receiver, arguments):
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
