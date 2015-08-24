from __future__ import absolute_import
from __future__ import print_function

import time
import subprocess

from timeit import timeit

import matplotlib.pyplot as plt

import equibel as eb
import formulagen


@profile
def completion_test(G):
    start_time = time.clock()
    R = eb.completion(G)
    end_time = time.clock()
    return end_time - start_time


@profile
def write_graph_to_file(G, filename):
    f = open(filename, 'w')
    asp_str = eb.convert_to_asp(G)
    f.write(asp_str)
    f.close()


@profile
def concat(string_list, delim):
    return delim.join(string_list)


@profile
def ground_lines(list_of_filenames):
    all_filenames = concat(list_of_filenames, " ")
    command = "gringo {0} | wc -l".format(all_filenames)
    #proc = Popen(command.format(filename), shell=True, stdout=PIPE, universal_newlines=True)
    lines = int(subprocess.check_output(command, shell=True))
    return lines


@profile
def time_command(command):
    statement = "subprocess.call(\"{0}\", shell=True)".format(command)
    print(statement)
    elapsed_time = timeit(stmt=statement, setup="import subprocess", number=1)
    print("Elapsed time = {0}".format(elapsed_time))
    return elapsed_time


@profile
def lines_test(G):
    write_graph_to_file(G, "temp_asp_file")

    filenames = ["temp_asp_file"]
    graph_lines = ground_lines(filenames)

    filenames.append("asp/eq_sets.lp")
    eq_lines = ground_lines(filenames)

    filenames.append("asp/transitive.lp")
    eq_transitive_lines = ground_lines(filenames)

    filenames.append("asp/translate.lp")
    eq_translate_lines = ground_lines(filenames)

    return (graph_lines, eq_lines, eq_transitive_lines, eq_translate_lines)


@profile
def solving_time_test(G):
    write_graph_to_file(G, "temp_asp_file")
    
    solving_command = "clingo {0} 0 --heuristic=domain --enum-mode=domRec --verbose=0 --quiet=2"

    filenames = ["temp_asp_file", "asp/eq_sets.lp"]
    command = solving_command.format(concat(filenames, " "))
    eq_time = time_command(command)

    filenames.append("asp/transitive.lp")
    command = solving_command.format(concat(filenames, " "))
    eq_transitive_time = time_command(command)

    filenames.append("asp/translate.lp")
    command = solving_command.format(concat(filenames, " "))
    eq_translate_time = time_command(command)

    return (eq_time, eq_transitive_time, eq_translate_time)


@profile
def solving_translate_test(G):
    write_graph_to_file(G, "temp_asp_file")
    
    #solving_command = "clingo {0} 0 --heuristic=domain --enum-mode=domRec --verbose=0 --quiet=2"
    solving_command = "clingo {0} 0 --heuristic=domain --enum-mode=domRec"
    filenames = ["temp_asp_file", "asp/eq_sets.lp", "asp/transitive.lp", "asp/translate.lp"]
    command = solving_command.format(concat(filenames, " "))
    translate_time = time_command(command)

    return translate_time



@profile
def generate_graph(graph_gen_func, 
                   formula_gen_func,
                   graph_gen_args={"n": 10},
                   formula_gen_args={"num_vars": 5}):
    G = graph_gen_func(**graph_gen_args)
    for node_id in G.nodes():
        formula = formula_gen_func(**formula_gen_args)
        G.add_formula(node_id, formula)
    return G


@profile
def run_test(test_func, graph_gen_func, formula_gen_func, graph_gen_args, formula_gen_args):
    G = generate_graph(graph_gen_func, formula_gen_func, graph_gen_args, formula_gen_args)
    data = test_func(G)
    return data
    

@profile
def run_tests(test_func=completion_test,
              start_num_nodes=5, 
              end_num_nodes=50, 
              step_size=5, 
              repetitions=1,
              graph_gen_func=eb.path_graph,
              formula_gen_func=formulagen.literal_conj,
              num_vars=5):
    data = dict()
    for num_nodes in range(start_num_nodes, end_num_nodes+1, step_size):
        for rep in range(repetitions):
            print("Running tests on {0} nodes, rep {1}...".format(num_nodes, rep+1))
            current_data = run_test(test_func, graph_gen_func, formula_gen_func, 
                                    graph_gen_args={"n": num_nodes}, 
                                    formula_gen_args={"num_vars": num_vars})
            if num_nodes in data:
                data[num_nodes].append(current_data)
            else:
                data[num_nodes] = [current_data]

    return data


@profile
def line_graph(data):
    averages = {key: (sum(value)/len(value)) for (key,value) in data.items()}
    plt.plot(averages.keys(), averages.values(), 'ro-')
    plt.title("Clingo Solving Times for Star Graphs with 5-Variable Formulas")
    plt.ylabel("Solving Time (seconds)")
    plt.xlabel("Number of Nodes")
    plt.show()


@profile
def histogram(data):
    vals = data.values()
    flattened_vals = [x for lst in vals for x in lst]
    plt.hist(flattened_vals, 30, color='g', normed=True)
    plt.title("Completion Time Histogram: 10-Node Star Graph with 4-Variable Formulas")
    plt.ylabel("Frequency")
    plt.xlabel("Completion Time")
    plt.show()
    


if __name__ == '__main__':
    data = run_tests(test_func=completion_test,
                     start_num_nodes=3,
                     end_num_nodes=10,
                     step_size=1,
                     repetitions=1,
                     graph_gen_func=eb.star_graph,
                     formula_gen_func=formulagen.literal_conj,
                     num_vars=5)

    print(data)
    
    #line_graph(data)
    #histogram(data)
