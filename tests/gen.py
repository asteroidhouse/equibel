from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import time
import subprocess
import signal

from timeit import timeit

import matplotlib.pyplot as plt

import equibel as eb
import formulagen


def create_atom_mapping(atoms):
    mapping = dict()
    for (index, atom) in enumerate(atoms):
        mapping[atom] = index
    return mapping
    

def completion_test(G):
    start_time = time.clock()
    print("STARTING COMPLETION!")
    R = eb.completion(G)
    end_time = time.clock()
    elapsed_time = end_time - start_time
    print("RESULT")
    print_formulas(R)
    print("TIME: {0}".format(elapsed_time))
    print()
    return elapsed_time


def completion_test_debug(G):
    start_time = time.clock()
    R, node_models, num_models, num_terms_list = eb.completion(G, debug=True)
    end_time = time.clock()
    elapsed_time = end_time - start_time
    print()
    print("RESULT")
    print_formulas(R)
    print("TIME: {0}".format(elapsed_time))
    print()

    print("Models for each node: {0}".format(node_models))
    print("Number of models: {0}".format(num_models))
    print("# terms per model: {0}".format(num_terms_list[0]))

    return (elapsed_time, num_models, num_terms_list[0][0], num_terms_list[0][1])


def write_graph_to_file(G, filename):
    atoms = [eb.Prop(atom) for atom in G.atoms()]
    sorted_atoms = tuple(sorted(atoms))
    atom_mapping = create_atom_mapping(sorted_atoms)
    f = open(filename, 'w')
    asp_str = eb.convert_to_asp(G, atom_mapping)
    f.write(asp_str)
    f.close()


def concat(string_list, delim):
    return delim.join(string_list)


def ground_lines(list_of_filenames):
    all_filenames = concat(list_of_filenames, " ")
    command = "gringo {0} | wc -l".format(all_filenames)
    #proc = Popen(command.format(filename), shell=True, stdout=PIPE, universal_newlines=True)
    lines = int(subprocess.check_output(command, shell=True))
    return lines


def time_command(command):
    statement = "subprocess.call(\"{0}\", shell=True)".format(command)
    print(statement)
    elapsed_time = timeit(stmt=statement, setup="import subprocess", number=1)
    print("Elapsed time = {0}".format(elapsed_time))
    return elapsed_time


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


def solving_time_test(G):
    write_graph_to_file(G, "temp_asp_file")
    
    solving_command = "clingo {0} 0 --heuristic=domain --enum-mode=domRec --verbose=0 --quiet=2"

    filenames = ["temp_asp_file", "asp/eq_sets.lp"]
    command = solving_command.format(concat(filenames, " "))
    eq_time = time_command(command)
    
    """
    filenames.append("asp/transitive.lp")
    command = solving_command.format(concat(filenames, " "))
    eq_transitive_time = time_command(command)

    filenames.append("asp/translate.lp")
    command = solving_command.format(concat(filenames, " "))
    eq_translate_time = time_command(command)
    """

    #return (eq_time, eq_transitive_time, eq_translate_time)
    return eq_time

def solving_translate_test(G):
    write_graph_to_file(G, "temp_asp_file")
    
    #solving_command = "clingo {0} 0 --heuristic=domain --enum-mode=domRec --verbose=0 --quiet=2"
    solving_command = "clingo {0} 0 --heuristic=domain --enum-mode=domRec"
    filenames = ["temp_asp_file", "asp/eq_sets.lp", "asp/transitive.lp", "asp/translate.lp"]
    command = solving_command.format(concat(filenames, " "))
    translate_time = time_command(command)

    return translate_time


def print_formulas(G):
    for node_id in G.nodes():
        print("Node {0}: {1}".format(node_id, repr(G.formulas(node_id))))


