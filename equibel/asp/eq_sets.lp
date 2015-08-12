% Edges are bidirectional <-> The sharing of information goes both ways.
edge(X,Y) :- edge(Y,X).

% Now we break each formula down into all of its subformulas. These subformulas are used later in the code
% to check whether an interpretation entails all of the nodes' original beliefs. After truth values are assigned
% to an node's atoms, that node's initial beliefs are "built back up" from these subformulas, to find whether
% a particular valuation satisfies those beliefs.
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

% We generate a set of equivalences linking together atoms in nodes that are directly connected.
{ eq(P,X,Y) : atom(P), edge(X,Y), X < Y }.

% Can we find an assignment of truth values (restricted by our set of equivalences) such that all the original formulas are satisfied?
% We want to see if truth values can be assigned to the atoms such that all the original formulas hold.
1 { tv(N,P,1) ; tv(N,P,0) } 1 :- atom(P), node(N).

%:- tv(N,true,0), node(N).

% Atoms that are "linked" by an equivalence must have the same truth value in both nodes.

%:- eq(P,X,Y), truth_value(P,X,V), truth_value(P,Y,W), V != W.
% The addition of edge(X,Y) below ensures that no unnecessary constraints are created 
% when we run the program together with transitive.lp. Without edge(X,Y), we get tons 
% more constraints that don't really matter (I think).
:- eq(P,X,Y), edge(X,Y), tv(X,P,V), tv(Y,P,W), V != W.


% Now we build up the original formulas for each node using the truth values assigned to each atom, to see
% if the original formulas are satisfied under this valuation.

%satisfied(P,X) :- truth_value(P,X,true).
satisfied(N,P) :- tv(N,P,1), atom(N,P).
% POSSIBLY satisfied(P,X) :- truth_value(P,X,true), atom(P,X). just to eliminate some unnecessary ground lines
satisfied(N,F) :- F = and(A,B), satisfied(N,A), satisfied(N,B), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = or(A,B),  satisfied(N,A), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = or(A,B),  satisfied(N,B), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = implies(A,B),  not satisfied(N,A), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = implies(A,B),      satisfied(N,B), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = iff(A,B),          satisfied(N,A), satisfied(N,B), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = iff(A,B),      not satisfied(N,A), not satisfied(N,B), subformula(N,F), subformula(N,A), subformula(N,B).
satisfied(N,F) :- F = neg(A),        not satisfied(N,A), subformula(N,F), subformula(N,A).

% All original formulas must be satisfied in order for the EQ set to be valid.
:- formula(N,F), not satisfied(N,F).

% This heuristic is used to find maximal sets of equivalences, with respect to set containment.
_heuristic(eq(P,X,Y), true, 1) :- atom(P), edge(X,Y), X < Y.

#show _heuristic/3.
#show eq/3.
#show tv/3.
