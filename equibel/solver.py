"""This file contains functions that implement the following approaches 
to consistency-based belief change in a graph-oriented setting:

1. Global completion: ``eb.global_completion(G)``
2. Simple iteration: ``eb.iterate_simple(G)``
3. Expanding iteration: ``eb.iterate_expanding(G)``
4. Augmenting iteration: ``eb.iterate_augmenting(G)``
5. The ring method: ``eb.iterate_ring(G)``

Each of the approaches has two separate implementations, corresponding to 
the *semantic* and *syntactic* characterizations. In addition, there are 
two ways of maximizing equivalences used by any approach: *inclusion-based* 
or *cardinality-based* maximization. 

Each function listed above takes three optional arguments: 
    1. ``method``, which is a string that is either "semantic" or "syntactic", 
       representing the method by which to perform the completion; e.g. based 
       on either the syntactic or semantic characterizations
    2. ``opt_type``, which is a string that is either "inclusion" or "cardinality", 
       representing the type of maximization to be  performed over equivalences 
    3. ``simplify``, which is a Boolean flag specifying whether to simplify the 
       final formulas at each node.
"""
#    Copyright (C) 2016
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.
from __future__ import absolute_import

import multiprocessing as mp

import platform
import pkg_resources
from collections import defaultdict
import copy
import tempfile

import networkx as nx
from sympy import *

import equibel as eb
from equibel import asprin


if platform.system() == 'Linux':
    if platform.architecture()[0] == '64bit':
        from equibel.includes.linux_64 import gringo
    #elif platform.architecture()[0] == '32bit':
    #    from equibel.includes.linux_32 import gringo
elif platform.system() == 'Darwin':
    from equibel.includes.mac import gringo


SEMANTIC = 'semantic'
SYNTACTIC = 'syntactic'

CARDINALITY = 'cardinality'
INCLUSION = 'inclusion'

PROJECTION = 'projection'
CONSENSUS = 'consensus'


###################################################################
###  ENCODING AND ASPRIN PREFERENCE FILE FOR GLOBAL COMPLETION  ###
###################################################################
EQ_GLOBAL = pkg_resources.resource_filename('equibel', 'asp/problem_encodings/global.lp')
PREFERENCE_GLOBAL = pkg_resources.resource_filename('equibel', 'asp/preferences/global_pref.lp')


##############################################
####  FILES FOR CARDINALITY MAXIMIZATION  ####
##############################################
GLOBAL_CARDINALITY_MAX = pkg_resources.resource_filename('equibel', 'asp/auxilliary/global_card_max.lp')
EXPANDING_CARDINALITY_MAX = pkg_resources.resource_filename('equibel', 'asp/auxilliary/expanding_card_max.lp')


#####################################################################
###  ENCODING AND ASPRIN PREFERENCE FILE FOR EXPANDING ITERATION  ###
###  (ALSO USED FOR SIMPLE ITERATION AND THE RING METHOD)         ###
#####################################################################
EXPANDING_ENCODING = pkg_resources.resource_filename('equibel', 'asp/problem_encodings/expanding.lp')
EXPANDING_PREFERENCE = pkg_resources.resource_filename('equibel', 'asp/preferences/expanding_pref.lp')


######################################################################
###  ENCODING AND ASPRIN PREFERENCE FILE FOR AUGMENTING ITERATION  ###
######################################################################
AUGMENTING_ENCODING = pkg_resources.resource_filename('equibel', 'asp/problem_encodings/augmenting.lp')
AUGMENTING_PREFERENCE = pkg_resources.resource_filename('equibel', 'asp/preferences/augmenting_pref.lp')


##################################
###  AUXILLIARY ASP ENCODINGS  ###
##################################
DECONSTRUCT = pkg_resources.resource_filename('equibel', 'asp/auxilliary/deconstruct.lp')
TRANSITIVE = pkg_resources.resource_filename('equibel', 'asp/auxilliary/transitive.lp')
SYMMETRIC = pkg_resources.resource_filename('equibel', 'asp/auxilliary/symmetric.lp')


################################
###  NEIGHBORHOOD ENCODINGS  ###
################################
WEB = pkg_resources.resource_filename('equibel', 'asp/neighborhoods/web.lp')
USPT = pkg_resources.resource_filename('equibel', 'asp/neighborhoods/uspt.lp')
RING = pkg_resources.resource_filename('equibel', 'asp/neighborhoods/ring.lp')


