from __future__ import absolute_import

import sys
from collections import defaultdict
from functools import wraps
import copy
import platform
import pkg_resources

import gringo

import equibel as eb

if platform.system() == 'Linux':
    if platform.architecture()[0] == '64bit':
        if platform.dist()[0] in ['centos', 'CentOS']:
            import equibel.includes.linux.bit64.centos.gringo as gringo
            from equibel.includes.linux.bit64.centos.gringo import Control, Model, Fun
        else:
            import equibel.includes.linux.bit64.gringo as gringo
            from equibel.includes.linux.bit64.gringo import Control, Model, Fun
    elif platform.architecture()[0] == '32bit':
        import equibel.includes.linux.bit32.gringo as gringo
        from equibel.includes.linux.bit32.gringo import Control, Model, Fun
elif platform.system() == 'Darwin':
    import equibel.includes.mac.gringo as gringo
    from equibel.includes.mac.gringo import Control, Model, Fun

import equibel.FormulaExtractor as FormulaExtractor
import equibel.formatters.ASP_Formatter as ASP_Formatter
#from equibel.simbool.simplify import simplify

EQ_SETS_FILE = pkg_resources.resource_filename('equibel', 'asp/eq_sets.lp')

CONTAINMENT = 0
CARDINALITY = 1

def completion(G, method=CONTAINMENT):
    atoms = [eb.Prop(atom) for atom in G.atoms()]
    sorted_atoms = tuple(sorted(atoms))

    ctl = gringo.Control()
    #ctl.conf.configuration = 'handy'
    ctl.conf.solver.heuristic = 'domain'
    ctl.conf.solve.enum_mode = 'domRec'
    ctl.conf.solve.models = 0
    #ctl.conf.solve.parallel_mode = 2

    ctl.load(EQ_SETS_FILE)
    ctl.add('base', [], eb.convert_to_asp(G))
    ctl.ground([('base', [])])

    node_models = defaultdict(set)
    node_tv_dict = defaultdict(int)
    
    it = ctl.solve_iter()
    for m in it:
        node_tv_dict.clear()
        terms = m.atoms(gringo.Model.SHOWN)
        for term in terms:
            if term.name() == 'tv':
                node, atom_index, truth_value = term.args()
                node_tv_dict[node] |= truth_value << atom_index
       
        for node in node_tv_dict:
            node_models[node].add(node_tv_dict[node])
    print(node_models)
    
    R = copy.deepcopy(G)
    for node in node_models:
        t = tuple(node_models[node])
        formula = formula_from_models(t, sorted_atoms)
        print(repr(formula))
        simple = simplify(formula)
        R.set_formulas(node, [simple])
    return R


def memo(func):
    cache = {}
    @wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap


@memo
def simplify(formula):
    return eb.simplify(formula)


@memo
def formula_from_models(models, atoms):
    disjunction = eb.Prop(False)
    for model in models:
        disjunction |= formula_from_model(model, atoms)
    return disjunction


@memo
def formula_from_model(model, atoms):
    """Creates a propositional formula from a (single) model.
       
       The input model must be an integer whose bits represent
       the truth values of atoms in a given sorted order.

       For example, given an alphabet A = {p, q, r}, and a 
       model 6 = 110 (base 2), the formula returned by this 
       function is p & q & ~r.
    """
    conjunction = eb.Prop(True) 
    for (index, atom) in enumerate(atoms):
        truth_value = model & (1 << index)
        if truth_value:
            conjunction &= atom
        else:
            conjunction &= ~atom
    return conjunction


def revise(K, R):
    G = equibel.path_graph(2)

    if isinstance(K, str):
        G.add_formula(0, equibel.parse_infix_formula(K))
    elif isinstance(K, list):
        for belief in K:
            G.add_formula(0, equibel.parse_infix_formula(belief))

    if isinstance(R, str):
        G.add_formula(1, equibel.parse_infix_formula(R))
    elif isinstance(R, list):
        for belief in R:
            G.add_formula(1, equibel.parse_infix_formula(belief))

    S = completion(G)
    return S.formulas(1)

def proj_merge(belief_bases, entailment_constraint=None):
    G = equibel.star_graph(len(belief_bases))

    if entailment_constraint:
        G.add_formula(0, entailment_constraint)

    for (i, belief_base) in enumerate(belief_bases, 1):
        G.add_formula(i, belief_base)

    S = completion(G)
    return S.formulas(0)
    

def con_merge(belief_bases, entailment_based_constraints=None, consistency_based_constraints=None):
    pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python solver.py NUM_NODES")
        sys.exit(1)
    
    num_nodes = int(sys.argv[1])
    
    solver = EqSolver()
    G = equibel.path_graph(num_nodes)
    G.add_formula(0, "p & q & r & s")
    G.add_formula(num_nodes-1, "~p & ~q & ~r & ~s")
    R = completion(G)
    for node_id in R.nodes():
        print("Node {0}, formulas = {1}".format(node_id, R.formulas(node_id)))
