% Agents are identified by integers starting at 1.
node(1..8).

% As a user requirement, the set of atoms used in each agent's initial beliefs must be explicitly stated.
atom(p, 1).
atom(p, 6).

% The initial beliefs of each agent:
formula(p, 1).
formula(neg(p), 6).

% Agents that are connected by an edge can communicate directly to incorporate beliefs from one another.
edge(1,2 ; 1,3 ; 2,3 ; 3,4 ; 4,5 ; 5,1 ; 1,6 ; 1,7 ; 6,7 ; 7,8 ; 6,8).