def expanding_maximal_answer_sets(G, distances, center, radius, atoms=None, neighborhood_type=USPT,
                                  method=SEMANTIC, opt_type=INCLUSION):
    if opt_type == INCLUSION:
        if method == SEMANTIC:
            models = asprin.compute_optimal_models([EXPANDING_ENCODING, EXPANDING_PREFERENCE, DECONSTRUCT, neighborhood_type],
                                                    [("base", [], G.to_asp(atoms)),
                                                     ("base", [], distances),
                                                     ("base", [], "#const center={}.".format(center)),
                                                     ("base", [], "#const radius={}.".format(radius))])
            return models
        elif method == SYNTACTIC:
            ctl = gringo.Control()
            ctl.conf.configuration = 'crafty'
            ctl.conf.solver.heuristic = 'domain'
            ctl.conf.solve.enum_mode = 'domRec'
            ctl.conf.solve.models = 0

            ctl.load(EXPANDING_ENCODING)
            ctl.load(TRANSITIVE)
            ctl.load(SYMMETRIC)
            ctl.load(DECONSTRUCT)
            ctl.load(neighborhood_type)

            ctl.add("base", [], G.to_asp(atoms))
            ctl.add("base", [], distances)
            ctl.add("base", [], "#const center={}.".format(center))
            ctl.add("base", [], "#const radius={}.".format(radius))
            ctl.ground([('base', [])])
            answer_sets = []
            for ans in ctl.solve_iter():
                answer_sets.append(ans.atoms(gringo.Model.SHOWN))
            return answer_sets
    elif opt_type == CARDINALITY:
        ctl = gringo.Control()
        ctl.conf.configuration = 'crafty'
        ctl.conf.solver.heuristic = 'domain'
        ctl.conf.solve.opt_mode = 'optN'
        ctl.conf.solve.models = 0

        ctl.load(EXPANDING_ENCODING)
        ctl.load(SYMMETRIC)
        ctl.load(DECONSTRUCT)
        ctl.load(neighborhood_type)
        ctl.load(EXPANDING_CARDINALITY_MAX)

        if method == SYNTACTIC:
            ctl.load(TRANSITIVE)

        ctl.add("base", [], G.to_asp(atoms))
        ctl.add("base", [], distances)
        ctl.add("base", [], "#const center={}.".format(center))
        ctl.add("base", [], "#const radius={}.".format(radius))

        #if method == SEMANTIC:
        #    ctl.add("base", [], "#show tv/4.")

        ctl.ground([('base', [])])

        old_opt_value = None
        answer_sets = []
        for ans in ctl.solve_iter():
            print(ans.atoms(gringo.Model.SHOWN))
            print("OPTIMIZATION = {}".format(ans.optimization()))
            current_opt_value = ans.optimization()
            if current_opt_value != old_opt_value:
                old_opt_value = current_opt_value
                continue
            answer_sets.append(ans.atoms(gringo.Model.SHOWN))
        return answer_sets


def augmenting_iteration_maximal_answer_sets(G, distances, center, eccentricity):
    models = asprin.compute_optimal_models([AUGMENTING_ENCODING, AUGMENTING_PREFERENCE, DECONSTRUCT],
                                            [("base", [], G.to_asp()),
                                             ("base", [], distances),
                                             ("base", [], "#const center={}.".format(center)),
                                             ("base", [], "#const eccentricity={}.".format(eccentricity))])
    return models


def maximal_answer_sets(G, method=SEMANTIC, opt_type=INCLUSION):
    if opt_type == INCLUSION:
        if method == SEMANTIC:
            answer_sets = asprin.compute_optimal_models([EQ_GLOBAL, PREFERENCE_GLOBAL, DECONSTRUCT],
                                                        [("base", [], G.to_asp()),
                                                         ("base", [], "#show tv/3.")])
            return answer_sets
        elif method == SYNTACTIC:
            ctl = gringo.Control()
            ctl.conf.configuration = 'crafty'
            ctl.conf.solver.heuristic = 'domain'
            ctl.conf.solve.enum_mode = 'domRec'
            ctl.conf.solve.models = 0

            ctl.load(EQ_GLOBAL)
            ctl.load(TRANSITIVE)
            ctl.load(SYMMETRIC)
            ctl.load(DECONSTRUCT)

            ctl.add("base", [], G.to_asp())
            ctl.ground([('base', [])])
            answer_sets = []
            for ans in ctl.solve_iter():
                answer_sets.append(ans.atoms(gringo.Model.SHOWN))
            return answer_sets
    elif opt_type == CARDINALITY:
        ctl = gringo.Control()
        ctl.conf.configuration = 'crafty'
        ctl.conf.solver.heuristic = 'domain'
        ctl.conf.solve.opt_mode = 'optN'
        ctl.conf.solve.models = 0

        ctl.load(EQ_GLOBAL)
        ctl.load(SYMMETRIC)
        ctl.load(DECONSTRUCT)
        ctl.load(GLOBAL_CARDINALITY_MAX)

        if method == SYNTACTIC:
            ctl.load(TRANSITIVE)

        ctl.add("base", [], G.to_asp())

        if method == SEMANTIC:
            ctl.add("base", [], "#show tv/3.")

        ctl.ground([('base', [])])

        old_opt_value = None
        answer_sets = []
        for ans in ctl.solve_iter():
            current_opt_value = ans.optimization()
            if current_opt_value != old_opt_value:
                old_opt_value = current_opt_value
                continue
            answer_sets.append(ans.atoms(gringo.Model.SHOWN))
    
        return answer_sets



