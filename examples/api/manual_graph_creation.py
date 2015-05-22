import equibel as eb

if __name__ == '__main__':
    G = eb.EquibelGraph()

    # Create edges. The nodes corresponding to the endpoints of 
    # the edges are added automatically if not already present:
    G.add_edges([(1,2), (1,3), (3,4), (2,4)]) 

    # Add formulas to nodes:
    G.add_formula(1, "p")
    G.add_formula(2, "~p & q")
    G.add_formula(3, "r")
    
    # Find the completion of the G-scenario:
    R = eb.completion(G)

    # Print the resulting formulas at each node:
    for node_id in R.nodes():
        print("Node {0}: {1}".format(node_id, R.formulas(node_id)))
