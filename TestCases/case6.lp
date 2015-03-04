node(1..4).

formula(p, 1).
formula(and(neg(p), q), 2).
formula(and(q, neg(r)), 3).
formula(r, 4).
formula(or(p,q), 4).

edge(1,2 ; 1,3 ; 1,4 ; 2,3 ; 2,4 ; 3,4).
