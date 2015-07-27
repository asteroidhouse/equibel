import sys
from collections import defaultdict
from mem_top import mem_top
from pympler.tracker import SummaryTracker
import gc
import objgraph

import gringo

def on_model(model):
    #print(model)
    pass

def on_finish(res, canceled):
    print(res, canceled)

def dump_garbage():
    """
    show us what's the garbage about
    """
        
    # force collection
    print "\nGARBAGE:"
    gc.collect()

    print "\nGARBAGE OBJECTS:"
    for x in gc.garbage:
        s = str(x)
        if len(s) > 80: s = s[:80]
        print type(x),"\n  ", s

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
    #ctl.solve()

    #f = ctl.solve_async(on_model=on_model, on_finish=on_finish)
    #f.wait()
    models = defaultdict(set)
    node_tv_dict = defaultdict(dict)

    with ctl.solve_iter() as it:
        for m in it:
            #gc.collect()
            node_tv_dict.clear()
            for term in m.atoms(gringo.Model.SHOWN):
                if term.name() == 'tv':
                    #node, atom_fun, truth_value = term.args()
                    #atom = str(atom_fun)
                    node, atom, truth_value = term.args()
                    #if node not in node_tv_dict:
                    #    node_tv_dict[node] = dict()
                    node_tv_dict[node][atom] = truth_value
                    #print(node_tv_dict)
            for node in node_tv_dict:
                models[node].add(frozenset(node_tv_dict[node].items()))
            #gc.collect()
            objgraph.show_most_common_types()
        print(models)
    
    """
    with ctl.solve_iter() as it:
        for m in it:
            print(m.atoms(gringo.Model.SHOWN))
        #print(d)
    """

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: model_inspect.py FILENAME")
        sys.exit(1)
    
    gc.enable()
    gc.set_debug(gc.DEBUG_LEAK)

    filename = sys.argv[1]
    run_solver(filename)