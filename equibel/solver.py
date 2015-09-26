"""
"""
#    Copyright (C) 2014-2015 by
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.
from __future__ import absolute_import
from __future__ import print_function

import copy
from collections import defaultdict
from functools import wraps
import platform
import pkg_resources
import sys

import networkx as nx

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

import equibel.formatters.ASP_Formatter as ASP_Formatter


EQ_SETS_FILE = pkg_resources.resource_filename('equibel', 'asp/eq_sets.lp')
EQ_ITERATE_FILE = pkg_resources.resource_filename('equibel', 'asp/eq_iterate.lp')
EQ_IT_CONTAINMENT_FILE = pkg_resources.resource_filename('equibel', 'asp/eq_it_containment.lp')
EQ_IT_CARDINALITY_FILE = pkg_resources.resource_filename('equibel', 'asp/eq_it_cardinality.lp')

EQ_BASE_FILE = pkg_resources.resource_filename('equibel', 'asp/eq_base.lp')
EQ_CARDINALITY_FILE = pkg_resources.resource_filename('equibel', 'asp/eq_cardinality.lp')
EQ_CONTAINMENT_FILE = pkg_resources.resource_filename('equibel', 'asp/eq_containment.lp')

EXPANDING_FILE = pkg_resources.resource_filename('equibel', 'asp/expanding.lp')
EXPANDING_CONTAINMENT_FILE = pkg_resources.resource_filename('equibel', 'asp/expanding_containment.lp')
EXPANDING_CARDINALITY_FILE = pkg_resources.resource_filename('equibel', 'asp/expanding_cardinality.lp')

CONTAINMENT = 'containment'
CARDINALITY = 'cardinality'


def create_atom_mapping(atoms):
    """
    """
    mapping = dict()
    for (index, atom) in enumerate(atoms):
        mapping[atom] = index
    return mapping


def iterate_steady(G):
    atoms = [eb.Prop(atom) for atom in G.atoms()]
    sorted_atoms = tuple(sorted(atoms))

    atom_mapping = create_atom_mapping(sorted_atoms)

    iterations = 0

    old_R = None
    R = copy.deepcopy(G)

    while old_R != R:
        iterations += 1
        old_R = copy.deepcopy(R)
        ctl = gringo.Control()
        ctl.conf.configuration = 'crafty'
        ctl.conf.solver.heuristic = 'domain'
        ctl.conf.solve.enum_mode = 'domRec'
        ctl.conf.solve.models = 0
        #ctl.conf.solve.parallel_mode = 2

        #print(eb.convert_to_asp(R, atom_mapping))

        ctl.load(EQ_ITERATE_FILE)
        ctl.add('base', [], eb.convert_to_asp(R, atom_mapping))
        ctl.ground([('base', [])])

        node_models = defaultdict(set)
        node_tv_dict = defaultdict(int)
        
        it = ctl.solve_iter()
        for m in it:
            node_tv_dict.clear()
            terms = m.atoms(gringo.Model.SHOWN)
            for term in terms:
                if term.name() == 'tv':
                    center_node, node, atom_index, truth_value = term.args()
                    if center_node == node:
                        node_tv_dict[node] |= truth_value << atom_index
            
            for node in node_tv_dict:
                node_models[node].add(node_tv_dict[node])
        
        #print(node_models)

        true_prop = eb.Prop(True)

        for node in node_models:
            t = tuple(node_models[node])
            formula = formula_from_models(t, sorted_atoms)
            simp = simplified(formula)
            if simp != true_prop:
                R.set_formulas(node, [simp])

    return R, iterations


def load_iteration_files(ctl, method):
    ctl.load(EQ_ITERATE_FILE)
    if method == CONTAINMENT:
        ctl.load(EQ_IT_CONTAINMENT_FILE)
    elif method == CARDINALITY:
        ctl.load(EQ_IT_CARDINALITY_FILE)


