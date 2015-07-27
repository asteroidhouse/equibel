import sys
from collections import defaultdict

import gringo

@profile
def on_model(model):
    #print(model)
    pass

@profile
def on_finish(res, canceled):
    print(res, canceled)

@profile
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

    node_models = defaultdict(set)

    with ctl.solve_iter() as it:
        for m in it:
            node_tv_dict = defaultdict(int)
            terms = m.atoms(gringo.Model.SHOWN)
            for term in terms:
                if term.name() == 'tv':
                    node, atom_index, truth_value = term.args()
                    node_tv_dict[node] |= truth_value << atom_index
            for node in node_tv_dict:
                node_models[node].add(node_tv_dict[node])
        print(node_models)
    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: model_inspect.py FILENAME")
        sys.exit(1)

    filename = sys.argv[1]
    run_solver(filename)
