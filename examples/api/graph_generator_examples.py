import equibel as eb


def print_formulas(G):
    for node_id in G.nodes():
        print("Node {0}: {1}".format(node_id, G.formulas(node_id)))


if __name__ == '__main__':

    # ----------------------------------------------------
    #                   PATH GRAPH
    # ----------------------------------------------------

    # Create a path graph on 20 nodes, numbered 0 to 19:
    path20 = eb.path_graph(20, directed=False)
    # Add a formula to the first node in the path:
    path20.add_formula(0, "p")
    # Find the completion:
    result20 = eb.completion(path20)
    # Print formulas at all nodes:
    print_formulas(result20)

    print("\n----------------------------------\n")


    # ----------------------------------------------------
    #                   STAR GRAPH
    # ----------------------------------------------------

    # Create a star graph on 11 nodes: one central node, 
    # and 10 outer nodes. The central node has ID 0, and 
    # the outer nodes have IDs 1 to 10:
    star5 = eb.star_graph(5)
    # Add formulas to nodes. In this case, none of the 
    # formulas conflict, so we expect that in the 
    # completion, the central node 0 will maintain the 
    # conjunction of these formulas:
    star5.add_formula(1, "p")
    star5.add_formula(2, "q")
    star5.add_formula(3, "r")
    star5.add_formula(4, "s")
    star5.add_formula(5, "t")
    # Find the completion:
    result5 = eb.completion(star5)
    # Print the formula in the completion at node 0:
    print(result5.formulas(0))
    

    print("\n----------------------------------\n")
    

    # ----------------------------------------------------
    #                 COMPLETE GRAPH
    # ----------------------------------------------------

    # Create a complete graph on 8 nodes, numbered 0 to 7:
    complete8 = eb.complete_graph(8)
    # Add formulas to nodes. In this case, nodes 0 and 5
    # hold mutually inconsistent beliefs, so we expect 
    # that in the completion, none of the other nodes will 
    # have any opinion on p:
    complete8.add_formula(0, "p")
    complete8.add_formula(5, "~p")
    # Find the completion:
    result8 = eb.completion(complete8)
    # Print all the resultant formulas:
    print_formulas(result8)
    
