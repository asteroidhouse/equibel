"""Provides drawing functions that enable visualization of:

1. Arbitrary graphs and associated scenarios;
2. Model graphs corresponding to base graphs, for the 
   restricted case where the base graphs are paths.

This file defines functions that extend the graph drawing capabilities 
of NetworkX by adding the option to display formulas associated with nodes.

Visualization of model graphs is limited to the case where the 
base graph is a path graph; this is not due to technical constraints, 
but rather due to the fact that it is difficult to spatially lay 
out nodes of arbitrary graphs in such a way that the resulting model 
graph is human-readable.
"""
#    Copyright (C) 2016
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.
from __future__ import absolute_import

from collections import defaultdict
from matplotlib.patches import Rectangle

import matplotlib.pyplot as plt

from sympy import pprint, satisfiable, to_cnf, simplify, latex
import networkx as nx
import equibel as eb

from equibel.graph import EquibelGraph

import copy


def copy_dict(source_dict, diffs):
    """Returns a copy of source_dict, updated with the new key-value pairs in diffs."""
    result = dict(source_dict)
    result.update(diffs)
    return result


def tablize(atoms, truths={}):
    if not atoms:
        yield truths
    else:
        curr_atom = next(iter(atoms))
        for truth_val in [True, False]:
            for model in tablize(atoms-{curr_atom}, copy_dict(truths, {curr_atom: truth_val})):
                yield model


def models_with_all_atoms(formula, atoms):
    """Takes a formula and a set of atoms (that do not necessarily appear in the formula), 
    and returns a set of *models* of the formula, where each model is represented by a 
    *dictionary* that maps each atom to a Boolean value, where atoms are drawn from the 
    set of atoms that appear in ``formula`` *and* the set of atoms represented by ``atoms``.

    Parameters
    ----------
    formula : A Sympy formula.
    atoms : A set of Sympy atoms.

    Example
    -------
    >>> p,q,r = [eb.parse_formula(letter) for letter in "pqr"]
    >>> f = p | q
    >>> eb.models_with_all_atoms(f, {p,q})
    [{p: True, q: True}, 
     {p: True, q: False},
     {p: False, q: True}]
    >>> eb.models_with_all_atoms(f, {p,q,r})
    [{p: True, q: True, r: True}, 
     {p: True, q: True, r: False},
     {p: True, q: False, r: True},
     {p: True, q: False, r: False},
     {p: False, q: True, r: True},
     {p: False, q: True, r: False}]
    """
    if formula == True:
        return [model for model in tablize(atoms)]

    original_models = [model for model in satisfiable(formula, all_models=True)]
    extra_atoms = atoms - formula.atoms()

    if not extra_atoms:
        return original_models
    else:
        models_all_atoms = []
        for model in original_models:
            models_all_atoms += [updated_model for updated_model in tablize(extra_atoms, model)]
        return models_all_atoms
        


def model_set(model):
    """Converts a model from a dictionary representation to a set representation.

    Given a ``model`` represented by a dictionary mapping atoms to Boolean values, 
    this function returns the *set* of atoms that are mapped to ``True`` in the dictionary.

    Paramters
    ---------
    model : A dictionary mapping atoms to Boolean values.

    Example
    -------
    >>> p,q,r = [eb.parse_formula(letter) for letter in "pqr"]
    >>> eb.model_set({p: True, q: False, r: True})
    set([p, r])
    """
    return set([atom for atom in model if model[atom] == True])


def symmetric_diff(a,b):
    """Computes the symmetric difference of sets ``a`` and ``b``."""
    return a ^ b


def allmin(lst,less_than=None):
    if not less_than:
        less_than = lambda x,y: x < y

    min_lst = []
    for a in lst:
        found_subset = False
        for b in lst:
            if less_than(b,a):
                found_subset = True
                break
        if not found_subset:
            min_lst.append(a)
    return min_lst


def min_model_edges(edge_change_sets):
    unique_min_model_edge_dict = defaultdict(list)
    duplicated_min_model_edge_dict = defaultdict(list)
    
    for edge in edge_change_sets:
        change_sets = edge_change_sets[edge]
        min_change_sets = allmin(change_sets, lambda x,y: x[1] < y[1])
        
        for s in min_change_sets:
            found_duplicate = False
            for t in min_change_sets:
                if s != t and s[1] == t[1]:
                    found_duplicate = True
                    break
            if found_duplicate:
                duplicated_min_model_edge_dict[edge].append(s)
            else:
                unique_min_model_edge_dict[edge].append(s)
    
    return (unique_min_model_edge_dict, duplicated_min_model_edge_dict)


def draw_graph(G, pos=None):
    if not pos:
        pos = nx.spring_layout(G)

    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 10
    fig_size[1] = 8

    plt.figure()

    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)

    for node in G.nodes():
        x, y = pos[node]
        plt.text(x, y + 0.1, "${}$".format(latex(G.formula_conj(node))), fontsize=16, horizontalalignment='center')
    
    plt.axis("off")


