# Equibel

## Introduction

*Note: This project is still under construction. More documentation will be available soon.*

Equibel is a toolkit for working with equivalence-based belief change.
It can be used in two ways:

1. Programmatically, via the **equibel** Python module, or
2. Interactively, via the **equibeli** command-line interface

## Currently Supported Platforms

* OS X with Python 2.x

## Installation

It is recommended that you install Equibel into a *virtual environment*.


1. Create a project directory and a virtual environment:

```
mkdir equibel_projects
cd equibel_projects
virtualenv venv --python=python2.7
```

2. Activate the virtual environment:

```
source venv/bin/activate
```

3. Get the source code by cloning this repository:

```
git clone git://github.com/asteroidhouse/equibel.git
```

4. Enter the equibel directory and run pip:

```
cd equibel
pip install .
```
