import copy

import gringo
from gringo import Control, Model, Fun

import equibel.format.ASP_Formatter as ASP_Formatter
import equibel.FormulaExtractor as FormulaExtractor
from equibel.simbool.proposition import Prop
from equibel.simbool.simplify import simplify

ATOMS_KEY    = 'atoms'
WEIGHTS_KEY  = 'weights'
FORMULAS_KEY = 'formulas'

CONTAINMENT = 'containment'
CARDINALITY = 'cardinality'

class EqSolver:

    def __init__(self):
        self.optimal_models = set()
        self.optimal_values = None

    def find_models(self, asp_string, method=CONTAINMENT):
        self.optimal_models = set()
        self.optimal_values = None

        ctl = gringo.Control()
        ctl.load('equibel/eq_sets.lp')
        ctl.load('equibel/transitive.lp')
        ctl.load('equibel/translate.lp')

        self._configure_control(ctl, method)

        ctl.add('base', [], asp_string)
        ctl.ground([('base', [])])
        ctl.solve(on_model=self.capture_optimal_models)

        return self.optimal_models


    def iteration(self, asp_string, method=CONTAINMENT):
        self.optimal_models = set()
        self.optimal_values = None

        ctl = gringo.Control()
        ctl.load('equibel/eq_sets.lp')
        ctl.load('equibel/translate.lp')

        self._configure_control(ctl, method)

        ctl.add('base', [], asp_string)
        ctl.ground([('base', [])])
        ctl.solve(on_model=self.capture_optimal_models)

        return self.optimal_models

    def one_shot_dicts(self, asp_string, method=CONTAINMENT):
        models = self.find_models(asp_string, method)
        return self.model_dicts(models)

    def iteration_dicts(self, asp_string, method=CONTAINMENT):
        models = self.iteration(asp_string, method)
        return self.model_dicts(models)

    def model_dicts(self, models):
        model_list = []

        for model in models:
            term_dict = dict()
            term_names = set(term.name() for term in model)
            for term_name in term_names:
                term_dict[term_name] = [term for term in model if term.name() == term_name]
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
        #model_atoms = frozenset(atom for atom in model.atoms(Model.SHOWN) if atom.name() == 'new_formula')
        model_atoms = frozenset(model.atoms(Model.SHOWN))
        opt_values = model.optimization()

        if self.optimal_values is None:
            self.optimal_values = opt_values
            self.optimal_models.add(model_atoms)
        elif opt_values == self.optimal_values:
            self.optimal_models.add(model_atoms)
        elif opt_values < self.optimal_values:
            self.optimal_values = opt_values
            self.optimal_models.clear()
            self.optimal_models.add(model_atoms)


# TEST TEST TEST
def completion(G, solving_method=CONTAINMENT):
    solver = EqSolver()
    models = solver.one_shot_dicts(ASP_Formatter.convert_to_asp(G), solving_method)
    node_formulas = FormulaExtractor.combine_formulas(models)

    R = copy.deepcopy(G)

    # TODO: Decide whether to always represent "multiple formulas" as a 
    # single conjunction, or whether to keep them separate.
    for node_id in R.nodes():
        if node_id in node_formulas:
            new_formula = node_formulas[node_id]
            old_formula = conjunction(R.node[node_id][FORMULAS_KEY])
            R.node[node_id][FORMULAS_KEY] = set([simplify(old_formula & new_formula)])

    return R


# TEST TEST TEST
def iterate(G, num_iterations=1, solving_method=CONTAINMENT):
    solver = EqSolver()
    asp_string = ASP_Formatter.convert_to_asp(G)

    node_formulas = None

    for i in range(num_iterations):
        models = solver.iteration_dicts(asp_string)
        node_formulas = FormulaExtractor.combine_formulas(models)
        for node_id in node_formulas:
            formula = node_formulas[node_id]
            asp_string += "formula({formula}, {node}).".format(formula=formula, node=node_id)

    R = copy.deepcopy(G)

    # TODO: Decide whether to always represent "multiple formulas" as a 
    # single conjunction, or whether to keep them separate.
    for node_id in R.nodes():
        if node_id in node_formulas:
            new_formula = node_formulas[node_id]
            old_formula = conjunction(R.node[node_id][FORMULAS_KEY])
            R.node[node_id][FORMULAS_KEY] = set([simplify(old_formula & new_formula)])

    return R


def conjunction(formulas):
    result = Prop(True)

    for formula in formulas:
        result &= formula

    return simplify(result)



if __name__ == '__main__':
    a = Prop('a')
    b = Prop('b')
    c = Prop('c')

    form1 = a & b
    form2 = b | ~c

    print(repr(conjunction([form1, form2])))


    solver = EqSolver()
    final_models2 = solver.find_models(open('TestCases/case8.lp').read(), method=EqSolver.CONTAINMENT)
    final_models = solver.model_dicts(open('TestCases/case9.lp').read(), method=EqSolver.CARDINALITY)
    
    for model in final_models:
        print(model['eq'])

    formulas = FormulaExtractor.combine_formulas(final_models)

    print(formulas)

    print("\n")

    for model in final_models2:
        print(model)

