_heuristic(eq(P,X,Y), true, 1) :- atom(P), edge(X,Y), X < Y.

#show _heuristic/3.
#show eq/3.
#show tv/3.
