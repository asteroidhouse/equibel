#const _asprin_n=0.
#const _asprin_no_print=-1.

#preference(p(Distance),superset) {
    eq(center,Distance,Atom,X,Y) : atom(Atom), edge(X,Y), dist(center,X,Distance-1), dist(center,Y,Distance);
    eq(center,Distance,Atom,X,Y) : atom(Atom), edge(X,Y), dist(center,Y,Distance-1), dist(center,X,Distance);
    eq(center,Distance,Atom,X,Y) : atom(Atom), edge(X,Y), dist(center,X,Distance), dist(center,Y,Distance)
} : Distance=1..eccentricity.

#preference(prioritized_preferences,lexico) {
    Distance :: name(p(eccentricity-Distance+1))
} : Distance=1..eccentricity.

#optimize(prioritized_preferences).