def revise(K, alpha, simplify=False):
    """Revises a knowledge base $K$ by a formula $\alpha$.

    This function implements the consistency-based revision operator introduced in [?], by:
        1. Constructing a two-node path graph 0 <--> 1; 
        2. Associating the formulas in $K$ with node 0, and the formula $\alpha$ with node 1;
        3. Computing the new belief at node 1 by determining what parts of $K$ can be incorporated 
           while maintaining consistency with $\alpha$.

    Parameters
    ----------
    K     : A formula string or a list of formula strings (taken conjunctively as a knowledge base)
    alpha : A formula string or a list of formula strings (taken conjunctively)
    simplify : A Boolean flag specifying whether to simplify the result of revision.

    Returns
    -------
    R : A single formula representing the resultant knowledge base $K \dot{+} \alpha$, taken 
        conjunctively.

    Examples
    --------
    The simplest way to call this function is to provide a single formula for each of ``K`` 
    and ``alpha``:

    >>> eb.revise('p & q', '~p | ~q')
    And(Or(And(Not(p), q), And(Not(q), p)), Or(Not(p), Not(q)))

    To pretty-print formulas in infix notation with Unicode symbols, we can use:

    >>> eb.pprint(eb.revise('p & q', '~p | ~q'))

    Note that, by default, the formula representing the result of revision is not simplified.
    Setting the optional argument ``simplify=True`` enables this final simplification step:

    >>> eb.revise('p & q', '~p | ~q', simplify=True)
    Or(And(Not(p), q), And(Not(q), p))

    The above revision is equivalent to the following form, using a list of formula strings 
    ['p', 'q'] (taken conjunctively) instead of the single formula string 'p & q':

    >>> eb.revise(['p', 'q'], '~p | ~q', simplify=True)
    Or(And(Not(p), q), And(Not(q), p))
    """
    G = eb.path_graph(2)

    if isinstance(K, list):
        for item in K:
            G.add_formula(0, item)
    else:
        G.add_formula(0, K)


    if isinstance(alpha, list):
        for item in alpha:
            G.add_formula(1, item)
    else:
        G.add_formula(1, alpha)

    print(G.to_asp())
    
    atoms = G.atoms()

    eq_sets = []

    ctl = gringo.Control()
    ctl.conf.configuration = 'crafty'
    ctl.conf.solver.heuristic = 'domain'
    ctl.conf.solve.enum_mode = 'domRec'
    ctl.conf.solve.models = 0

    ctl.load(EQ_GLOBAL)
    ctl.load(TRANSITIVE)
    ctl.load(SYMMETRIC)
    ctl.load(DECONSTRUCT)

    ctl.add("base", [], G.to_asp(atoms))
    ctl.ground([('base', [])])
    answer_sets = ctl.solve_iter()

    #num_answer_sets = 0

    for answer_set in answer_sets:
        #num_answer_sets += 1
        current_eq_atoms = set()
        for term in answer_set.atoms(gringo.Model.SHOWN):
            if term.name() == 'eq':
                atom_fun, X, Y = term.args()
                atom = symbols(atom_fun.name())
                current_eq_atoms.add(atom)
        eq_sets.append(current_eq_atoms)
    #print("Found {} EQ sets".format(num_answer_sets))
    
    disjuncts = set()

    for eq_atoms in eq_sets:
        conj = true
        diff_atoms = atoms - eq_atoms
        original_formula = G.formula_conj(0)
        translated_formula = original_formula.xreplace({x: ~x for x in diff_atoms})
        conj &= translated_formula
        disjuncts.add(conj)

    resultant_formula = G.formula_conj(1) & disjunction(disjuncts)

    if simplify:
        return eb.simplify_logic(resultant_formula)
    else:
        return resultant_formula


def global_completion(G, method=SEMANTIC, opt_type=INCLUSION, simplify=False):
    """Finds the global completion of a graph and associated scenario.

    Parameters
    ----------
    G : An EquibelGraph object, representing a graph and associated scenario
    method : A string that is either "semantic" or "syntactic", representing the 
             method by which to perform the completion; e.g. based on either the 
             syntactic or semantic characterizations.
    opt_type : A string that is either "inclusion" or "cardinality", 
               representing the type of maximization to be performed 
               over equivalences.
    simplify : A Boolean flag specifying whether to simplify the final formulas at each node.

    Returns
    -------
    R : A new EquibelGraph object, representing the global completion of ``G``.
    """
    if method == SEMANTIC:
        R = global_completion_semantic(G, opt_type=opt_type)
    elif method == SYNTACTIC:
        R = global_completion_syntactic(G, opt_type=opt_type)

    if simplify:
        simplify_all_formulas(R)
    return R


def global_completion_semantic(G, opt_type=INCLUSION):
    """Finds the global completion of a graph and associated scenario, using the 
    **semantic characterization**.

    Parameters
    ----------
    G : An EquibelGraph object, representing a graph and associated scenario
    opt_type : A string that is either "inclusion" or "cardinality", representing 
               the type of maximization to be performed over equivalences.
    simplify : A Boolean flag specifying whether to simplify the final formulas at each node.

    Returns
    -------
    R : A new EquibelGraph object, representing the global completion of ``G``.
    """
    node_models = defaultdict(set)
    node_model_dict = defaultdict(list)
    models = maximal_answer_sets(G, method=SEMANTIC, opt_type=opt_type)

    for model in models:
        node_model_dict.clear()

        for term in model:
            if term.name() == 'tv':
                node, atom_fun, truth_value = term.args()
                atom = symbols(atom_fun.name())
                if truth_value == 1:
                    node_model_dict[node].append(atom)

        for node in G.nodes():
            if node_model_dict[node]:
                node_models[node].add(frozenset(node_model_dict[node]))
            else:
                # node has no models with true atoms
                node_models[node].add(frozenset())

    atoms = G.atoms()
    
    R = copy.deepcopy(G)
    R.clear_formulas()
    for node in node_models:
        t = tuple(node_models[node])
        formula = formula_from_models(t, atoms)
        R.add_formula(node, formula)

    return R


