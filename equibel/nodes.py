from equibel.runtime import *

class RootNode:
     def __init__(self, nodes=[]):
          self.nodes = nodes

     def append(self, node):
          # To avoid reversing the input sequence when building the AST.
          self.nodes = [node] + self.nodes
          return self

     def evaluate(self, context):
          ret_val = None
          for node in self.nodes:
               ret_val = node.evaluate(context)
          return ret_val

     def __str__(self):
          s = ""
          for node in self.nodes:
               s += str(node) + "\n"
          return s

class LiteralNode:
     def __init__(self, value):
          self.value = value

     def evaluate(self, context):
          if isinstance(self.value, int):
               return Runtime["Number"].new_value(self.value)
          elif isinstance(self.value, str):
               return Runtime["String"].new_value(self.value)
          elif isinstance(self.value, tuple):
               return Runtime["OrderedPair"].new_value(self.value)
          elif isinstance(self.value, list):
               return Runtime["Set"].new_value(set(item.evaluate(context).python_value for item in self.value))
          elif isinstance(self.value, RangeNode):
               return Runtime["Set"].new_value(set(self.value.evaluate(context)))
          else:
               raise ValueError("Unknown literal type: " + str(type(a)))

     def __str__(self):
          if isinstance(self.value, list):
               s = ""
               for item in self.value:
                    s += str(item.value)
               return s
          else:
               return str(self.value)

class RangeNode:
     def __init__(self, start, end):
          self.start = start
          self.end = end

     def evaluate(self, context):
          try:
               start_int = int(self.start)
               end_int = int(self.end)
               return list(range(start_int, end_int + 1))
          except Exception as err:
               raise ValueError("Cannot construct non-numeric range: {0}..{1}".format(self.start, self.end))

class CallNode:
     def __init__(self, receiver, method, arguments=[]):
          self.receiver = receiver
          self.method = method
          self.arguments = arguments

     def evaluate(self, context):
          if self.receiver is None and self.method in context.locals:
               return context.locals[self.method]
          else:
               if self.receiver:
                    receiver = self.receiver.evaluate(context)
               else:
                    receiver = context.current_self

               arguments = list(map(lambda arg: arg.evaluate(context), self.arguments))
               return receiver.call(self.method, arguments)

     def __str__(self):
          return "{0}.{1}({2})".format(self.receiver, self.method, list(str(arg) for arg in self.arguments))


class SetLocalNode:
     def __init__(self, name, value):
          self.name = name
          self.value = value

     def evaluate(self, context):
          context.locals[self.name] = self.value.evaluate(context)
          return context.locals[self.name]

     def __str__(self):
          return "{0} = {1}".format(self.name, self.value)

# TODO: Could possibly replace this with another call to CallNode.
class ModAssignNode:
     def __init__(self, name, assign_operator, value):
          self.name = name
          self.assign_operator = assign_operator
          self.value = value

     def evaluate(self, context):
          original_object = context.locals.get(self.name)
          if original_object is None:
               context.locals[self.name] = self.value.evaluate(context)
          else:
               argument = self.value.evaluate(context)
               if self.assign_operator == '+=':
                    result_object = original_object.call("mod_add", argument)
               elif self.assign_operator == '-=':
                    result_object = original_object.call("mod_subtract", argument)
               context.locals[self.name] = result_object

          return context.locals[self.name]

     def __str__(self):
          return "{0} {1} {2}".format(self.name, self.assign_operator, self.value)
