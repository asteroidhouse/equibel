% #const center=1.

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
atom(P) :- atom(_,P).


star_node(center, center).
star_node(center, Node) :- edge(Node, center).

% star_atom(center, Atom) :- atom(center, Atom).
% NO LONGER USING STAR ATOMS
%star_atom(center, Atom) :- star_node(center, Node), atom(Node, Atom).


%{ tv(center, Node, Atom, 0) ; tv(center, Node, Atom, 1) } == 1 :- star_node(center, Node), star_atom(center, Atom).
% SWITCHED FROM STAR ATOMS TO JUST ATOMS
{ tv(center, Node, Atom, 0) ; tv(center, Node, Atom, 1) } == 1 :- star_node(center, Node), atom(Atom).

% Here, the order of the nodes matters: the center of the star graph must come first.
%{ eq(center, Node, Atom) : star_node(center, Node), star_atom(center, Atom), Node != center }.
% SWITCHED FROM STAR ATOMS TO JUST ATOMS
{ eq(center, Node, Atom) : star_node(center, Node), atom(Atom), Node != center }.

:- eq(center, Node, Atom), tv(center, Node, Atom, V), tv(center, center, Atom, W), Node != center, V != W.

sat(center,Node,Atom) :- tv(center,Node,Atom,1).
sat(center,Node,F) :- F = and(A,B), sat(center,Node,A), sat(center,Node,B), subformula(Node,F), subformula(Node,A), subformula(Node,B).
sat(center,Node,F) :- F = or(A,B),  sat(center,Node,A), subformula(Node,F), subformula(Node,A), subformula(Node,B).
sat(center,Node,F) :- F = or(A,B),  sat(center,Node,B), subformula(Node,F), subformula(Node,A), subformula(Node,B).
sat(center,Node,F) :- F = implies(A,B),  not sat(center,Node,A), node(center), subformula(Node,F), subformula(Node,A), subformula(Node,B).
sat(center,Node,F) :- F = implies(A,B),      sat(center,Node,B), subformula(Node,F), subformula(Node,A), subformula(Node,B).
sat(center,Node,F) :- F = iff(A,B),          sat(center,Node,A), sat(center,Node,B), subformula(Node,F), subformula(Node,A), subformula(Node,B).
sat(center,Node,F) :- F = iff(A,B),      not sat(center,Node,A), not sat(center,Node,B), node(center), subformula(Node,F), subformula(Node,A), subformula(Node,B).
sat(center,Node,F) :- F = neg(A),        not sat(center,Node,A), node(center), subformula(Node,F), subformula(Node,A).

%:- formula(X,F), node(N), not satisfied(N,X,F).

% Is this symmetry required?
eq(Node, center, Atom) :- eq(center, Node, Atom).


star_formula(center, Node, Formula) :- star_node(center, Node), formula(Node, Formula).

:- star_formula(center, Node, Formula), not sat(center, Node, Formula).

#show eq/3.
#show tv/4.
%#show star_node/2.
