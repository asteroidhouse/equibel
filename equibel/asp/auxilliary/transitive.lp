% Transitiviity
eq(center,Atom,X,Z) :- eq(center,Atom,X,Y), eq(center,Atom,Y,Z), X != Z.

eq(Atom,X,Z) :- eq(Atom,X,Y), eq(Atom,Y,Z), X != Z.
