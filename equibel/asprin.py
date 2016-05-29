"""This file provides a programmatic interface to the ``asprin`` preference handling 
framework - this allows asprin to be invoked from Python, and allows preferred answer 
to be returned directly in Python.
The currently distributed version of ``asprin`` is designed as a stand-alone system, 
so using it as-is would involve parsing its command-line output.
"""

# Original Author: Javier Romero
# Modified by: Paul Vicol

import sys
import subprocess
import platform
import pkg_resources
import tempfile

if platform.system() == 'Linux':
    if platform.architecture()[0] == '64bit':
        from equibel.includes.linux_64.gringo import *
        asprin_parser = pkg_resources.resource_filename('equibel', 'includes/linux_64/asprin.parser')
    #elif platform.architecture()[0] == '32bit':
    #    from equibel.includes.linux_32.gringo import *
    #    asprin_parser = pkg_resources.resource_filename('equibel', 'includes/linux_32/asprin.parser')
elif platform.system() == 'Darwin':
    from equibel.includes.mac.gringo import *
    asprin_parser = pkg_resources.resource_filename('equibel', 'includes/mac/asprin.parser')


aspypart = pkg_resources.resource_filename('equibel', 'asp/aspypart.lp')
asprin_lib = pkg_resources.resource_filename('equibel', 'asp/asprin.lib')


current_module = sys.modules[__name__]


holds, nholds, shown, base = [], [], [], []
enum, nmodels, answers, maxmodels = 0, 0, 1, 1


optimal_models = []


def get(val, default):
    return val if val is not None else default

def getHolds():
    global holds
    return holds

def getNHolds():
    global nholds
    return nholds

def printShown():
    global enum, answers, shown, nmodels, noprint
    #print "Answer: " + str(answers)
    answers = answers + 1
    enum = enum + 1
    #print("Answer: " + str(enum))
    #if noprint == 0:
    #    print('%s' % ' '.join(map(str,shown)))

def printShownOpt():
    global nmodels, noprint
    if noprint == -1:
        noprint = 0
        printShown()
        noprint = -1
    else:
        printShown()
    #print("OPTIMUM FOUND *")
    nmodels = nmodels + 1

def cat(*args):
    return ''.join(str(x) for x in args)

def handleError(m):
    global error
    error = 1
    for t in m:
        if t.name() == "_error" and len(t.args()) == 1:
            print(str(t.args()[0]))


def onModel(model):
    global holds, nholds, shown, maxmodels, step, nosyntax, mode
    # syntax errors
    if step == 1 and nosyntax == 0 and (Fun("_error",[]) in model.atoms(Model.TERMS)):
        handleError(model.atoms(Model.TERMS))
        return
    # shown atoms
    holds, shown = [], []
    for a in model.atoms(Model.SHOWN):
        if (a.name() == "_holds_at_zero"):
            holds.append(a.args()[0])
        elif (a.name()[0] != "_"):
            shown.append(a)
    # false _holds_at_zero terms
    if maxmodels != 1 or mode == 1:
        nholds = []
        for a in model.atoms(Model.TERMS | Model.COMP):
            if (a.name() == "_holds_at_zero"):
                nholds.append(a.args()[0])


def onModelMany(model):
    global shown, found, base
    global optimal_models
    shown = []
    for a in model.atoms(Model.SHOWN):
        if (a.name()[0] != "_"):
            shown.append(a)
    if found == 0 and len(shown) == len(base): # do not repeat model!
        for a in base:
            if a not in shown:
                #printShownOpt()
                optimal_models.append(shown)
                return
        found = 1
    else:
        #printShownOpt()
        optimal_models.append(shown)


def doEnumerate(prg, step, maxmodels):
    global base, shown, nmodels, found, holds, nholds, mode
    if (maxmodels == 0):
        prg.conf.solve.models = 0
    else:
        prg.conf.solve.models = maxmodels - nmodels + 1
    found = 0
    base = shown
    assumptions = [(Fun("_holds",[x,0]),True)  for x in holds] + [(Fun("_holds",[x,0]),False) for x in nholds]
    if mode == 1:
        assumptions += [(Fun("_holds",[x,1]),False) for x in holds] + [(Fun("_holds",[x,1]),False) for x in nholds]
    prg.solve(assumptions, on_model = onModelMany)
    prg.conf.solve.models = 1


