n_node(center,radius,center).
n_node(center,radius,X) :- dist(center,X,radius).
n_edge(center,radius,center,X) :- n_node(center,radius,X).
n_edge(center,radius,X,center) :- n_edge(center,radius,center,X). % For edge symmetry.