def create_eq_dicts(answer_sets):
    """Extracts ``eq/3`` predicates from a set of answer sets, and structures them into a 
    dictionary that makes it easy to retrieve the set of atoms on which two nodes agree.

    Parameters
    ----------
    answer_sets : An iterable container of answer sets.
                  Each answer set is represented as a list of *terms* (defined in the 
                  ``gringo`` module).
    """
    eq_dicts = []
    for answer_set in answer_sets:
        current_eq_dict = defaultdict(lambda: defaultdict(set))
        for term in answer_set:
            if term.name() == 'eq':
                atom_fun, X, Y = term.args()
                atom = symbols(atom_fun.name())
                current_eq_dict[X][Y].add(atom)
        eq_dicts.append(current_eq_dict)
    return eq_dicts


def global_completion_syntactic(G, opt_type=INCLUSION):
    """Finds the global completion of a graph and associated scenario, using the 
    **syntactic characterization**.

    Parameters
    ----------
    G : An EquibelGraph object, representing a graph and associated scenario
    opt_type : A string that is either "inclusion" or "cardinality", representing 
               the type of maximization to be performed over equivalences.
    simplify : A Boolean flag specifying whether to simplify the final formulas at each node.

    Returns
    -------
    R : A new EquibelGraph object, representing the global completion of ``G``.
    """
    atoms = G.atoms()
    answer_sets = maximal_answer_sets(G, method=SYNTACTIC, opt_type=opt_type)
    eq_dicts = create_eq_dicts(answer_sets)
    
    R = copy.deepcopy(G)
    R.clear_formulas()

    disjuncts = defaultdict(set)

    for eq_dict in eq_dicts:
        for j in G:
            conj = true
            for i in G:
                if i != j:
                    eq_atoms = eq_dict[j][i]
                    diff_atoms = atoms - eq_atoms
                    original_formula = G.formula_conj(i)
                    translated_formula = original_formula.xreplace({x: ~x for x in diff_atoms})
                    conj &= translated_formula
            disjuncts[j].add(conj)

    for node in G:
        resultant_formula = G.formula_conj(node) & disjunction(disjuncts[node])
        R.add_formula(node, resultant_formula)

    return R


def simple_semantic(G, center, atoms, opt_type=INCLUSION):
    """Computes the formula for node ``center`` in graph ``G`` that results from 
    one iteration of the simple (fixed-radius) approach, using the *semantic characterization*.
    
    Parameters
    ----------
    G : An EquibelGraph object, representing a graph and an associated scenario
    center : A node in ``G`` for which to compute the result of simple iteration
    atoms : A set of Sympy atomic propositions, representing the *alphabet*.
    opt_type : A string that is either "inclusion" or "cardinality", representing 
               the type of maximization to be performed over equivalences.
    """
    dist_str = create_distance_string(G)
    ecc = nx.eccentricity(G, center)

    answer_sets = expanding_maximal_answer_sets(G, dist_str, center, 1, atoms=atoms, neighborhood_type=USPT,
                                                method=SEMANTIC, opt_type=opt_type)

    center_models = set()
    node_model_dict = dict()

    for answer_set in answer_sets:
        current_eq_set = set()
        for term in answer_set:
            if term.name() == 'tv':
                center_node, node, atom_fun, truth_value = term.args()
                atom = symbols(atom_fun.name())
                if center_node == node:
                    node_model_dict[atom] = truth_value

        true_atoms = frozenset([atom for atom in node_model_dict if node_model_dict[atom] == 1])
        center_models.add(true_atoms)
    
    formula = formula_from_models(center_models, atoms)
    return {center: formula}


def simple_syntactic(G, center, atoms, opt_type=INCLUSION):
    """Computes the formula for node ``center`` in graph ``G`` that results from 
    one iteration of the simple (fixed-radius) approach, using the *syntactic characterization*.
    
    Parameters
    ----------
    G : An EquibelGraph object, representing a graph and an associated scenario
    center : A node in ``G`` for which to compute the result of simple iteration
    atoms : A set of Sympy atomic propositions, representing the *alphabet*.
    opt_type : A string that is either "inclusion" or "cardinality", representing 
               the type of maximization to be performed over equivalences.
    """
    dist_str = create_distance_string(G)
    ecc = nx.eccentricity(G, center)

    eq_sets = []
    answer_sets = expanding_maximal_answer_sets(G, dist_str, center, 1, atoms=atoms, neighborhood_type=USPT,
                                                method=SYNTACTIC, opt_type=opt_type)

    for answer_set in answer_sets:
        # current_eq_set is a mapping like current_eq_set[2] = {p,q,r}, 
        # current_eq_set[3] = {p,q}, all with respect to a given node (e.g. node 1)
        current_eq_set = defaultdict(set)
        for term in answer_set:
            if term.name() == 'eq':
                center_node, atom_fun, X, Y = term.args()
                atom = symbols(atom_fun.name())
                if center_node == X:
                    current_eq_set[Y].add(atom)

        eq_sets.append(current_eq_set)

    formula = formula_from_eq_sets(G, center, eq_sets, atoms)
    return {center: formula}


