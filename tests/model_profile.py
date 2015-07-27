import sys

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
    #ctl.solve()

    #f = ctl.solve_async(on_model=on_model, on_finish=on_finish)
    #f.wait()
    
    models = defaultdict(set)
    node_tv_dict = defaultdict(dict)
    
    with ctl.solve_iter() as it:
        for m in it:
            node_tv_dict.clear()
            terms = m.atoms(gringo.Model.SHOWN)
            for term in terms:
                if term.name() == 'tv':
                    #node, atom_fun, truth_value = term.args()
                    #atom = str(atom_fun)
                    node, atom, truth_value = term.args()
                    node_tv_dict[node][atom] = truth_value
                    #print(node_tv_dict)
            for node in node_tv_dict:
                if node not in models:
                    models[node] = set()
                models[node].add(frozenset(node_tv_dict[node].items()))
        print(models)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: model_inspect.py FILENAME")
        sys.exit(1)

    filename = sys.argv[1]
    run_solver(filename)
