% Author:  Paul Vicol
% Email:   pvicol@sfu.ca
% 
% Purpose: This program translates formulas from one node's language to another node's language, given a set of 
%          equivalences that link the atoms used by these nodes.
%          In converting formulas from one language to another, atoms that are in the EQ set are 
%          simply given new subscripts (to indicate that they are being used in a formula believed by the
%          receiving node), while atoms that are not in the EQ set are negated and also given new subscripts.
%          In this way, while the formulas are translated, they are modified to ensure that they are consistent
%          with the formulas already believed by the receiving node.


translate(R,P,X,Y) :- atom(P), R = P,          eq(P,X,Y).
translate(R,P,X,Y) :- atom(P), R = neg(P), not eq(P,X,Y), node(X;Y), X != Y.

translate(R,F,X,Y) :- F = neg(A), R = neg(C), translate(C,A,X,Y), subformula(F,X), subformula(A,X),
                      node(X;Y), X != Y.
translate(R,F,X,Y) :- F = and(A,B), R = and(C,D), translate(C,A,X,Y), translate(D,B,X,Y), subformula(F,X), subformula(A,X), 
                      subformula(B,X), node(X;Y), X != Y.
translate(R,F,X,Y) :- F = or(A,B), R = or(C,D),  translate(C,A,X,Y), translate(D,B,X,Y), subformula(F,X), subformula(A,X),
                      subformula(B,X), node(X;Y), X != Y.
translate(R,F,X,Y) :- F = implies(A,B), R = implies(C,D), translate(C,A,X,Y), translate(D,B,X,Y), subformula(F,X), 
                      subformula(A,X), subformula(B,X), node(X;Y), X != Y.
translate(R,F,X,Y) :- F = iff(A,B), R = iff(C,D), translate(C,A,X,Y), translate(D,B,X,Y), subformula(F,X), 
                      subformula(A,X), subformula(B,X), node(X;Y), X != Y.


%new_formula(R,X,Y) :- formula(F,X), translate(R,F,X,Y), not subformula(R,Y), eq(_,X,Y), node(X,Y), X != Y.
%new_formula(R,X,Y) :- formula(F,X), translate(R,F,X,Y), eq(_,X,Y), node(X;Y), X != Y.
new_formula(R,X,Y) :- formula(F,X), translate(R,F,X,Y), edge(X,Y), node(X;Y), X != Y.
%new_formula(R,X,Y) :- formula(F,X), translate(R,F,X,Y), eq(P,X,Y), subformula(P,X), node(X;Y), X != Y.

new_formula(Y,F)   :- new_formula(F,_,Y).

#show new_formula/2.
