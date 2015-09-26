#program expand(radius).

edge(X,Y) :- edge(Y,X).

subformula(N,S) :- formula(N,S).
subformula(N,S) :- subformula(N, and(S,_)).
subformula(N,S) :- subformula(N, and(_,S)).
subformula(N,S) :- subformula(N, or(S,_)).
subformula(N,S) :- subformula(N, or(_,S)).
subformula(N,S) :- subformula(N, implies(S,_)).
subformula(N,S) :- subformula(N, implies(_,S)).
subformula(N,S) :- subformula(N, iff(S,_)).
subformula(N,S) :- subformula(N, iff(_,S)).
subformula(N,S) :- subformula(N, neg(S)).

compound_prop(N,F) :- F = and(A,B), subformula(N,F), subformula(N,A), subformula(N,B).
compound_prop(N,F) :- F = or(A,B), subformula(N,F), subformula(N,A), subformula(N,B).
compound_prop(N,F) :- F = implies(A,B), subformula(N,F), subformula(N,A), subformula(N,B).
compound_prop(N,F) :- F = iff(A,B),	subformula(N,F), subformula(N,A), subformula(N,B).
compound_prop(N,F) :- F = neg(A), subformula(N,F), subformula(N,A).

atom(X,Atom) :- subformula(X,Atom), not compound_prop(X,Atom).
%atom(Atom)   :- atom(_,Atom).

star_node(Center,X) :- dist(Center,X,D), D <= radius.
star_edge(Center,X,Y) :- edge(X,Y), star_node(Center,X), star_node(Center,Y).
star_atom(Center,Atom) :- star_node(Center,X), atom(X,Atom).

{ eq(Center,Atom,X,Y) : star_atom(Center,Atom), star_edge(Center,X,Y), X < Y } :- node(Center).
{ tv(Center,X,Atom,0) ; tv(Center,X,Atom,1) } == 1 :- star_node(Center,X), star_atom(Center,Atom).
:- eq(Center,Atom,X,Y), tv(Center,X,Atom,Val1), tv(Center,Y,Atom,Val2), Val1 != Val2.

sat(Center,X,Atom) :- tv(Center,X,Atom,1).
sat(Center,X,F) :- F = and(A,B), sat(Center,X,A), sat(Center,X,B), subformula(X,A), subformula(X,B), subformula(X,F).
sat(Center,X,F) :- F = or(A,B), sat(Center,X,A), subformula(X,A), subformula(X,B), subformula(X,F).
sat(Center,X,F) :- F = or(A,B), sat(Center,X,B), subformula(X,A), subformula(X,B), subformula(X,F).

sat(Center,X,F) :- F = implies(A,B), not sat(Center,X,A), node(Center), subformula(X,A), subformula(X,B), subformula(X,F).
sat(Center,X,F) :- F = implies(A,B),     sat(Center,X,B), subformula(X,A), subformula(X,B), subformula(X,F).

sat(Center,X,F) :- F = iff(A,B), sat(Center,X,A), sat(Center,X,B), subformula(X,A), subformula(X,B), subformula(X,F).
sat(Center,X,F) :- F = iff(A,B), not sat(Center,X,A), not sat(Center,X,B), node(Center), subformula(X,A), subformula(X,B), subformula(X,F).

sat(Center,X,F) :- F = neg(A), not sat(Center,X,A), node(Center), subformula(X,A), subformula(X,F).

%:- formula(X,F), node(Center), not sat(Center,X,F).
:- formula(X,F), star_node(Center,X), not sat(Center,X,F).
