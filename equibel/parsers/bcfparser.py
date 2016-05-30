"""Parser for the Belief Change Format (BCF) representation of a graph and 
associated scenario.

An example of the Belief Change Format is as follows:

n 1..5
a p q r

f 1 (-p)
f 3 (*(p q))
f 3 (+(-p r))
f 4 (+(*(p q) r))
f 5 (*(-q r))

e 1 2
e 1 3
e 3 1
e 2 4
e 4 2
e 2 5
e 5 2
e 4 5
"""
#    Copyright (C) 2016
#    Paul Vicol <pvicol@sfu.ca>
#    All rights reserved.
#    MIT license.
from __future__ import absolute_import

import sys
import re

from equibel.graph import EquibelGraph
import equibel.parsers.FormulaParserSim as FormulaParserSim
import equibel.formatters.BCF_Formatter as BCF_Formatter


__all__ = ["parse_bcf"]


class FormatError(Exception):
    pass


def process_node_line(tokens, graph, line_num):
    """
    """
    # There are two cases for valid tokens:
    #    1) The token can be an individual positive integer, like 3, or
    #    2) The token can be a range of the form x..y, where x and y are
    #      positive integers. To keep the parsing simple, whitespace is
    #      not allowed anywhere in the token, so "3.. 5" is invalid.

    if not tokens:
        raise FormatError("Empty node line on line {0}".format(line_num))

    for token in tokens:
        if '..' in token:
            m = re.match(r'([0-9]+)\.\.([0-9]+)', token)
            if not m:
                raise FormatError("Unrecognized range on line {0}: \"{1}\"".format(line_num, token))

            range_start = int(m.group(1))
            range_end   = int(m.group(2))

            if range_start > range_end:
                raise FormatError("End of range is smaller than start of range on line {0}: \"{1}\""
                                  .format(line_num, token))

            node_ids = range(range_start, range_end + 1)
            graph.add_nodes(node_ids)
        elif token.isdigit():
            node_id = int(token)
            graph.add_node(node_id)
        else:
            raise FormatError("Unrecognized node token on line {0}: \"{1}\"".format(line_num, token))


def process_atom_line(tokens, graph, line_num):
    """
    """
    if not tokens:
        raise FormatError("Empty atom line on line {0}".format(line_num))

    for token in tokens:
        if not re.match(r'[a-zA-Z][a-zA-Z0-9]*', token):
            raise FormatError("invalid atom name on line {0}: \"{1}\"".format(line_num, token))

        graph.add_atom(token)


def process_edge_line(tokens, graph, line_num):
    """
    """
    if not tokens:
        raise FormatError("Empty edge line on line {0}".format(line_num))
    if len(tokens) != 2:
        raise FormatError("Expected exactly 2 arguments in edge line on line {0}, got: \"{1}\""
                          .format(line_num, ", ".join(tokens)))

    from_node_str, to_node_str = tokens

    if not from_node_str.isdigit():
        raise FormatError("invalid node number on line {0}: \"{1}\"".format(line_num, from_node_str))
    if not to_node_str.isdigit():
        raise FormatError("invalid node number on line {0}: \"{1}\"".format(line_num, to_node_str))

    from_node_id = int(from_node_str)
    to_node_id = int(to_node_str)
    graph.add_edge(from_node_id, to_node_id)


def process_formula_line(node_str, formula_str, graph, line_num):
    """
    """
    if not node_str.isdigit():
        raise FormatError("Invalid node number on line {0}: \"{1}\"".format(line_num, node_str))
    if not formula_str:
        raise FormatError("No formula provided on line {0}".format(line_num))

    node_id = int(node_str)
    formula = FormulaParserSim.parse_formula(formula_str)
    graph.add_formula(node_id, formula)


process_line = {
    'n': process_node_line,
    'a': process_atom_line,
    'e': process_edge_line,
    'f': process_formula_line
}

def parse_bcf(filename):
    """
    """
    f = open(filename, 'r')

    # Creates the graph used to accumulate the information in the
    # BCF file. As each line is parsed, this graph is updated to
    # maintain the nodes, edges, atoms, weights, and formulas.
    graph = EquibelGraph()

    line_num = 1

    line = f.readline()

    while line:
        tokens = line.split()

        if tokens:
            line_type = tokens[0]
            if line_type in ['n', 'a', 'e']:
                process_line[line_type](tokens[1:], graph, line_num)
            elif line_type == 'f':
                formula_start_line = line_num
                if not tokens[1:]:
                    raise FormatError("Empty formula line on line {0}".format(formula_start_line))
                node_str = tokens[1]

                formula_str = " ".join(tokens[2:])
                while not balanced_parentheses(formula_str):
                    next_line = f.readline()
                    line_num += 1
                    if not next_line:
                        raise FormatError("Unbalanced parentheses on line {0}".format(line_num))

                    # The space ensures that tokens on successive lines don't get compacted into
                    # a single token, i.e. "p\n-q" becomes "p -q" instead of "p-q"
                    formula_str += " " + next_line.strip()

                process_formula_line(node_str, formula_str, graph, formula_start_line)
            elif line_type == 'c':
                pass
            else:
                raise FormatError("Unrecognized line type on line {0}: \"{1}\"".format(line_num, line_type))

        line_num += 1
        line = f.readline()

    f.close()
    return graph


def balanced_parentheses(s):
    stack = []
    push_chars, pop_chars = "({[", ")}]"
    for c in s:
        if c in push_chars:
            stack.append(c)
        elif c in pop_chars:
            if not len(stack):
                return False
            else:
                stack_top = stack.pop()
                balancing_bracket = push_chars[pop_chars.index(c)]
                if stack_top != balancing_bracket:
                    return False

    return not len(stack)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python BCF_Parser.py filename')
        sys.exit(1)

    filename = sys.argv[1]

    try:
        graph = parse_bcf(filename)
        print(BCF_Formatter.convert_to_bcf(graph))
    except FormatError as err:
        print(err)
