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

def print_function(receiver, arguments):
     if len(arguments) > 0:
          for arg in arguments:
               print(arg.python_value)
     return None


Runtime["Class"].methods["new"] = lambda receiver, arguments: receiver.new()

Runtime["Object"].methods["print"] = print_function
