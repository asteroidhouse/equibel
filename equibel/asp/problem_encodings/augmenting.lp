edge(X,Y) :- edge(Y,X).

n_node(center,Radius,X) :- dist(center,X,D), D <= Radius, Radius = 1..eccentricity.
n_edge(center,Radius,X,Y) :- edge(X,Y), n_node(center,Radius,X), n_node(center,Radius,Y), dist(center,X,D1), dist(center,Y,D2), D1 != D2, Radius = 1..eccentricity.

{ eq(center,Distance,Atom,X,Y) : atom(Atom), edge(X,Y), dist(center,X,Distance-1), dist(center,Y,Distance) } :- Distance=1..eccentricity.
{ eq(center,Distance,Atom,X,Y) : atom(Atom), edge(X,Y), dist(center,Y,Distance-1), dist(center,X,Distance) } :- Distance=1..eccentricity.

eq(center,Atom,X,Y) :- eq(center,_,Atom,X,Y).

{ tv(center,X,Atom,0) ; tv(center,X,Atom,1) } == 1 :- node(X), atom(Atom).
:- eq(center,Atom,X,Y), tv(center,X,Atom,Val1), tv(center,Y,Atom,Val2), Val1 != Val2.

sat(center,X,Atom) :- tv(center,X,Atom,1).
sat(center,X,F) :- F = and(A,B), sat(center,X,A), sat(center,X,B), subformula(X,F), subformula(X,A), subformula(X,B).
sat(center,X,F) :- F = or(A,B),  sat(center,X,A), subformula(X,F), subformula(X,A), subformula(X,B).
sat(center,X,F) :- F = or(A,B),  sat(center,X,B), subformula(X,F), subformula(X,A), subformula(X,B).
sat(center,X,F) :- F = implies(A,B),  not sat(center,X,A), subformula(X,F), subformula(X,A), subformula(X,B).
sat(center,X,F) :- F = implies(A,B),      sat(center,X,B), subformula(X,F), subformula(X,A), subformula(X,B).
sat(center,X,F) :- F = iff(A,B),          sat(center,X,A), sat(center,X,B), subformula(X,F), subformula(X,A), subformula(X,B).
sat(center,X,F) :- F = iff(A,B),      not sat(center,X,A), not sat(center,X,B), subformula(X,F), subformula(X,A), subformula(X,B).
sat(center,X,F) :- F = neg(A),        not sat(center,X,A), subformula(X,F), subformula(X,A).

:- formula(X,F), not sat(center,X,F).

_heuristic(eq(center,Distance,Atom,X,Y), true, eccentricity-Distance+1) :- atom(Atom), edge(X,Y), dist(center,X,Distance-1), dist(center,Y,Distance), Distance=1..eccentricity.
_heuristic(eq(center,Distance,Atom,X,Y), true, eccentricity-Distance+1) :- atom(Atom), edge(X,Y), dist(center,Y,Distance-1), dist(center,X,Distance), Distance=1..eccentricity.

#show tv/4.
%#show eq/5.
#show eq/4.
#show _heuristic/3.
