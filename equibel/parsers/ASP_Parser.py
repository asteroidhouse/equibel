#    Copyright (C) 2014-2015 by
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    BSD license.

from __future__ import absolute_import

import sys
from equibel.PredicateTree import predicate_parser

#TODO: Handle cases where the input is UNSATISFIABLE - now an error occurs somewhere else.

def parse_model(line):
    predicate_strs = line.split()
    predicates = [predicate_parser.parse_predicate(pred_str) for pred_str in predicate_strs]
    #print([str(pred) for pred in predicates])

    predicate_groups = dict()
    predicate_names = set(pred.name for pred in predicates)
    for pred_name in predicate_names:
        predicate_groups[pred_name] = [pred for pred in predicates if pred.name == pred_name]

    return predicate_groups
    

def parse_models(lines):
    ignore_lines = ['Optimization', 'OPTIMUM', 'Answer', 'SATISFIABLE']

    models = []
    for line in lines:
        if not line:
            continue
        if any(line.startswith(ignore) for ignore in ignore_lines):
            continue
        models.append(parse_model(line))
    return models

def parse_asp(text):
    lines = text.strip().split("\n")
    return parse_models(lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python3 ASP_Parser.py filename')
        sys.exit(1)

    filename = sys.argv[1]

    f = open(filename, 'r')
    text = f.read()

    try:
        models = parse_asp(text)
        for model in models:
            print("Model")
            for pred_name in model:
                print("{0}: ".format(pred_name))
                for predicate in model[pred_name]:
                    print(predicate)
                print()
    except Exception as err:
        print(err)