def generate_graph(graph_gen_func, 
                   formula_gen_func,
                   graph_gen_args={"n": 10},
                   formula_gen_args={"num_vars": 5}):
    G = graph_gen_func(**graph_gen_args)
    for node_id in G.nodes():
        formula = formula_gen_func(**formula_gen_args)
        G.add_formula(node_id, formula)
    print_formulas(G)
    return G


def run_test(test_func, graph_gen_func, formula_gen_func, graph_gen_args, formula_gen_args):
    G = generate_graph(graph_gen_func, formula_gen_func, graph_gen_args, formula_gen_args)
    data = test_func(G)
    return data
    

def run_tests(test_func=completion_test,
              start_num_nodes=5, 
              end_num_nodes=50, 
              step_size=5, 
              repetitions=1,
              graph_gen_func=eb.path_graph,
              formula_gen_func=formulagen.literal_conj,
              num_vars=5,
              timeout=100):
    signal.signal(signal.SIGALRM, handler)
    data = dict()
    num_overtime = 0
    for num_nodes in range(start_num_nodes, end_num_nodes+1, step_size):
        for rep in range(repetitions):
            print("Running tests on {0} nodes, rep {1}...".format(num_nodes, rep+1))

            """
            p = multiprocessing.Process(target=run_test, name="Test", kwargs={'test_func':completion_test_debug,
                                                                              'graph_gen_func':eb.path_graph,
                                                                              'formula_gen_func':formulagen.literal_conj,
                                                                              'graph_gen_args':{"n": num_nodes},
                                                                              'formula_gen_args':{"num_vars": num_vars}})
            p.start()
            p.join(timeout)

            # If thread is active
            if p.is_alive():
                print("The test is still running... let's kill it...")

                p.terminate()
                p.join()
            """
            
            signal.alarm(timeout)

            try:
                current_data = run_test(test_func, graph_gen_func, formula_gen_func, 
                                        graph_gen_args={"n": num_nodes}, 
                                        formula_gen_args={"num_vars": num_vars})
                if num_nodes in data:
                    data[num_nodes].append(current_data)
                else:
                    data[num_nodes] = [current_data]
            except Exception, ex:
                num_overtime += 1
                print(ex)

    return data, num_overtime


def handler(signum, frame):
    print("\nKilling the current run...")
    raise Exception("Computation Time Exceeded :-(")


def line_graph(data):
    averages = {key: (sum(value)/len(value)) for (key,value) in data.items()}
    plt.plot(averages.keys(), averages.values(), 'ro-')
    plt.title("Clingo Solving Times for Star Graphs with 5-Variable Formulas")
    plt.ylabel("Solving Time (seconds)")
    plt.xlabel("Number of Nodes")
    plt.show()


def histogram(data):
    vals = data.values()
    flattened_vals = [x for lst in vals for x in lst]
    plt.hist(flattened_vals, 30, color='g', normed=True)
    plt.title("Completion Time Histogram: 10-Node Star Graph with 4-Variable Formulas")
    plt.ylabel("Frequency")
    plt.xlabel("Completion Time")
    plt.show()
    
def print_model_time_ratios(data):
    for node in data:
        print("Time/Models/Terms For {0} Nodes".format(node))
        print("---------------------------------")
        results = data[node]
        for result in results:
            solving_time, num_models, total_terms, tv_terms = result
            ratio = solving_time / num_models
            print("{0}, {1}, {2}".format(solving_time, num_models, total_terms))
        print()

if __name__ == '__main__':
    reps = 2
    data, num_overtime = run_tests(test_func=solving_time_test,
                         start_num_nodes=3,
                         end_num_nodes=15,
                         step_size=1,
                         repetitions=2,
                         graph_gen_func=eb.path_graph,
                         formula_gen_func=formulagen.literal_conj,
                         num_vars=5,
                         timeout=100)

    print(data)
    print_model_time_ratios(data)

    print("Num overtime = {0}".format(num_overtime))
    print("Percent overtime = {0}".format((num_overtime / (len(data) * reps)) * 100))

    #line_graph(data)
    #histogram(data)