def draw_model_lifting(G, pos=None, show_only_min_edges=False, highlight_nodes=[], highlight_color='#33FF99'):
    if not pos:
        pos = nx.spring_layout(G)

    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 20
    fig_size[1] = 18

    plt.figure()

    atoms = G.atoms()
    model_pos = dict()
    lifting = EquibelGraph()
    model_nodes = defaultdict(list)
    model_num = 1
    
    plt.axis('off')

    for node in G.nodes():
        x,y = pos[node]

        formula = G.formula_conj(node)
        models = models_with_all_atoms(formula, atoms)
        
        num_models = len(models)
        
        ######################################################################
        ###   PUT RECTANGLES AROUND MODELS CORRESPONDING TO THE SAME NODE  ###
        ######################################################################
        currentAxis = plt.gca()
        if node in highlight_nodes:
            currentAxis.add_patch(Rectangle((x - 0.3, y - num_models + 0.5), 0.6, num_models, facecolor=highlight_color, alpha=0.3))
        else:
            currentAxis.add_patch(Rectangle((x - 0.3, y - num_models + 0.5), 0.6, num_models, facecolor="yellow", alpha=0.3))
        plt.text(x, y + 0.8, "{}".format(node), fontsize=20, horizontalalignment='center')
        ######################################################################

        cur_mod_num = 0
        
        for model in models:
            lifting.add_node(model_num, model=model_set(model))
            model_nodes[node].append(model_num)
            model_pos[model_num] = (x, y - cur_mod_num)
            model_num += 1
            cur_mod_num += 1
    
    
    edge_change_sets = defaultdict(list)

    for (node1, node2) in G.edges():
        for model_node1 in model_nodes[node1]:
            for model_node2 in model_nodes[node2]:
                model1 = lifting.node[model_node1]['model']
                model2 = lifting.node[model_node2]['model']
                lifting.add_edge(model_node1, model_node2, label=symmetric_diff(model1, model2))
                edge_change_sets[(node1,node2)].append(((model_node1,model_node2),symmetric_diff(model1, model2)))
    
    
    (unique_dict, duplicated_dict) = min_model_edges(edge_change_sets)
    
    unique_min_model_edges = [tup for item in unique_dict for tup in unique_dict[item]]
    duplicated_min_model_edges = [tup for item in duplicated_dict for tup in duplicated_dict[item]]
    
    nx.draw_networkx_nodes(lifting, model_pos, node_size=400, node_color='#4444FF')
    nx.draw_networkx_labels(lifting, model_pos)
    
    if not show_only_min_edges:
        nx.draw_networkx_edges(lifting, model_pos)
        
    
    nx.draw_networkx_edges(lifting, model_pos, edgelist=[item[0] for item in unique_min_model_edges], 
                           width=4, edge_color='red')
    nx.draw_networkx_edges(lifting, model_pos, edgelist=[item[0] for item in duplicated_min_model_edges], 
                            width=4, edge_color='orange')
    
    # Specifiy edge labels explicitly
    edge_labels = dict([((u,v), d['label']) for u,v,d in lifting.edges(data=True)])
    
    if not show_only_min_edges:
        nx.draw_networkx_edge_labels(lifting, model_pos, edge_labels=edge_labels, label_pos=0.8, rotate=False, font_size=11,
                                     bbox=dict(facecolor='#EEEEEE', edgecolor='black', boxstyle='round,pad=0.3'))
    
    unique_edge_labels = {(u,v): "{{{}}}".format(', '.join(sorted(str(item) for item in s))) for ((u,v),s) in unique_min_model_edges}
    nx.draw_networkx_edge_labels(lifting, model_pos, edge_labels=unique_edge_labels, label_pos=0.8, rotate=False, font_size=11,
                                 bbox=dict(facecolor='#FFAAAA', edgecolor='red', boxstyle='round,pad=0.3'))
    
    duplicated_edge_labels = {(u,v): "{{{}}}".format(', '.join(sorted(str(item) for item in s))) for ((u,v),s) in duplicated_min_model_edges}
    nx.draw_networkx_edge_labels(lifting, model_pos, edge_labels=duplicated_edge_labels, label_pos=0.8, rotate=False, font_size=11,
                                 bbox=dict(facecolor='#FFFFAA', edgecolor='orange', boxstyle='round,pad=0.3'))
    
    
    for node in G.nodes():
        for model_node in model_nodes[node]:
            x,y = model_pos[model_node]
            sorted_strings_for_label = sorted(str(item) for item in lifting.node[model_node]['model'])
            above_node_label = "{{{}}}".format(', '.join(sorted_strings_for_label))
            plt.text(x, y + 0.2, above_node_label, fontsize=12, horizontalalignment='center')

    #plt.show()



def draw_path_model_lifting(G, R1=None, R2=None, show_only_min_edges=True):
    if R1 is not None and R2 is not None:
        diff_nodes = find_diff_nodes(R1, R2)
    else:
        diff_nodes = []

    y_coord = 1
    x_coord = 1

    pos = dict()
    for node in G:
        pos[node] = (x_coord, y_coord)
        x_coord += 2

    draw_model_lifting(G, pos, show_only_min_edges=True, highlight_nodes=diff_nodes)


def find_diff_nodes(S,T):
    """Returns a list of nodes that have different formulas in graphs S and T."""
    diff_nodes = []
    for node in S:
        s_formula = S.formula_conj(node)
        t_formula = T.formula_conj(node)
        if s_formula != t_formula:
            diff_nodes.append(node)
    return diff_nodes
