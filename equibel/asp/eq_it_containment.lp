_heuristic(eq(N,P,N,M), true, 1) :- atom(N,P), edge(M,N).
_heuristic(eq(N,P,N,M), true, 1) :- atom(M,P), edge(M,N).

#show _heuristic/3.
#show eq/4.
#show tv/4.