def only_one_model_for_each_eq_set(models_for_eq_set_dict):
    """Checks whether each EQ set in ``models_for_eq_set_dict`` is associated with 
    *only one* model.

    Parameters
    ----------
    models_for_eq_set_dict : A dictionary where *keys* are EQ sets (represented by any 
                             hashable objects, in this case strings) and *values* are 
                             sets of models (where each model is a set of atoms).

    Returns
    -------
    Returns True if each EQ set in the dictionary is associated with a single model; 
    returns False otherwise (that is, if any EQ set in the dictionary is associated 
    with *more than* one model).
    """
    for eq_set in models_for_eq_set_dict:
        if len(models_for_eq_set_dict[eq_set]) > 1:
            return False
    return True


def expanding_semantic(G, center, atoms, opt_type=INCLUSION):
    """Computes the formula for node ``center`` in graph ``G`` that results from 
    one iteration of the expanding approach, using the *semantic characterization*.
    
    Parameters
    ----------
    G : An ``EquibelGraph`` object, representing a graph and an associated scenario
    center : A node in ``G`` for which to compute the result of simple iteration
    atoms : A set of Sympy atomic propositions, representing the *alphabet*.
    opt_type : A string that is either "inclusion" or "cardinality", representing 
               the type of maximization to be performed over equivalences.
    """
    dist_str = create_distance_string(G)
    ecc = nx.eccentricity(G, center)

    #print("CENTER = {}".format(center))
    #print("Eccentricity = {}".format(ecc))

    for radius in range(1, ecc+1):
        #print("RADIUS = {}".format(radius))
        #print(G.to_asp(atoms))

        center_models = set()
        models = expanding_maximal_answer_sets(G, dist_str, center, radius, atoms=atoms,
                                               method=SEMANTIC, opt_type=opt_type)
        node_model_dict = dict()
        models_for_eq_set_dict = defaultdict(set)

        for model in models:
            current_eq_set = set()
            for term in model:
                if term.name() == 'tv':
                    center_node, node, atom_fun, truth_value = term.args()
                    atom = symbols(atom_fun.name())
                    if center_node == node:
                        node_model_dict[atom] = truth_value
                elif term.name() == 'eq':
                    current_eq_set.add(str(term))

            true_atoms = frozenset([atom for atom in node_model_dict if node_model_dict[atom] == 1])
            center_models.add(true_atoms)
            models_for_eq_set_dict[frozenset(current_eq_set)].add(true_atoms)

        mid_formula = formula_from_models(center_models, atoms)
        G.clear_formulas_from(center)
        G.add_formula(center, mid_formula)

        # Early stopping condition:
        if only_one_model_for_each_eq_set(models_for_eq_set_dict):
            break

    formula = formula_from_models(center_models, atoms)
    return {center: formula}


def expanding_syntactic(G, center, atoms, opt_type=INCLUSION):
    """Computes the formula for node ``center`` in graph ``G`` that results from 
    one iteration of the expanding approach, using the *syntactic characterization*.
    
    Parameters
    ----------
    G : An ``EquibelGraph`` object, representing a graph and an associated scenario
    center : A node in ``G`` for which to compute the result of simple iteration
    atoms : A set of Sympy atomic propositions, representing the *alphabet*.
    opt_type : A string that is either "inclusion" or "cardinality", representing 
               the type of maximization to be performed over equivalences.
    """
    dist_str = create_distance_string(G)
    ecc = nx.eccentricity(G, center)

    #print("CENTER = {}".format(center))
    #print("Eccentricity = {}".format(ecc))

    for radius in range(1, ecc+1):
        eq_sets = []

        #print("RADIUS = {}".format(radius))
        #print(G.to_asp(atoms))

        answer_sets = expanding_maximal_answer_sets(G, dist_str, center, radius, atoms=atoms,
                                               method=SYNTACTIC, opt_type=opt_type)

        for answer_set in answer_sets:
            current_eq_set = defaultdict(set) # mapping like current_eq_set[2] = {p,q,r}, current_eq_set[3] = {p,q}, all for node 1
            for term in answer_set:
                if term.name() == 'eq':
                    center_node, atom_fun, X, Y = term.args()
                    atom = symbols(atom_fun.name())
                    if center_node == X:
                        current_eq_set[Y].add(atom)
            eq_sets.append(current_eq_set)

        mid_formula = formula_from_eq_sets(G, center, eq_sets, atoms)
        G.clear_formulas_from(center)
        G.add_formula(center, mid_formula)

    final_formula = G.formula_conj(center)
    return {center: final_formula}


def formula_from_eq_sets(G, current_node, eq_sets, atoms):
    disjuncts = set()
    for eq_set in eq_sets:
        conj = true
        for node in eq_set:
            eq_atoms = eq_set[node]
            diff_atoms = atoms - eq_atoms
            original_formula = G.formula_conj(node)
            translated_formula = original_formula.xreplace({x: ~x for x in diff_atoms})
            conj &= translated_formula
        disjuncts.add(conj)
    return G.formula_conj(current_node) & disjunction(disjuncts)


