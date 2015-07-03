#    Copyright (C) 2014-2015 by
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    BSD license.

from __future__ import absolute_import
from __future__ import print_function

import sys
import pkg_resources
import copy
import platform

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
TRANSLATE_FILE = pkg_resources.resource_filename('equibel', 'asp/translate.lp')
EQ_EXPANDING_FILE = pkg_resources.resource_filename('equibel', 'asp/eq_expanding.lp')


class EqSolver(object):

    def __init__(self):
        self.optimal_models = set()
        self.optimal_values = None

    def find_models(self, asp_string, method=CONTAINMENT):
        #print("ASP STRING = {0}".format(asp_string))
        self.optimal_models = set()
        self.optimal_values = None

        ctl = gringo.Control()
        ctl.load(EQ_SETS_FILE)
        ctl.load(TRANSITIVE_FILE)

        self._configure_control(ctl, method)

        ctl.add('base', [], asp_string)
        ctl.ground([('base', [])])
        ctl.solve(on_model=self.capture_optimal_models)

        #print("SOLVER MODELS = {0}".format(self.optimal_models))
        print("NUM EQ SETS = {0}".format(len(self.optimal_models)))
        return self.optimal_models


    def one_shot_eq(self, asp_string, method=CONTAINMENT):
        models = self.find_models(asp_string, method)
        return self.extract_eq(models)

    
    def extract_eq(self, models):
        eq_dicts = []
        for model in models:
            eq_dict = dict()
            for term in model:
                if term.name() == 'eq':
                    atom = str(term.args()[0])
                    node1 = term.args()[1]
                    node2 = term.args()[2]
                    if node2 not in eq_dict:
                        eq_dict[node2] = dict()
                        eq_dict[node2][node1] = [atom]
                    else:
                        if node1 not in eq_dict[node2]:
                            eq_dict[node2][node1] = [atom]
                        else:
                            eq_dict[node2][node1].append(atom)
            eq_dicts.append(eq_dict)
        return eq_dicts
    

    def one_shot_dicts(self, asp_string, method=CONTAINMENT):
        models = self.find_models(asp_string, method)
        return self.model_dicts(models)


    def model_dicts(self, models):
        model_list = []

        for model in models:
            term_dict = dict()
            for term in model:
                name = term.name()
                if name in term_dict:
                    term_dict[name].append(term)
                else:
                    term_dict[name] = [term]
            model_list.append(term_dict)

        return model_list

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

    def capture_optimal_models(self, model):
        model_atoms = frozenset(model.atoms(Model.SHOWN))
        opt_values = model.optimization()

        #print("Opt val = {0}".format(self.optimal_values))

        if self.optimal_values is None:
            self.optimal_values = opt_values
            self.optimal_models.add(model_atoms)
        elif opt_values == self.optimal_values:
            self.optimal_models.add(model_atoms)
        elif opt_values < self.optimal_values:
            self.optimal_values = opt_values
            self.optimal_models.clear()
            self.optimal_models.add(model_atoms)


"""
# TEST TEST TEST
def completion(G, solving_method=CONTAINMENT):
    solver = EqSolver()
    models = solver.one_shot_dicts(ASP_Formatter.convert_to_asp(G), solving_method)
    #print("MODELS = {0}".format(models))
    node_formulas = FormulaExtractor.combine_formulas(models)

    R = copy.deepcopy(G)

    # TODO: Decide whether to always represent "multiple formulas" as a
    # single conjunction, or whether to keep them separate.
    for node_id in R.nodes():
        if node_id in node_formulas:
            new_formula = node_formulas[node_id]
            old_formula = conjunction(R.formulas(node_id))
            R.set_formulas(node_id, [simplify(old_formula & new_formula)])
            #R.set_formulas(node_id, [old_formula & new_formula])

    return R
"""


def conjunction(formulas):
    result = Prop(True)

    for formula in formulas:
        #print("FORMULA : {0}".format(formula))
        result &= formula

    """
    res = simplify(result)
    if debug:
        print("SIMPLIFIED CONJUNCTION = {0}".format(res))
    return res
    """
    return result


def disjunction(formulas):
    result = Prop(False)

    for formula in formulas:
        result |= formula

    #return simplify(result)
    return result

debug = False

def completion(G, solving_method=CONTAINMENT):
    #print("COMPLETION")
    solver = EqSolver()
    eq_dicts = solver.one_shot_eq(equibel.convert_to_asp(G), solving_method)
    if debug:
        print("EQ DICTS = {0}".format(eq_dicts))
        print("NUMBER OF EQ DICTS = {0}".format(len(eq_dicts)))
    return final_formulas(G, eq_dicts)


def final_formulas(G, eq_dicts):
    if debug:
        print("In final formulas...")
        print("-------------------------------")
    R = copy.deepcopy(G)
    for node in R.nodes():
        res = new_formula(node, G, eq_dicts)
        if debug:
            print("NODE {0} NEW FORMULAS= {1}".format(node, repr(res)))
        new_form = conjunction([form for form in G.formulas(node)] + [res])
        if debug:
            print("NODE {0} CONJUNCTION OF NEW FORMULAS= {1}".format(node, repr(new_form)))
        R.set_formulas(node, [simplify(new_form)])
        #R.set_formulas(node, [new_form])
    return R


def new_formula(node, G, eq_dicts):
    if debug:
        print("In new formulas...")
        print("-------------------------------")
    conjunctions = set()
    for eq_dict in eq_dicts:
        formulas = []
        if node in eq_dict:
            other_nodes = [curr_node for curr_node in G.nodes() if curr_node != node]
            if debug:
                print("\tUsing EQ DICT: {0}".format(eq_dict))
                print("\t-------------------------------")
            for other_node in other_nodes:
                if debug:
                    print("\t\tTranslating from {0} -> {1}".format(other_node, node))
                    print("\t\t-------------------------------")
                #eq_atoms = eq_dict[node][other_node]
                eq_atoms = eq_dict[node].get(other_node, [])
                if debug:
                    print("\t\t\tEQ atoms = {0}".format(eq_atoms))
                formulas.append(translate_formulas(G.formulas(other_node), eq_atoms))
                if debug:
                    print("\t\t\tFormulas = {0}".format(formulas))
            conjunctions.add(conjunction([form for forms in formulas for form in forms]))
            if debug:
                print("\tCONJUNCTIONS = {0}".format(conjunctions))

    return simplify(disjunction(conjunctions))


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


def translate_formula(formula, eq_atoms):
    if debug:
        print("\t\t\t\t\tTranslating {0} with {1}".format(repr(formula), eq_atoms))
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
    solver = EqSolver()

    G = equibel.path_graph(20)
    G.add_formula(0, "p & q")
    G.add_formula(1, "a & b & c & d & e & f & g & h & i & j & ~p")
    #eq_dicts = solver.one_shot_eq(equibel.convert_to_asp(G), method=CONTAINMENT)
    #print(eq_dicts)

    #print(eq_dicts)
    #print("NEW FORMULA {0}".format(new_formulas(0, G, eq_dicts)))

    """
    formula = equibel.parse_infix_formula("(p & q) | r")
    eq_atoms = ['q']
    translated = translate_formula(formula, eq_atoms)
    print(repr(translated))
    """

    R = completion(G)
    for node_id in R.nodes():
        print("Node {0}, formulas = {1}".format(node_id, R.formulas(node_id)))


    #filename = sys.argv[1]
    #f = file(filename, 'r')
    #final_models = solver.one_shot_dicts(equibel.convert_to_asp(G), method=CONTAINMENT)
    #print(final_models)

