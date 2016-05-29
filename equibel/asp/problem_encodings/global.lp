edge(X,Y) :- edge(Y,X).

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

_heuristic(eq(P,X,Y), true, 1) :- atom(P), edge(X,Y), X < Y.

#show _heuristic/3.
%#show tv/3.
#show eq/3.
