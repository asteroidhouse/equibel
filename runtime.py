class AwesomeObject:
     def __init__(self, awesome_class, python_value=None):
          if python_value is None:
               python_value = self
          self.awesome_class = awesome_class
          self.python_value  = python_value
     
     def call(self, method, arguments):
          self.awesome_class.lookup(method).call(self, arguments)

class AwesomeClass(AwesomeObject):
     def __init__(self):
          #if 'Runtime' in vars() or 'Runtime' in globals():
          try:
               awesome_class = Runtime["Class"]
          except NameError:
               awesome_class = None
               print("It wasn't defined.")
          
          super(awesome_class)

          self.awesome_methods = {}

     def lookup(self, method_name):
          method = self.awesome_methods[method_name]
          if method is None:
               raise Exception("Method not found: {0}".format(method_name))
          return method

     def __new__(cls):
          return AwesomeObject(cls)

     @classmethod
     def new_value(cls, value):
          return AwesomeObject(cls, value)

class AwesomeMethod:
     def __init__(self, params, body):
          self.params = params
          self.body = body

     def call(self, receiver, arguments):
          self.body.evaluate(Context(receiver))

class Context:
     constants = {}

     def __init__(self, current_self, current_class=None):
          if current_class is None:
               current_class = current_self.awesome_class

          self.locals = {}
          self.current_self = current_self
          self.current_class = current_class

     def __getitem__(self, name):
          return Context.constants[name]

     def __setitem__(self, name, value):
          Context.constants[name] = value

awesome_class = AwesomeClass()
awesome_class.awesome_class = awesome_class
awesome_object_class = AwesomeClass()

#Runtime = Context(awesome_object_class.class.__new__())
Runtime = Context(AwesomeClass())

Runtime["Class"]  = awesome_class
Runtime["Object"] = awesome_object_class
Runtime["Number"] = AwesomeClass()
Runtime["String"] = AwesomeClass()


def print_function(receiver, arguments):
     if len(arguments) > 0:
          print(arguments[0])
     return None

Runtime["Object"].awesome_methods["print"] = print_function