def simplify_all_formulas(G):
    """Simplifies the formulas of all nodes in ``G``.

    This function modifies ``G`` in place; it does **not** return a new graph.

    Parameters
    ----------
    G : An ``EquibelGraph`` object.

    Example
    -------
    >>> G = eb.path_graph(2)
    >>> G.add_formula(0, 'p & (p | q | r | s)')
    >>> G.add_formula(1, '(p & q) | (p & ~q)')
    >>> eb.simplify_all_formulas(G)
    >>> G.formulas()
    {0: set([p]), 1: set([p])}
    """
    for node in G:
        formula = G.formula_conj(node)
        simplified_formula = simplify_logic(formula)
        G.clear_formulas_from(node)
        if simplified_formula != True:
            G.add_formula(node, simplified_formula)


def iterate_function_fixpoint(G, iteration_function, method=SEMANTIC, opt_type=INCLUSION, simplify=False):
    """Finds the fixpoint of ``iteration_function`` applied on the graph ``G``.

    This is a higher-order function that repeatedly applies a *function* ``iteration_function``, 
    starting with the initial graph ``G``, producing a sequence of ``EquibelGraph`` objects, 
    until reaching a state where the current ``EquibelGraph`` is equal to the previous one; then, 
    the final ``EquibelGraph`` is returned.

    Parameters
    ----------
    G : An ``EquibelGraph`` object
    iteration_function : The function to be applied iteratively, starting with ``G``
    method : A string that is either "semantic" or "syntactic", representing the 
             method by which to perform the completion; e.g. based on either the 
             syntactic or semantic characterizations.
    opt_type : A string that is either "inclusion" or "cardinality", 
               representing the type of maximization to be performed 
               over equivalences.
    simplify : A Boolean flag specifying whether to simplify the final formulas at each node.
    """
    old_R = None
    R = G

    num_iterations = 0
    while R != old_R:
        num_iterations += 1
        old_R = copy.deepcopy(R)
        R = iteration_function(R, method=method, opt_type=opt_type, simplify=simplify)

    return R, num_iterations


def iterate_expanding_fixpoint(G, method=SEMANTIC, opt_type=INCLUSION, simplify=False):
    """Finds the fixpoint of *expanding iteration* with respect the graph ``G``."""
    return iterate_function_fixpoint(G, iterate_expanding, method=method, opt_type=opt_type, simplify=simplify)


def iterate_augmenting_fixpoint(G, method=SEMANTIC, opt_type=INCLUSION, simplify=False):
    """Finds the fixpoint of *augmenting iteration* with respect the graph ``G``."""
    return iterate_function_fixpoint(G, iterate_augmenting, method=method, opt_type=opt_type, simplify=simplify)


def iterate_simple_fixpoint(G, method=SEMANTIC, opt_type=INCLUSION, simplify=False):
    """Finds the fixpoint of *simple iteration* with respect the graph ``G``."""
    return iterate_function_fixpoint(G, iterate_simple, method=method, opt_type=opt_type, simplify=simplify)


def iterate_ring_fixpoint(G, method=SEMANTIC, opt_type=INCLUSION, simplify=False):
    """Finds the fixpoint of the *ring method* with respect to the graph ``G``."""
    return iterate_function_fixpoint(G, iterate_ring, method=method, opt_type=opt_type, simplify=simplify)


def iterate_expanding(G, method=SEMANTIC, opt_type=INCLUSION, simplify=False):
    if method == SEMANTIC:
        R = parallel_iteration(G, expanding_semantic, opt_type=opt_type)
    elif method == SYNTACTIC:
        R = parallel_iteration(G, expanding_syntactic, opt_type=opt_type)

    if simplify:
        simplify_all_formulas(R)
    return R


def iterate_simple(G, method=SEMANTIC, opt_type=INCLUSION, simplify=False):
    if method == SEMANTIC:
        R = parallel_iteration(G, simple_semantic, opt_type=opt_type)
    elif method == SYNTACTIC:
        R = parallel_iteration(G, simple_syntactic, opt_type=opt_type)

    if simplify:
        simplify_all_formulas(R)
    return R


def iterate_augmenting(G, method=SEMANTIC, opt_type=INCLUSION, simplify=False):
    if method == SEMANTIC:
        R = parallel_iteration(G, augmenting_semantic, opt_type=opt_type)
    elif method == SYNTACTIC:
        R = parallel_iteration(G, augmenting_syntactic, opt_type=opt_type)

    if simplify:
        simplify_all_formulas(R)
    return R


def iterate_ring(G, method=SEMANTIC, opt_type=INCLUSION, simplify=False):
    if method == SEMANTIC:
        R = parallel_iteration(G, ring_semantic, opt_type=opt_type)
    elif method == SYNTACTIC:
        R = parallel_iteration(G, ring_syntactic, opt_type=opt_type)
    
    if simplify:
        simplify_all_formulas(R)
    return R


