edge(X,Y) :- edge(Y,X).

{ eq(center,Atom,X,Y) : atom(Atom), n_edge(center,radius,X,Y) }.
{ tv(center,X,Atom,0) ; tv(center,X,Atom,1) } == 1 :- n_node(center,radius,X), atom(Atom).
:- eq(center,Atom,X,Y), tv(center,X,Atom,Val1), tv(center,Y,Atom,Val2), Val1 != Val2.

sat(center,X,Atom) :- tv(center,X,Atom,1).
sat(center,X,F) :- F = and(A,B), sat(center,X,A), sat(center,X,B), subformula(X,A), subformula(X,B), subformula(X,F).
sat(center,X,F) :- F = or(A,B), sat(center,X,A), subformula(X,A), subformula(X,B), subformula(X,F).
sat(center,X,F) :- F = or(A,B), sat(center,X,B), subformula(X,A), subformula(X,B), subformula(X,F).

sat(center,X,F) :- F = implies(A,B), not sat(center,X,A), node(center), subformula(X,A), subformula(X,B), subformula(X,F).
sat(center,X,F) :- F = implies(A,B),     sat(center,X,B), subformula(X,A), subformula(X,B), subformula(X,F).

sat(center,X,F) :- F = iff(A,B), sat(center,X,A), sat(center,X,B), subformula(X,A), subformula(X,B), subformula(X,F).
sat(center,X,F) :- F = iff(A,B), not sat(center,X,A), not sat(center,X,B), node(center), subformula(X,A), subformula(X,B), subformula(X,F).

sat(center,X,F) :- F = neg(A), not sat(center,X,A), node(center), subformula(X,A), subformula(X,F).

:- formula(X,F), n_node(center,radius,X), not sat(center,X,F).

_heuristic(eq(center,Atom,X,Y), true, 1) :- atom(Atom), n_edge(center,radius,X,Y).

#show eq/4.
#show tv/4.
#show _heuristic/3.
