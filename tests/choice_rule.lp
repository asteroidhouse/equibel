#script (python)

import gringo

def on_model(m):
    #m.optimization()
    #s = str(m)
    print(m)


def main(prg):
    prg.conf.solve.models = 0
    
    prg.ground([('base', [])])
    prg.solve(on_model=on_model)
    #prg.solve()

#end.

{ a; b; c; d; e; f; g; h; i; j; k; l; m; n; o; p; q; r; s; t; u; v; w; x; y; z } == 10.

%*
thing(1..30).

{ selected(X) : thing(X) } == 8.

#show selected/1.
*%
