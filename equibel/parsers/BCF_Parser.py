#    Copyright (C) 2014-2015 by
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


# Can do one of two things here:
#    1) check that there is only one item in the tokens list,
#      and raise an exception if not, or
#    2) ignore any items after the first in the tokens list
#
# Using method (1), "t directed blah" is invalid, while using
# method (2), it is valid. How strict should the parser be?
#
# Since we want good error reporting for improperly formatted
# files, we will go with method (1).
#
# Philosophy: Things MUST be formatted correctly, but the
#           program will show you where any problems are.
#           This is more useful than ignoring an error, since
#           that error may be indicative of other problems
#           that the user did not notice.
def process_type_line(tokens, graph, line_num):
    if not tokens:
        raise FormatError("Empty type line on line {0}".format(line_num))
    if len(tokens) != 1:
        raise FormatError("Expected exactly 1 argument in type line on line {0}, got: \"{1}\""
                          .format(line_num, ", ".join(tokens)))

    graph_type = tokens[0].lower()

    if graph_type == 'directed':
        graph.to_directed()
    elif graph_type == 'undirected':
        graph.to_undirected()
    else:
        raise FormatError("unrecognized graph type on line {0}: \"{1}\""
                          .format(line_num, graph_type))


def process_node_line(tokens, graph, line_num):
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
    if not tokens:
        raise FormatError("Empty atom line on line {0}".format(line_num))

    for token in tokens:
        if not re.match(r'[a-zA-Z][a-zA-Z0-9]*', token):
            raise FormatError("invalid atom name on line {0}: \"{1}\"".format(line_num, token))

        graph.add_atom(token)


def process_weight_line(tokens, graph, line_num):
    if not tokens:
        raise FormatError("Empty weight line on line {0}".format(line_num))
    if len(tokens) != 3:
        raise FormatError("Expected exactly 3 arguments in weight line on line {0}, got: \"{1}\""
                          .format(line_num, ", ".join(tokens)))

    node_str, atom_name, weight_str = tokens

    if not node_str.isdigit():
        raise FormatError("invalid node number on line {0}: \"{1}\"".format(line_num, node_str))
    if not re.match(r'[a-zA-Z][a-zA-Z0-9]*', atom_name):
        raise FormatError("invalid atom name on line {0}: \"{1}\"".format(line_num, atom_name))
    if not weight_str.isdigit():
        raise FormatError("invalid weight on line {0}: \"{1}\"".format(line_num, weight_str))

    node_id = int(node_str)
    weight  = int(weight_str)
    graph.add_weight(node_id, atom_name, weight)


def process_edge_line(tokens, graph, line_num):
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
    if not node_str.isdigit():
        raise FormatError("Invalid node number on line {0}: \"{1}\"".format(line_num, node_str))
    if not formula_str:
        raise FormatError("No formula provided on line {0}".format(line_num))

    node_id = int(node_str)

    # TODO: May raise another exception.
    formula = FormulaParserSim.parse_formula(formula_str)
    graph.add_formula(node_id, formula)


process_line = {
    't': process_type_line,
    'n': process_node_line,
    'a': process_atom_line,
    'w': process_weight_line,
    'e': process_edge_line,
    'f': process_formula_line
}

def parse_bcf(filename):
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
            if line_type in ['t', 'n', 'a', 'w', 'e']:
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


# From StackOverflow
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
