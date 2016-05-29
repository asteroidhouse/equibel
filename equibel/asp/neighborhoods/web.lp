n_node(center,radius,X) :- dist(center,X,D), D <= radius.
n_edge(center,radius,X,Y) :- edge(X,Y), n_node(center,radius,X), n_node(center,radius,Y).