def compute_optimal_models(input_files, program_parts_to_add=None):

    global found, shown, base, nosyntax, step, error, mode
    global enum, nmodels, answers, maxmodels, project, noprint
    global optimal_models

    holds, nholds, shown, base = [], [], [], []
    #, nmodels, answers, maxmodels = 0, 0, 1, 1
    optimal_models = []

    step = 1
    unsat = 0
    startone = 1
    opt = []
    error = 0

    prg = Control()
    # NEW
    prg.conf.configuration = 'crafty'
    prg.conf.solver.heuristic = 'domain'

    compiled_asp_code = subprocess.check_output([asprin_parser, asprin_lib] + input_files)

    #print(compiled_asp_code)

    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file.write(compiled_asp_code)
        temp_file.flush()
        prg.load(temp_file.name)

    prg.load(aspypart)

    if program_parts_to_add:
        for program_part in program_parts_to_add:
            prg.add(*program_part)

    #print("ASPRIN STARTED...")

    # options
    maxmodels   = get(prg.get_const("_asprin_n"), 1)
    project     = get(prg.get_const("_asprin_project"), 0)
    releaselast = get(prg.get_const("_asprin_release_last"), 0)
    forgetopt   = get(prg.get_const("_asprin_no_opt_improving"), 0)
    dovolatile  = get(prg.get_const("_asprin_do_external"), 0)
    nosyntax    = get(prg.get_const("_asprin_no_syntax_check"), 0)
    nobf        = get(prg.get_const("_asprin_no_boolean_formula"), 0)
    tr          = get(prg.get_const("_asprin_tr"), "")
    steps       = get(prg.get_const("_asprin_steps"), 0)
    noprint     = get(prg.get_const("_asprin_no_print"), 0)
    heuristic   = get(prg.get_const("_asprin_heuristic"), 0)
    mode        = get(prg.get_const("_asprin_mode"), 0)

    # ground base
    if nobf != 0:
        prg.ground([("base",[])], current_module)
    else:
        prg.ground([("base",[]), ("_bf",[])], current_module)

    # heuristic
    if (heuristic != 0):
        prg.add("_show_heuristic", [], "#show _heuristic/3. #show _holds/2.")
        prg.ground([("_heuristic",[]), ("_show_heuristic",[])], current_module)

    # syntax
    if nosyntax == 0:
        prg.ground([("_syntax_check",[])], current_module)
        prg.assign_external(Fun("_check",[]), True)

    # main loop
    while True:

        # add rules to improve on previous model
        if (step > startone) and (mode == 0):
            if (releaselast != 0) and (step - startone > 1):
                prg.release_external(Fun("_volatile", [0,step-2]))
            # ground to improve (with volatile or fact)
            if ((maxmodels != 1) or (releaselast != 0) or (dovolatile != 0)):
                prg.ground([("_doholds",[step-1]), ("_preference",[0,step-1]), ("_constraints",[0,step-1]), ("_volatile_external",[0,step-1])], current_module)
                prg.assign_external(Fun("_volatile", [0,step-1]), True)
            else:
                prg.ground([("_doholds",[step-1]), ("_preference",[0,step-1]), ("_constraints",[0,step-1]), ("_volatile_fact",[0,step-1])], current_module)

        # ground once mode
        if mode == 1:
            if step == 2:
                if maxmodels != 1:
                    prg.ground([("_openholds",[step-1]), ("_preference",[0,step-1]), ("_constraints",[0,step-1]), ("_volatile_external",[0,step-1])], current_module)
                else:
                    prg.ground([("_openholds",[step-1]), ("_preference",[0,step-1]), ("_constraints",[0,step-1]), ("_volatile_fact",[0,step-1])], current_module)
            if maxmodels != 1 and step == (startone + 1):
                prg.assign_external(Fun("_volatile",[0,1]), True)

        # solve
        if mode == 1 and step > startone:
            ret = prg.solve([(Fun("_holds",[x,1]),True) for x in holds] + [(Fun("_holds",[x,1]),False) for x in nholds], on_model=onModel)
        else:
            ret = prg.solve(on_model=onModel)

        # syntax
        if error == 1:
            break
        if step == 1 and nosyntax == 0:
            prg.release_external(Fun("_check",[]))

        # set translation of extended rules
        if (step == 2) and (tr is not ""):
            prg.conf.asp.trans_ext = tr

        # if UNSAT
        if ret == SolveResult.UNSAT:

            # stop if program is unsat (step==1), last call was unsat (unsat==1) or we already computed maxmodels
            if (step==1):
                print "UNSATISFIABLE"
                break
            if (unsat==1):
                break
            #if noprint==999: print "\nAnswer: " + str(enum) + "\n" +
            if noprint==-1:
                #print('%s' % ' '.join(map(str,shown)))
                optimal_models.append(shown)
            nmodels += 1
            if (maxmodels == nmodels):
                break

            # relax conditions on previous models
            if mode == 0:
                prg.release_external(Fun("_volatile",[0,step-1]))
                if (releaselast == 0):
                    for i in range(startone,step-1):
                        prg.release_external(Fun("_volatile",[0,i]))
            elif mode == 1:
                prg.assign_external(Fun("_volatile",[0,1]), False)

            # if no projection, enumerate many
            if (project == 0):
                doEnumerate(prg,step,maxmodels)
            if (maxmodels == nmodels):
                break

            # add rules to be different and not worse than optimal models
            if mode == 1 and step == 2:
                step = 0 # hack to avoid redefining _holds(X,1)
            if mode == 1:
                prg.ground([("_doholds",[step-1])], current_module)
            if forgetopt != 0:
                prg.ground([("_deletemodel",[]),("_preference", [step-1,0]),("_unsat_constraints", [step-1,0]),("_volatile_external",[step-1,0])], current_module)
                prg.assign_external(Fun("_volatile",[step-1,0]), True)
                for i in opt:
                    prg.assign_external(Fun("_volatile",[i,0]), True)
                opt.append(step-1)
            else:
                prg.ground([("_deletemodel",[]),("_preference", [step-1,0]),("_unsat_constraints", [step-1,0]),("_volatile_fact",[step-1,0])], current_module)
            if mode == 1 and step == 0:
                step = 2

            startone = step + 1
            unsat = 1

        #if SAT
        else:
            printShown()
            if (unsat==1 and forgetopt != 0):
                for i in opt:
                    prg.assign_external(Fun("_volatile",[i,0]), False)
            unsat = 0

        if steps == step:
            break
        step = step+1

    #print("ASPRIN ENDED...")

    return optimal_models



if __name__ == '__main__':
    models = compute_optimal_models(['./equibel/asp/eq_base.lp', './equibel/asp/preference.lp', './equibel/asp/test_chain.lp'])
    print(models)