def augmenting_semantic(G, center, atoms, opt_type=INCLUSION):
    dist_str = create_distance_string(G)
    ecc = nx.eccentricity(G, center)

    center_models = set()
    models = augmenting_iteration_maximal_answer_sets(G, dist_str, center, ecc)
    node_model_dict = dict()

    for model in models:
        for term in model:
            if term.name() == 'tv':
                center_node, node, atom_fun, truth_value = term.args()
                atom = symbols(atom_fun.name())
                if center_node == node:
                    node_model_dict[atom] = truth_value

        true_atoms = frozenset([atom for atom in node_model_dict if node_model_dict[atom] == 1])
        center_models.add(true_atoms)

    formula = formula_from_models(center_models, atoms)
    return {center: formula}


def augmenting_syntactic(G, center, atoms, opt_type=INCLUSION):
    dist_str = create_distance_string(G)
    ecc = nx.eccentricity(G, center)

    answer_sets = augmenting_iteration_maximal_answer_sets(G, dist_str, center, ecc)

    eq_sets = []

    for answer_set in answer_sets:
        current_eq_set = defaultdict(set)
        for term in answer_set:
            if term.name() == 'eq':
                center_node, atom_fun, X, Y = term.args()
                atom = symbols(atom_fun.name())
                if center_node == X:
                    current_eq_set[Y].add(atom)

        #print("CURRENT EQ SET = {}".format(current_eq_set))
        eq_sets.append(current_eq_set)

    #print("ALL EQ SETS AT RADIUS {} = {}".format(radius, eq_sets))

    formula = formula_from_eq_sets(G, center, eq_sets, atoms)
    return {center: formula}


def ring_semantic(G, center, atoms, opt_type=INCLUSION):
    dist_str = create_distance_string(G)
    ecc = nx.eccentricity(G, center)

    iteration_model_sets = []

    for radius in range(1, ecc+1):
        center_models = set()
        models = expanding_maximal_answer_sets(G, dist_str, center, radius, atoms=atoms, neighborhood_type=RING, 
                                               method=SEMANTIC, opt_type=opt_type)
        node_model_dict = dict()

        for model in models:
            for term in model:
                if term.name() == 'tv':
                    center_node, node, atom_fun, truth_value = term.args()
                    atom = symbols(atom_fun.name())
                    if center_node == node:
                        node_model_dict[atom] = truth_value

            true_atoms = frozenset([atom for atom in node_model_dict if node_model_dict[atom] == 1])
            center_models.add(true_atoms)

        iteration_model_sets.append(frozenset(center_models))

        mid_formula = formula_from_models(center_models, atoms)
        G.clear_formulas_from(center)
        G.add_formula(center, mid_formula)

    formula = formula_from_models(center_models, atoms)
    simplified_formula = simplify_logic(formula)
    return {center: simplified_formula}


def ring_syntactic(G, center, atoms, opt_type=INCLUSION):
    dist_str = create_distance_string(G)
    ecc = nx.eccentricity(G, center)

    #print("CENTER = {}".format(center))
    #print("Eccentricity = {}".format(ecc))

    for radius in range(1, ecc+1):
        eq_sets = []

        #print("RADIUS = {}".format(radius))
        #print(G.to_asp(atoms))

        answer_sets = expanding_maximal_answer_sets(G, dist_str, center, radius, atoms=atoms, neighborhood_type=RING,
                                               method=SYNTACTIC, opt_type=opt_type)

        for answer_set in answer_sets:
            # current_eq_set is a mapping like current_eq_set[2] = {p,q,r}, 
            # current_eq_set[3] = {p,q}, all with respect to a given node (e.g. node 1)
            current_eq_set = defaultdict(set)
            for term in answer_set:
                if term.name() == 'eq':
                    center_node, atom_fun, X, Y = term.args()
                    atom = symbols(atom_fun.name())
                    if center_node == X:
                        current_eq_set[Y].add(atom)

            #print("CURRENT EQ SET = {}".format(current_eq_set))
            eq_sets.append(current_eq_set)

        #print("ALL EQ SETS AT RADIUS {} = {}".format(radius, eq_sets))

        mid_formula = formula_from_eq_sets(G, center, eq_sets, atoms)
        G.clear_formulas_from(center)
        G.add_formula(center, mid_formula)

    final_formula = G.formula_conj(center)
    return {center: final_formula}



def serial_iteration(G, iteration_function, opt_type=INCLUSION):
    """Applies ``iteration_function`` over all nodes in ``G`` in a *serial fashion* (i.e. one 
    node at a time).
    
    Parameters
    ----------
    G : An EquibelGraph object
    iteration_function : A function that conforms to the following input/output interface: 
                         **Input:** Takes a graph ``G``, a node ``center`` for which to compute 
                                    the results of the iteration, and a set of ``atoms``.
                         **Output:** Returns a singleton dictionary of the form ``{ center: formula }``
                                     mapping the node ``center`` to a formula resulting from the iteration.
    """
    atoms = G.atoms()
    final_formula_dict = dict()

    for center in G:
        result = iteration_function(copy.deepcopy(G), center, atoms, opt_type=opt_type)
        final_formula_dict.update(result)

    R = copy.deepcopy(G)
    R.clear_formulas()
    for node in final_formula_dict:
        R.add_formula(node, final_formula_dict[node])

    return R