def iterate(G, num_iterations=1, method=CARDINALITY):
    atoms = [eb.Prop(atom) for atom in G.atoms()]
    sorted_atoms = tuple(sorted(atoms))

    atom_mapping = create_atom_mapping(sorted_atoms)

    R = copy.deepcopy(G)

    for i in range(num_iterations):
        ctl = gringo.Control()
        configure_solver(ctl, method)
        load_iteration_files(ctl, method)

        ctl.add('base', [], eb.convert_to_asp(R, atom_mapping))
        ctl.ground([('base', [])])

        node_models = defaultdict(set)
        node_tv_dict = defaultdict(int)
        
        it = ctl.solve_iter()
        for m in it:
            node_tv_dict.clear()
            terms = m.atoms(gringo.Model.SHOWN)
            for term in terms:
                if term.name() == 'tv':
                    center_node, node, atom_index, truth_value = term.args()
                    if center_node == node:
                        node_tv_dict[node] |= truth_value << atom_index
           
            for node in node_tv_dict:
                node_models[node].add(node_tv_dict[node])
        
        #print(node_models)

        true_prop = eb.Prop(True)

        for node in node_models:
            t = tuple(node_models[node])
            formula = formula_from_models(t, sorted_atoms)
            simp = simplified(formula)
            if simp != true_prop:
                R.set_formulas(node, [simp])

    return R


def load_expanding_iteration_files(ctl, method):
    ctl.load(EXPANDING_FILE)
    if method == CONTAINMENT:
        ctl.load(EXPANDING_CONTAINMENT_FILE)
    elif method == CARDINALITY:
        ctl.load(EXPANDING_CARDINALITY_FILE)


def expanding_model_intersection(iteration_model_sets):
    resultant_models = iteration_model_sets[0]
    for model_set in iteration_model_sets[1:]:
        common_elements = resultant_models.intersection(model_set)
        if common_elements:
            resultant_models = common_elements
    return resultant_models


# TODO: FINISH THIS (ALSO HAVE TO UPDATE ASP PART)
def iterate_expanding(G, method=CARDINALITY):
    atoms = [eb.Prop(atom) for atom in G.atoms()]
    sorted_atoms = tuple(sorted(atoms))

    atom_mapping = create_atom_mapping(sorted_atoms)

    #R = copy.deepcopy(G)

    asp_str = eb.convert_to_asp(G, atom_mapping)

    diameter = 0
    lengths = nx.all_pairs_shortest_path_length(G)
    for node1 in lengths:
        for node2 in lengths[node1]:
            dist = lengths[node1][node2]
            if dist > diameter:
                diameter = dist
            asp_dist_str = "dist({0},{1},{2}).\n".format(node1, node2, dist)
            asp_str += asp_dist_str

    print("Diameter = {0}".format(diameter))

    node_models = defaultdict(set)
    node_tv_dict = defaultdict(int)

    iteration_model_sets = defaultdict(list)

    for radius in range(1, diameter+1):
        print("RADIUS = {0}".format(radius))
        ctl = gringo.Control()
        configure_solver(ctl, method)
        load_expanding_iteration_files(ctl, method)
        print(asp_str)
        ctl.add('base', [], asp_str)
        ctl.ground([('base', [])])
        ctl.ground([('expand', [radius])])

        it = ctl.solve_iter()
        for m in it:
            print(m)
            node_tv_dict.clear()
            terms = m.atoms(gringo.Model.SHOWN)
            for term in terms:
                if term.name() == 'tv':
                    center_node, node, atom_index, truth_value = term.args()
                    if center_node == node:
                        node_tv_dict[node] |= truth_value << atom_index
           
            for node in node_tv_dict:
                node_models[node].add(node_tv_dict[node])
        print(node_models)

        for node in node_models:
            iteration_model_sets[node].append(frozenset(node_models[node]))

        print(iteration_model_sets)

    for node in iteration_model_sets:
        print("Node {0}: {1}".format(node, iteration_model_sets[node]))

    for node in iteration_model_sets:
        resultant_models = expanding_model_intersection(iteration_model_sets[node])
        print("Resultant Models Node {0}: {1}".format(node, resultant_models))


    """
    true_prop = eb.Prop(True)

    for node in node_models:
        t = tuple(node_models[node])
        formula = formula_from_models(t, sorted_atoms)
        # TODO: Again, formulas are simplified, yielding slowdowns.
        simp = simplified(formula)
        if simp != true_prop:
            R.set_formulas(node, [simp])
    """

    return R


