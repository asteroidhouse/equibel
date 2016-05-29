#program base.
#show _holds_at_zero(X) : _holds(X,0).

#program _doholds(m).
_holds(X,m) :- X = @getHolds().

#program _openholds(m).
{ _holds(X,m) } :- X = @getHolds().
{ _holds(X,m) } :- X = @getNHolds().

#program _volatile_fact(_m1,_m2).
_volatile(_m1,_m2).

#program _volatile_external(_m1,_m2).
#external _volatile(_m1,_m2).

#program _deletemodel.
:- _holds(X,0) : X = @getHolds();
   not _holds(X,0) : X = @getNHolds().

#program _syntax_check.

#external _check : not _nocheck.

_error(M) :- M = @cat("ERROR (asprin): Two different optimize statements: ",X1," and ",X2,"."),
  __optimize(X1), __optimize(X2), X1 < X2,
  _check.

_error(M) :- M = @cat("ERROR (asprin): Two preference statements with same id (",Id,"), and different type (",T1," and ",T2,")."),
  __preference(Id,T1), __preference(Id,T2), T1 < T2,
  _check.

_error(M) :- M = @cat("ERROR (asprin): Optimize statement for ",X," has no corresponding preference statement."),
  __optimize(X), not __preference(X,_),
  _check.

_error(M) :- M = @cat("ERROR (asprin): name(",X,") atom in preference statement ",P," has no corresponding preference statement."),
  __preference(P,_,_,name(X),_), not __preference(X,_),
  _check.

_link(P1,P2) :- __preference(P2,_,_,name(P1),_), _check.
_link(P1,P2) :- _link(P1,P3), _link(P3,P2), _check.
_error(M) :- M = @cat("ERROR (asprin): Cycle between name atoms with statement ",P,"."),
  _link(P,P),
  _check.

#show _error    : _error(X), _check.
#show _error(X) : _error(X), _check.

#program _bf.

_formula(F) :- __preference(_,_,_,for(F),_), not _nobf.
_formula(F) :- _formula(_not(F)),   not _nobf.

_formula(F) :- _formula(_and(F,G)), not _nobf.  _formula(G) :- _formula(_and(F,G)), not _nobf.
_formula(F) :- _formula(_or(F,G)),  not _nobf.  _formula(G) :- _formula(_or(F,G)),  not _nobf.

_complex(_not(F))   :- _formula(_not(F)),   not _nobf.
_complex(_and(F,G)) :- _formula(_and(F,G)), not _nobf.
_complex(_or(F,G))  :- _formula(_or(F,G)),  not _nobf.

_sat(_not(F))   :- _formula(_not(F)), not _sat(F),            not _nobf.
_sat(_and(F,G)) :- _formula(_and(F,G)), _sat(F), _sat(G),     not _nobf.
_sat(_or(F,G))  :- _formula(_or(F,G)), 1 { _sat(F); _sat(G)}, not _nobf.

_holds(F,0) :- _sat(F), __preference(_,_,_,for(F),_), _complex(F), not _nobf.

#program _heuristic.
#const _asprin_heuristic_value=1.
_heuristic(_holds(X,0),_asprin_heuristic_mode,_asprin_heuristic_value) :- __preference(P,_,_,for(X),_).

#program _nowarnings.
_nobf :- _nobf.
_check :- _check. _nocheck :- _nocheck.
__preference(A,B,C,D,E) :- __preference(A,B,C,D,E).
__preference(A,B) :- __preference(A,B).
__optimize(X) :- __optimize(X).
__better(X,Y,Z) :- __better(X,Y,Z).
