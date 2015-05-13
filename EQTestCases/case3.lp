% Agents are identified by integers starting at 1.
node(1..4).

% As a user requirement, the set of atoms used in each agent's initial beliefs must be explicitly stated.
atom(p, 1).
atom(p, 2).

% The initial beliefs of each agent:
formula(p, 1).
formula(neg(p), 2).
formula(q,2).

% Agents that are connected by an edge can communicate directly to incorporate beliefs from one another.
edge(1,2 ; 1,3 ; 2,4 ; 3,4).
