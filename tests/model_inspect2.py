from __future__ import print_function
import sys
from collections import defaultdict
import gc
import objgraph

from guppy import hpy

from sys import getsizeof, stderr
from itertools import chain
from collections import deque
try:
    from reprlib import repr
except ImportError:
    pass
    

import gringo
from gringo import Model

def on_model(model):
    model.atoms(Model.SHOWN)

def on_finish(res, canceled):
    print(res, canceled)

def total_size(o, handlers={}, verbose=False):
    """ Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    """
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                   }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        #if id(o) in seen:       # do not double count the same object
        #    return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)

def run_solver(filename):
    ctl = gringo.Control()
    #ctl.conf.configuration = 'jumpy'
    ctl.conf.solver.heuristic = 'domain'
    ctl.conf.solve.enum_mode = 'domRec'
    ctl.conf.solve.models = 0
    #ctl.conf.solve.parallel_mode = 2

    ctl.load('eq_sets.lp')
    ctl.load(filename)

    ctl.ground([('base', [])])
    
    ctl.solve(on_model=on_model)

    node_models = defaultdict(set)
    node_tv_dict = defaultdict(int)
    
    #hp = hpy()
    print("Heap at the beginning:")
    #print(hp.heap())
    #it = ctl.solve_iter()
    #atoms = []
    #for m in it:
        #print(hp.heap())
        #terms = 
        #print(type(terms))
        #print(total_size(terms))
        #m.atoms(2)
        #for term in terms:
        #    pass
        
        #print(hp.heap())
    """
        #print(hp.heap())
        #node_tv_dict = defaultdict(int)
        node_tv_dict.clear()
        #terms = 
        #print("Size of m: {0}".format(total_size(terms)))
        for term in m.atoms(gringo.Model.SHOWN):
            #print(hp.heap())
            if term.name() == 'tv':
                node, atom_index, truth_value = term.args()
                node_tv_dict[node] |= truth_value << atom_index
       
        for node in node_tv_dict:
            node_models[node].add(node_tv_dict[node])
        del node_tv_dict
        #gc.collect()
        #print("OBJECTS")
        #objgraph.show_most_common_types()
    print(node_models)
    print("Size = {0}".format(total_size(node_models)))
    print("Heap at the end")
    """
    



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: model_inspect.py FILENAME")
        sys.exit(1)

    filename = sys.argv[1]
    run_solver(filename)
