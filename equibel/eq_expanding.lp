#const d.

% Now we break each formula down into all of its subformulas. These subformulas are used later in the code
% to check whether an interpretation entails all of the nodes' original beliefs. After truth values are assigned
% to an node's atoms, that node's initial beliefs are "built back up" from these subformulas, to find whether
% a particular valuation satisfies those beliefs.
subformula(F,X) :- formula(F,X).
subformula(A,X) :- subformula(and(A,_), X).
subformula(A,X) :- subformula(and(_,A), X).
subformula(A,X) :- subformula(or(A,_), X).
subformula(A,X) :- subformula(or(_,A), X).
subformula(A,X) :- subformula(implies(A,_), X).
subformula(A,X) :- subformula(implies(_,A), X).
subformula(A,X) :- subformula(iff(A,_), X).
subformula(A,X) :- subformula(iff(_,A), X).
subformula(A,X) :- subformula(neg(A), X).

compound_prop(F,X) :- F = and(A,B), subformula(F,X), subformula(A,X), subformula(B,X).
compound_prop(F,X) :- F = or(A,B), subformula(F,X), subformula(A,X), subformula(B,X).
compound_prop(F,X) :- F = implies(A,B), subformula(F,X), subformula(A,X), subformula(B,X).
compound_prop(F,X) :- F = iff(A,B),	subformula(F,X), subformula(A,X), subformula(B,X).
compound_prop(F,X) :- F = neg(A), subformula(F,X), subformula(A,X), subformula(B,X).

atom(P,X) :- subformula(P,X), not compound_prop(P,X).
atom(P)   :- atom(P,_).


% We generate a set of equivalences linking together atoms in nodes that are directly connected.
% { eq(P,X,Y) : atom(P) , edge(X,Y) }.
{ eq(P,X,Y) : atom(P) , dist(X,Y,d) }.

% Can we find an assignment of truth values (restricted by our set of equivalences) such that all the original formulas are satisfied?
% We want to see if truth values can be assigned to the atoms such that all the original formulas hold.
1 { truth_value(P,X,true) ; truth_value(P,X,false) } 1 :- atom(P), node(X).

% Atoms that are "linked" by an equivalence must have the same truth value in both nodes.
:- eq(P,X,Y), truth_value(P,X,V), truth_value(P,Y,W), V != W.


% Now we build up the original formulas for each node using the truth values assigned to each atom, to see
% if the original formulas are satisfied under this valuation.
satisfied(P,X) :- truth_value(P,X,true).
satisfied(F,X) :- F = and(A,B), satisfied(A,X), satisfied(B,X), subformula(F,X), subformula(A,X), subformula(B,X).
satisfied(F,X) :- F = or(A,B),  satisfied(A,X), subformula(F,X), subformula(A,X), subformula(B,X).
satisfied(F,X) :- F = or(A,B),  satisfied(B,X), subformula(F,X), subformula(A,X), subformula(B,X).
satisfied(F,X) :- F = implies(A,B),  not satisfied(A,X), subformula(F,X), subformula(A,X), subformula(B,X).
satisfied(F,X) :- F = implies(A,B),      satisfied(A,X), satisfied(B,X), subformula(F,X), subformula(A,X), subformula(B,X).
satisfied(F,X) :- F = iff(A,B),          satisfied(A,X), satisfied(B,X), subformula(F,X), subformula(A,X), subformula(B,X).
satisfied(F,X) :- F = iff(A,B),      not satisfied(A,X), not satisfied(B,X), subformula(F,X), subformula(A,X), subformula(B,X).
satisfied(F,X) :- F = neg(A),        not satisfied(A,X), subformula(F,X), subformula(A,X).

% All original formulas must be satisfied in order for the EQ set to be valid.
:- formula(F,X), not satisfied(F,X).

% #maximize { 1,P,X,Y:eq(P,X,Y),atom(P),edge(X,Y) }.
#maximize { 1,P,X,Y:eq(P,X,Y),atom(P),dist(X,Y,d) }.

% This heuristic is used to find maximal sets of equivalences, with respect to set containment.
% _heuristic(eq(P,X,Y), true, 1) :- atom(P), edge(X,Y), X < Y.
% _heuristic(eq(P,X,Y), true, 1) :- atom(P), edge(X,Y).
_heuristic(eq(P,X,Y), true, 1) :- atom(P), dist(X,Y,d).

#show _heuristic/3.
#show eq/3.
