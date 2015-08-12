from __future__ import print_function

import copy
import sys
from collections import defaultdict
from functools import wraps

import gringo

import equibel as eb

def create_atom_mapping(atoms):
    mapping = dict()
    for (index, atom) in enumerate(atoms):
        mapping[atom] = index
    return mapping

def iterate_steady(G):
    atoms = [eb.Prop(atom) for atom in G.atoms()]
    sorted_atoms = tuple(sorted(atoms))

    atom_mapping = create_atom_mapping(sorted_atoms)

    old_R = None
    R = copy.deepcopy(G)

    # TODO: Have a method of testing the equality of graphs
    while old_R != R:
        old_R = copy.deepcopy(R)
        ctl = gringo.Control()
        ctl.conf.configuration = 'handy'
        ctl.conf.solver.heuristic = 'domain'
        ctl.conf.solve.enum_mode = 'domRec'
        ctl.conf.solve.models = 0
        #ctl.conf.solve.parallel_mode = 2

        ctl.load('asp/eq_iterate.lp')
        print(eb.convert_to_asp(R, atom_mapping))
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
        print(node_models)

        true_prop = eb.Prop(True)

        for node in node_models:
            t = tuple(node_models[node])
            formula = formula_from_models(t, sorted_atoms)
            simp = simplify(formula)
            print("Node {0}: {1}".format(node, repr(simp)))
            if simp != true_prop:
                R.set_formulas(node, [simp])

    return R


def iterate(G, num_iterations):
    atoms = [eb.Prop(atom) for atom in G.atoms()]
    sorted_atoms = tuple(sorted(atoms))

    atom_mapping = create_atom_mapping(sorted_atoms)

    R = copy.deepcopy(G)

    for i in range(num_iterations):
        ctl = gringo.Control()
        ctl.conf.configuration = 'handy'
        ctl.conf.solver.heuristic = 'domain'
        ctl.conf.solve.enum_mode = 'domRec'
        ctl.conf.solve.models = 0
        #ctl.conf.solve.parallel_mode = 2

        ctl.load('asp/eq_iterate.lp')
        print(eb.convert_to_asp(R, atom_mapping))
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
        print(node_models)

        true_prop = eb.Prop(True)

        for node in node_models:
            t = tuple(node_models[node])
            formula = formula_from_models(t, sorted_atoms)
            simp = simplify(formula)
            print("Node {0}: {1}".format(node, repr(simp)))
            if simp != true_prop:
                R.set_formulas(node, [simp])

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


def print_formulas(G):
    for node in G:
        print("Node {0}: {1}".format(node, G.formulas(node)))


if __name__ == '__main__':
    G = eb.path_graph(5)
    G.add_formula(0, 'p')
    G.add_formula(4, '~p')
    print_formulas(G)

    R = iterate_steady(G)

    print_formulas(R)
