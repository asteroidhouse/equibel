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

EQ_SETS_FILE = pkg_resources.resource_filename('equibel', 'asp/eq_sets.lp')
TRANSITIVE_FILE = pkg_resources.resource_filename('equibel', 'asp/transitive.lp')
#TRANSLATE_FILE = pkg_resources.resource_filename('equibel', 'asp/translate.lp')
#EQ_EXPANDING_FILE = pkg_resources.resource_filename('equibel', 'asp/eq_expanding.lp')


class EqSolver(object):
    def __init__(self):
        self.optimal_models = set()
        self.eq_dicts = []
        self.graph = None
        self.conjunctions = dict()
        self.disjunctions = dict()

    def conjunction(formulas):
        result = Prop(True)
        for formula in formulas:
            result &= formula
        return result


    def disjunction(formulas):
        result = Prop(False)
        for formula in formulas:
            result |= formula
        return result
    
    def find_completion(self, G, method=CONTAINMENT):
        self.optimal_models = set()
        self.eq_dicts = []
        self.graph = G

        ctl = gringo.Control()
        ctl.load(EQ_SETS_FILE)
        ctl.load(TRANSITIVE_FILE)
        self._configure_control(ctl, method)

        ctl.add('base', [], equibel.convert_to_asp(G))
        ctl.ground([('base', [])])
        ctl.solve(on_model=self.on_model)
        
        for node in self.conjunctions:
            self.disjunctions[node] = disjunction(self.conjunctions[node])
            #print("DISJUNCTION NODE {0} = {1}".format(node, self.disjunctions[node]))
            
        R = copy.deepcopy(G)
        for node in R:
            new_information = self.disjunctions[node]
            updated_formula = conjunction([form for form in G.formulas(node)] + [new_information])
            R.set_formulas(node, [simplify(updated_formula)])
        return R

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
    
    def on_model(self, model):
        #print(model.atoms(Model.SHOWN))
        eq_dict = dict()
        for term in model.atoms(Model.SHOWN):
            if term.name() == 'eq':
                (atom_fun, node1, node2) = term.args()
                atom = str(atom_fun)
                if node1 not in eq_dict:
                    eq_dict[node1] = dict()
                    eq_dict[node1][node2] = set([atom])
                else:
                    if node2 not in eq_dict[node1]:
                        eq_dict[node1][node2] = set([atom])
                    else:
                        eq_dict[node1][node2].add(atom)
        
        for node1 in eq_dict:
            for node2 in eq_dict[node1]:
                eq_dict[node1][node2] = frozenset(eq_dict[node1][node2])
        
        self.translate_using_eq(eq_dict)
    
    def translate_using_eq(self, eq):
        for node in self.graph:
            other_nodes = [other for other in self.graph if other != node]
            formulas = set()
            for other_node in other_nodes:
                if node < other_node:
                    smaller_node = node
                    bigger_node = other_node
                else:
                    smaller_node = other_node
                    bigger_node = node
                if smaller_node in eq:
                    if bigger_node in eq[smaller_node]:
                        eq_atoms = eq[smaller_node][bigger_node]
                        other_node_formulas = self.graph.formulas(other_node)
                        if other_node_formulas:
                            trans = translate_formulas(other_node_formulas, eq_atoms)
                            formulas.update(trans)
                            #print("FORMULAS = {0}".format(formulas))
            
            if node not in self.conjunctions:
                self.conjunctions[node] = set([conjunction(formulas)])
            else:
                self.conjunctions[node].add(conjunction(formulas))


def conjunction(formulas):
    result = Prop(True)
    for formula in formulas:
        result &= formula
    return result


def disjunction(formulas):
    result = Prop(False)
    for formula in formulas:
        result |= formula
    return result

debug = False

def print_eq_dicts(eq_dicts):
    for eq_dict in eq_dicts:
        for key in eq_dict:
            print("{0} => {1}".format(key, eq_dict[key]))
        print("\n")

def completion(G, solving_method=CONTAINMENT):
    solver = EqSolver()
    return solver.find_completion(G)


def translate_formulas(formulas, eq_atoms):
    if debug:
        print("\t\t\tIn translate formulas...")
        print("\t\t\t-------------------------------")

    translated_formulas = []
    for formula in formulas:
        translated_form = translate_formula(formula, eq_atoms)
        if debug:
            print("\t\t\t\tOriginal = {0}, Translated = {1}".format(repr(formula), repr(translated_form)))
        translated_formulas.append(translated_form)

    #print("translate_formulas({0}, {1}) = {2}".format(formulas, eq_atoms, translated_formulas))
    return translated_formulas


def memo(func):
    cache = {}
    @wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap


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


# =================================================
# Functions that involve implicit graph topologies:
#   - Revision
#   - Contraction
#   - Merging (Projection and Consensus Based)
#   - Extrapolation
# =================================================

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


def contract(K, C):
    pass

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