def configure_solver(ctl, method):
    ctl.conf.configuration = 'crafty'
    if method == CONTAINMENT:
        ctl.conf.solver.heuristic = 'domain'
        ctl.conf.solve.enum_mode = 'domRec'
        ctl.conf.solve.models = 0
    elif method == CARDINALITY:
        ctl.conf.solve.opt_mode = 'optN'


def load_files(ctl, method):
    ctl.load(EQ_BASE_FILE)
    if method == CONTAINMENT:
        ctl.load(EQ_CONTAINMENT_FILE)
    elif method == CARDINALITY:
        ctl.load(EQ_CARDINALITY_FILE)


def completion(G, debug=False, method=CONTAINMENT):
    ctl = gringo.Control()
    configure_solver(ctl, method)
    load_files(ctl, method)
    return solve(ctl, G, method)


def solve(ctl, G, method):
    atoms = [eb.Prop(atom) for atom in G.atoms()]
    sorted_atoms = tuple(sorted(atoms))
    atom_mapping = create_atom_mapping(sorted_atoms)

    ctl.add('base', [], eb.convert_to_asp(G, atom_mapping))
    ctl.ground([('base', [])])

    if method == CONTAINMENT:
        return solve_containment(ctl, G, sorted_atoms)
    elif method == CARDINALITY:
        return solve_cardinality(ctl, G, sorted_atoms)


def solve_containment(ctl, G, sorted_atoms):
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

    #print(node_models)
    R = update_formulas(G, node_models, sorted_atoms)
    return R


def solve_cardinality(ctl, G, sorted_atoms):
    node_models = defaultdict(set)
    node_tv_dict = defaultdict(int)

    old_opt_value = None

    it = ctl.solve_iter()
    for m in it:
        current_opt_value = m.optimization()
        if current_opt_value != old_opt_value:
            old_opt_value = current_opt_value
            continue

        #print(m)
        node_tv_dict.clear()
        terms = m.atoms(gringo.Model.SHOWN)
        for term in terms:
            if term.name() == 'tv':
                node, atom_index, truth_value = term.args()
                node_tv_dict[node] |= truth_value << atom_index

        for node in node_tv_dict:
            node_models[node].add(node_tv_dict[node])

    #print(node_models)
    R = update_formulas(G, node_models, sorted_atoms)
    return R


def update_formulas(G, node_models, sorted_atoms):
    true_prop = eb.Prop(True)
    
    R = copy.deepcopy(G)
    R.clear_formulas()
    for node in node_models:
        t = tuple(node_models[node])
        formula = formula_from_models(t, sorted_atoms)
        simple = simplified(formula)
        if simple != true_prop:
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
def simplified(formula):
    return eb.simplify(formula)


@memo
def formula_from_models(models, atoms):
    disjunction = eb.Prop(False)
    for model in models:
        disjunction |= formula_from_model(model, atoms)
    return disjunction


@memo
def formula_from_model(model, atoms):
    """Creates a propositional formula from a single model.
       
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


def revise(K, R, method=CARDINALITY):
    G = eb.path_graph(2)

    if isinstance(K, str):
        G.add_formula(0, eb.parse_infix_formula(K))
    elif isinstance(K, list):
        for belief in K:
            G.add_formula(0, eb.parse_infix_formula(belief))

    if isinstance(R, str):
        G.add_formula(1, eb.parse_infix_formula(R))
    elif isinstance(R, list):
        for belief in R:
            G.add_formula(1, eb.parse_infix_formula(belief))

    S = completion(G, method=method)
    return S.formulas(1)


def merge(belief_bases, entailment_constraint=None):
    G = eb.star_graph(len(belief_bases))

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
    G = eb.path_graph(num_nodes)
    G.add_formula(0, "p & q & r & s")
    G.add_formula(num_nodes-1, "~p & ~q & ~r & ~s")
    R = completion(G)
    for node_id in R.nodes():
        print("Node {0}, formulas = {1}".format(node_id, R.formulas(node_id)))
