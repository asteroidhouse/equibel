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

atom(N,P) :- subformula(N,P), not compound_prop(N,P).
atom(P)   :- atom(_,P).

{ eq(P,X,Y) : atom(P), edge(X,Y), X < Y }.

1 { tv(N,P,1) ; tv(N,P,0) } 1 :- atom(P), node(N).

:- eq(P,X,Y), edge(X,Y), tv(X,P,V), tv(Y,P,W), V != W.

satisfied(N,P) :- tv(N,P,1), atom(N,P).
satisfied(N,F) :- F = and(A,B), satisfied(N,A), satisfied(N,B), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = or(A,B),  satisfied(N,A), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = or(A,B),  satisfied(N,B), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = implies(A,B),  not satisfied(N,A), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = implies(A,B),      satisfied(N,B), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = iff(A,B),          satisfied(N,A), satisfied(N,B), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = iff(A,B),      not satisfied(N,A), not satisfied(N,B), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = neg(A),        not satisfied(N,A), subformula(N,F), subformula(N,A).

:- formula(N,F), not satisfied(N,F).
