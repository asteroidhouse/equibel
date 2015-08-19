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
%atom(P)   :- atom(_,P).

% The first argument is the center node of the star graph under consideration.
%{ eq(N,P,M,N) : edge(M,N), atom(N,P), M < N }.
%{ eq(N,P,M,N) : edge(M,N), atom(M,P), M < N }.

{ eq(N,P,M,N) : edge(M,N), atom(N,P) }.
{ eq(N,P,M,N) : edge(M,N), atom(M,P) }.

% Makes equivalences symmetric
eq(N,P,N,M) :- eq(N,P,M,N).

{ tv(N,N,P,1) ; tv(N,N,P,0) } == 1 :- atom(N,P).
{ tv(N,N,P,1) ; tv(N,N,P,0) } == 1 :- edge(X,N), atom(X,P).

% N = centre node of the star graph
% X = any node in the star graph centered at N
% P = an atom that either occurs in some formula of X
{ tv(N,X,P,1) ; tv(N,X,P,0) } == 1 :- edge(X,N), atom(X,P).
{ tv(N,X,P,1) ; tv(N,X,P,0) } == 1 :- edge(X,N), atom(N,P).

%1 { tv(N,X,P,1) ; tv(N,X,P,0) } 1 :- atom(X,P), node(N), node(X).
%1 { tv(N,X,P,1) ; tv(N,X,P,0) } 1 :- atom(N,P), node(N), node(X).

:- eq(N,P,M,N), edge(M,N), tv(N,N,P,V), tv(N,M,P,W), V != W.

satisfied(N,X,P) :- tv(N,X,P,1), atom(X,P).
satisfied(N,X,F) :- F = and(A,B), satisfied(N,X,A), satisfied(N,X,B), subformula(X,F), subformula(X,A), subformula(X,B).
satisfied(N,X,F) :- F = or(A,B),  satisfied(N,X,A), subformula(X,F), subformula(X,A), subformula(X,B).
satisfied(N,X,F) :- F = or(A,B),  satisfied(N,X,B), subformula(X,F), subformula(X,A), subformula(X,B).
satisfied(N,X,F) :- F = implies(A,B),  not satisfied(N,X,A), node(N), subformula(X,F), subformula(X,A), subformula(X,B).
satisfied(N,X,F) :- F = implies(A,B),      satisfied(N,X,B), subformula(X,F), subformula(X,A), subformula(X,B).
satisfied(N,X,F) :- F = iff(A,B),          satisfied(N,X,A), satisfied(N,X,B), subformula(X,F), subformula(X,A), subformula(X,B).
satisfied(N,X,F) :- F = iff(A,B),      not satisfied(N,X,A), not satisfied(N,X,B), node(N), subformula(X,F), subformula(X,A), subformula(X,B).
satisfied(N,X,F) :- F = neg(A),        not satisfied(N,X,A), node(N), subformula(X,F), subformula(X,A).

%:- formula(X,F), node(N), not satisfied(N,X,F).

% OR BOTH OF THESE:
:- formula(N,F), node(N), not satisfied(N,N,F).
:- formula(X,F), edge(X,N), not satisfied(N,X,F).

_heuristic(eq(N,P,N,M), true, 1) :- atom(N,P), edge(M,N).
_heuristic(eq(N,P,N,M), true, 1) :- atom(M,P), edge(M,N).

#show _heuristic/3.
#show eq/4.
#show tv/4.
