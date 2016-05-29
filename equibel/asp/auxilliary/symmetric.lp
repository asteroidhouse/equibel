% Symmetry
eq(center, Atom, X, Y) :- eq(center, Atom, Y, X).
eq(Atom, X, Y) :- eq(Atom, Y, X).
