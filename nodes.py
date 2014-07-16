class Nodes:
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
               Runtime["Number"].new_value(self.value)
          elif isinstance(self.value, str):
               Runtime["String"].new_value(self.value)
          elif isinstance(self.value, tuple):
               Runtime["OrderedPair"].new_value(self.value)
          elif isinstance(self.value, list):
               Runtime["List"].new_value(self.value)
          else:
               raise ValueError("Unknown literal type: " + str(type(a)))

     def __str__(self):
          return str(self.value)

class CallNode:
     def __init__(self, receiver, method, arguments=[]):
          self.receiver = receiver
          self.method = method
          self.arguments = arguments

     def evaluate(self, context):
          if self.receiver is None and context.local[self.method]:
               return context.local[self.method]
          else:
               if self.receiver:
                    receiver = self.receiver.evaluate(context)
               else:
                    receiver = context.current_self

               arguments = map(lambda arg: arg.evaluate(context), self.arguments)
               receiver.call(self.method, arguments)

     def __str__(self):
          return "{0}.{1}({2})".format(self.receiver, self.method, list(map(str, self.arguments)))


#TODO: What else needs to be added to this class?
class ConstructorNode:
     def __init__(self, constructor, arguments=[]):
          self.constructor = constructor
          self.arguments = arguments

     # TODO: Check if this works. Not sure about it, because I haven't made the 
     #       runtime class yet.
     #-------------------------------------------------------------------------
     def evaluate(self, context):
          receiver = context.current_self
          arguments = map(lambda arg: arg.evaluate(context), self.arguments)
          receiver.call_constructor(self.constructor, arguments)

     def __str__(self):
          return "{0}({1})".format(self.constructor, list(map(str, self.arguments)))

     
class SetLocalNode:
     def __init__(self, name, value):
          self.name = name
          self.value = value

     def evaluate(self, context):
          context.local[self.name] = selv.value.evaluate(context)

     def __str__(self):
          return "{0} = {1}".format(self.name, self.value)
