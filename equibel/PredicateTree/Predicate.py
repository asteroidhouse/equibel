class Predicate:
    def __init__(self, name, children=[]):
        self.name = name
        self.children = children

    def __str__(self):
        return "{0}({1})".format(self.name, ",".join([str(child) for child in self.children]))
