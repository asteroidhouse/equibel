![Equibel](equibel_logo.png)

# Equibel


`Equibel` is a Python package for working with consistency-based belief change in a 
graph-oriented setting. 


## Currently Supported Platforms

* OS X with Python 2.7.x
* 64-bit Linux with Python 2.7.x

Note that while Equibel is distributed as a Python package, the core of the system is 
implemented using Answer Set Programming (ASP), and relies on an underlying ASP solver 
called `clingo`, which is part of the 
[Potsdam Answer Set Solving Collection (Potassco)](http://potassco.sourceforge.net). 

In particular, Equibel has two ASP-related dependencies: 
the [Python `gringo` module](http://potassco.sourceforge.net/gringo.html), which provides an 
interface to an ASP solver from within Python, and `asprin.parser`, which is a component of 
the `asprin` preference-handling framework. `asprin` is described in more detail 
[here](http://www.cs.uni-potsdam.de/asprin/), and can be download from 
[here](https://sourceforge.net/projects/potassco/files/asprin/).

The *Python* component of Equibel is highly portable across platforms; however, the `gringo`
and `asprin.parser` dependencies must be compiled for specific system configurations, producing 
system-specific binaries.
In order to simplify usage for some _common_ system configurations, Equibel includes pre-compiled 
binaries of these dependencies for 64-bit Linux distributions and Mac OS. These are placed in 
the `equibel/includes/` directory, which is structured as follows:

```
equibel/includes/
├── __init__.py
├── linux_64
│   ├── asprin.parser
│   ├── gringo.so
│   └── __init__.py
└── mac
    ├── asprin.parser
    ├── gringo.so
    └── __init__.py
```

*If Equibel does not function correctly once it is installed, this is likely due to the fact that 
the pre-compiled binaries are not compatible with your system.* In this case, you must compile 
the dependencies manually, by downloading the required components directly from 
[Potassco](http://potassco.sourceforge.net), and overwriting the resulting binaries in the folder 
that corresponds to your operating system.


## Installation

The following steps assume that you have the `pip` Python package manager 
installed. If you don't have `pip`, you can get it [here](https://pip.pypa.io/en/latest/installing.html).

1. Clone this repository (to create a local copy):
    
    ```
    $ git clone https://github.com/asteroidhouse/equibel.git
    ```

    This will create a folder called `equibel` in your current working directory.

2. Change directories to the `equibel` folder:
    
    ```
    $ cd equibel
    ```


3. Install Equibel using `pip` from within `equibel` as follows:

    ```
    $ sudo pip install .
    ```

4. Optionally, you can test whether everything works on your system by installing the `nose` 
   testing tool and running the tests in the _tests_ folder, as follows:
    
    ```
    $ sudo pip install nose
    ```
    
    ```
    $ nosetests tests/
    ```

    If all of the dependencies have installed correctly, the last command should print a series 
    of dots to the screen, one for each successfully completed test case.
   
    If the tests fail, it is most likely due to the *dependencies* of Equibel not being compatible 
    with your platform. As noted above, Equibel includes pre-compiled binaries of the Python `gringo` 
    module, as well as of `asprin.parser`, for 64-bit Linux distributions (tested on Ubuntu 14.04) and 
    for Mac OS (tested on OSX 10.10). If you are not using one of these systems, you will need to 
    manually compile the `gringo` and `asprin.parser` dependencies.

## Quickstart

To use Equibel within a Python program, you need to import the `equibel`
module. The following Python script creates a path graph, assigns formulas 
to nodes, find the global completion, and prints the resulting formulas at 
each node:

```python
import equibel as eb

if __name__ == '__main__':
    # Create an EquibelGraph object, which represents a graph and 
    # associated scenario.
    G = eb.EquibelGraph()

    # Create nodes:
    G.add_nodes_from([1, 2, 3, 4])

    # Create edges:
    G.add_edges_from([(1,2), (1,3), (3,4), (2,4)]) 

    # Add formulas to nodes:
    G.add_formula(1, "p & q & r")
    G.add_formula(4, "~p & ~q")

    # Find the global completion of the G-scenario:
    R = eb.global_completion(G)

    # Print the resulting formulas at each node:
    for node_id in R.nodes():
        print("Node {0}: {1}".format(node_id, R.formula_conj(node_id)))
```
