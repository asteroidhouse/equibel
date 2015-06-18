% We make equivalences symmetric.
eq(P,X,Y) :- eq(P,Y,X).

% We find the transitive closure of the equivalences.
eq(P,X,Y) :- eq(P,X,Z), eq(P,Z,Y), X != Y.
