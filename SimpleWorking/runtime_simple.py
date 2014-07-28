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
Runtime["Set"]           = EquibelClass()


Runtime["Class"].methods["new"] = lambda receiver, arguments: receiver.new()