def parallel_iteration(G, iteration_function, opt_type=INCLUSION):
    """Applies ``iteration_function`` over all nodes in ``G`` *in parallel* (using process pools).

    Parameters
    ----------
    G : An EquibelGraph object
    iteration_function : A function that conforms to the following input/output interface: 
                         **Input:** Takes a graph ``G``, a node ``center`` for which to compute 
                                    the results of the iteration, and a set of ``atoms``.
                         **Output:** Returns a singleton dictionary of the form ``{ center: formula }``
                                     mapping the node ``center`` to a formula resulting from the iteration.
    """
    atoms = G.atoms()

    # Using "processes=None" results in as many processes being created as 
    # there are cores (real or virtual) on the current machine.
    pool = mp.Pool(processes=None)
    results = [pool.apply_async(iteration_function, (G, center, atoms), {"opt_type": opt_type}) for center in G.nodes()]
    output = [p.get() for p in results]
    pool.close()
    pool.join()

    final_formula_dict = merge_dicts(output)

    R = copy.deepcopy(G)
    R.clear_formulas()
    for node in final_formula_dict:
        R.add_formula(node, final_formula_dict[node])

    return R


def merge_dicts(dictionaries):
    """Merges multiple separate dictionaries into a single dictionary.

    Parameters
    ----------
    dictionaries : An iterable container of Python dictionaries.

    Returns
    -------
    merged : A single dictionary that represents the result of merging the all the 
             dicts in ``dictionaries``.

    Example
    -------
    The primary purpose of this function is to create a single dictionary 
    by combining multiple singleton dictionaries, as shown in the following example:

    >>> dicts = [{'a': 1}, {'b': 2}, {'c': 3}]
    >>> eb.merge_dicts(dicts)
    {'a': 1, 'c': 3, 'b': 2}
    """
    merged = dictionaries[0].copy()
    for i in range(1, len(dictionaries)):
        merged.update(dictionaries[i])
    return merged


def print_formulas(G):
    """Pretty-prints the formulas associated with nodes in ``G``.

    Parameters
    ----------
    G : An ``EquibelGraph`` object
    """
    for node in G.nodes():
        print("Node {}:".format(node))
        pprint(G.formula_conj(node))
    print("\n")


def create_distance_string(G):
    """Creates a string containing the ASP encoding of the shortest-path 
    distances between all pairs of nodes in ``G``.

    Parameters
    ----------
    G : An EquibelGraph object.

    Returns
    -------
    dist_str : A string containing ``dist/3`` predicates, where ``dist(x,y,d)``
               represents that the distance between nodes ``x`` and ``y`` is ``d``.

    Example
    -------
    >>> G = eb.path_graph(3)
    >>> print(eb.create_distance_string(G))
    dist(0,0,0).
    dist(0,1,1).
    dist(0,2,2).
    dist(1,0,1).
    dist(1,1,0).
    dist(1,2,1).
    dist(2,0,2).
    dist(2,1,1).
    dist(2,2,0).
    """
    dist_str = ""
    lengths = nx.all_pairs_shortest_path_length(G)
    for node1 in lengths:
        for node2 in lengths[node1]:
            dist = lengths[node1][node2]
            dist_str += "dist({0},{1},{2}).\n".format(node1, node2, dist)
    return dist_str


def formula_from_models(models, alphabet):
    """Creates a formula in disjunctive normal form (DNF) given a set of models 
    and an alphabet.

    Parameters
    ----------
    models   : An iterable container (set, list, etc.) of *sets of atoms*, where 
               an atom is represented by a Sympy symbol
    alphabet : An iterable container of atoms, represented by Sympy symbols

    Example
    -------
    >>> p,q,r,s = [eb.parse_formula(f) for f in "pqrs"]
    >>> alphabet = [p,q,r,s]
    >>> models = [{p,q}]
    >>> eb.formula_from_models(models, alphabet)
    And(Not(r), Not(s), p, q)

    >>> models = [{p,q}, {p}]
    >>> eb.formula_from_models(models, alphabet)
    Or(And(Not(q), Not(r), Not(s), p), And(Not(r), Not(s), p, q))
    """
    conjuncts = set()
    for model in models:
        conj = true
        for atom in alphabet:
            if atom in model:
                conj &= atom
            else:
                conj &= ~atom
        conjuncts.add(conj)
    return disjunction(conjuncts)


def conjunction(formulas):
    """Computes the conjunction of a set of propositional formulas.
    
    Parameters
    ----------
    formulas : an iterable container of Sympy formulas

    Example
    -------
    >>> formulas = [eb.parse_formula(s) for s in "pqrst"]
    >>> formulas
    [p, q, r, s, t]
    >>> eb.conjunction(formulas)
    And(p, q, r, s, t)
    """
    return And(*formulas)


def disjunction(formulas):
    """Computes the disjunction of a set of propositional formulas.
    
    Parameters
    ----------
    formulas : An iterable container of Sympy formulas

    Example
    -------
    >>> formulas = [eb.parse_formula(s) for s in "pqrst"]
    >>> formulas
    [p, q, r, s, t]
    >>> eb.disjunction(formulas)
    Or(p, q, r, s, t)
    """
    return Or(*formulas)
