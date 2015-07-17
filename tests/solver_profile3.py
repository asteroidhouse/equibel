#    Copyright (C) 2014-2015 by
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.

from __future__ import absolute_import
from __future__ import print_function

import sys
import pkg_resources
import copy
import platform

import functools
from functools import wraps

import equibel

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
from equibel.simbool.proposition import Prop
from equibel.simbool.simplify import simplify


CONTAINMENT = 'containment'
CARDINALITY = 'cardinality'

EQ_SETS_FILE = 'asp/eq_sets.lp'
TRANSITIVE_FILE = 'asp/transitive.lp'


no_profile = False

if no_profile:
    def profile(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner


use_sets = True

class EqSolver(object):
    @profile
    def __init__(self):
        self.optimal_models = set()
        self.eq_dicts = []

    @profile
    def find_eq_dicts(self, asp_string, method=CONTAINMENT):
        self.optimal_models = set()
        self.eq_dicts = []

        ctl = gringo.Control()
        ctl.load(EQ_SETS_FILE)
        ctl.load(TRANSITIVE_FILE)
        self._configure_control(ctl, method)

        ctl.add('base', [], asp_string)
        ctl.ground([('base', [])])
        ctl.solve(on_model=self.create_eq_dicts)

        print("NUM EQ SETS = {0}".format(len(self.optimal_models)))
        return self.eq_dicts

    @profile
    def _configure_control(self, ctl, method):
        if method == CONTAINMENT:
            ctl.conf.solve.opt_mode   = 'ignore'
            ctl.conf.solve.enum_mode  = 'domRec'
            ctl.conf.solver.heuristic = 'domain'
            ctl.conf.solve.models = 0
        elif method == CARDINALITY:
            ctl.conf.solve.opt_mode   = 'optN'
            ctl.conf.solve.enum_mode  = 'auto'
            ctl.conf.solver.heuristic = 'none'
    
    @profile
    def create_eq_dicts(self, model):
        #print(model.atoms(Model.SHOWN))
        eq_dict = dict()
        for term in model.atoms(Model.SHOWN):
            if term.name() == 'eq':
                (atom_fun, node1, node2) = term.args()
                atom = str(atom_fun)
                if node2 not in eq_dict:
                    eq_dict[node2] = dict()
                    if use_sets:
                        eq_dict[node2][node1] = set([atom])
                    else:
                        eq_dict[node2][node1] = [atom]
                else:
                    if node1 not in eq_dict[node2]:
                        if use_sets:
                            eq_dict[node2][node1] = set([atom])
                        else:
                            eq_dict[node2][node1] = [atom]
                    else:
                        if use_sets:
                            eq_dict[node2][node1].add(atom)
                        else:
                            eq_dict[node2][node1].append(atom)
        for node2 in eq_dict:
            for node1 in eq_dict[node2]:
                eq_dict[node2][node1] = frozenset(eq_dict[node2][node1])
        self.eq_dicts.append(eq_dict)
            

@profile
def conjunction(formulas):
    result = Prop(True)
    for formula in formulas:
        result &= formula
    return result


@profile
def disjunction(formulas):
    result = Prop(False)
    for formula in formulas:
        result |= formula
    return result

debug = False

@profile
def print_eq_dicts(eq_dicts):
    for eq_dict in eq_dicts:
        for key in eq_dict:
            print("{0} => {1}".format(key, eq_dict[key]))
        print("\n")


@profile
def completion(G, solving_method=CONTAINMENT):
    solver = EqSolver()
    eq_dicts = solver.find_eq_dicts(equibel.convert_to_asp(G), solving_method)
    print_eq_dicts(eq_dicts)
    print("NUMBER OF EQ DICTS = {0}".format(len(eq_dicts)))
    return completion_graph(G, eq_dicts)


@profile
def completion_graph(G, eq_dicts):
    R = copy.deepcopy(G)
    final_disjunctions = eq_disjunctions(G, eq_dicts)
    for node in R:
        new_information = final_disjunctions[node]
        updated_formula = conjunction([form for form in G.formulas(node)] + [new_information])
        R.set_formulas(node, [simplify(updated_formula)])
    return R


@profile
def eq_disjunctions(G, eq_dicts):
    conjunction_dict = dict()
    for eq in eq_dicts:
        for node in G:
            other_nodes = [other for other in G if other != node]
            formulas = set()
            for other in other_nodes:
                if other in eq:
                    if node in eq[other]:
                        eq_atoms = eq[other][node]
                        other_node_formulas = G.formulas(other)
                        if other_node_formulas:
                            trans = translate_formulas(other_node_formulas, eq_atoms)
                            formulas.update(trans)
            if node not in conjunction_dict:
                conjunction_dict[node] = set([conjunction(formulas)])
            else:
                conjunction_dict[node].add(conjunction(formulas))
		
    disjunction_dict = dict()
    for node in conjunction_dict:
        disjunction_dict[node] = disjunction(conjunction_dict[node])
	
    return disjunction_dict


@profile
def translate_formulas(formulas, eq_atoms):
    translated_formulas = []
    for formula in formulas:
        translated_form = translate_formula(formula, eq_atoms)
        translated_formulas.append(translated_form)

    return translated_formulas


@profile
def memo(func):
    cache = {}
    @wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap


@profile
@memo
def translate_formula(formula, eq_atoms):
    if formula.is_atomic():
        if formula.get_name() in eq_atoms:
            return formula
        else:
            return ~formula

    op = formula.get_op()
    terms = formula.get_terms()
    translated_terms = [translate_formula(term, eq_atoms) for term in terms]
    return equibel.Prop(op, *translated_terms)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python solver_profile3.py NUM_NODES")
        sys.exit(1)
    
    num_nodes = int(sys.argv[1])
    
    solver = EqSolver()
    G = equibel.path_graph(num_nodes)
    G.add_formula(0, "p & q & r & s")
    G.add_formula(num_nodes-1, "~p & ~q & ~r & ~s")
    R = completion(G)
    for node_id in R.nodes():
        print("Node {0}, formulas = {1}".format(node_id, R.formulas(node_id)))