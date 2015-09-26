#program expand(radius).

_heuristic(eq(Center,Atom,X,Y), true, 1) :- star_edge(Center,X,Y), star_atom(Center,Atom), X < Y.

#show _heuristic/3.
#show eq/4.
#show tv/4.
