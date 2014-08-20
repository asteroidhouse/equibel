class ManagerError(Exception): pass

class GraphManager:
     def __init__(self):
          self.graphs = dict()
          self.current_context = None
          self.current_context_name = None

     def __iter__(self):
          return iter(self.graphs)

     def __getitem__(self, key):
          return self.graphs.get(key, None)

     def add(self, graph_name, graph):
          self.graphs[graph_name] = graph
          # The first graph added to the manager becomes the current context automatically.
          if not self.current_context:
               self.current_context = graph
               self.current_context_name = graph_name

     def update_context(self, graph):
          self.graphs[self.current_context_name] = graph
          self.current_context = graph
     
     def remove(self, graph_name):
          if graph_name not in self.graphs:
               raise ManagerError("graph \"{0}\" does not exist".format(graph_name))
          del self.graphs[graph_name]

     def set_context(self, graph_name):
          if graph_name not in self.graphs:
               raise ManagerError("graph \"{0}\" does not exist".format(graph_name))
          self.current_context = self.graphs[graph_name]
          self.current_context_name = graph_name
