<img src="https://github.com/navindu-ds/elpee/assets/114894532/81c9a74a-435d-4dd7-bef4-e9d88708cffb">

# Elpee

<p align="left">
     <img src="https://badgen.net/pypi/v/elpee" />
     <a href="LICENSE.md"><img src="https://badgen.net/static/license/Apache-2.0/blue" /></a>
<!--      <img src="https://badgen.net/github/releases/navindu-ds/elpee"/> -->
     <img src="https://badgen.net/github/prs/navindu-ds/elpee" />
     <img src="https://badgen.net/github/last-commit/navindu-ds/elpee" />
<!--      <img src="https://badgen.net/github/stars/navindu-ds/elpee"/> -->
     
</p>

*Solving linear programming problems one step at a time.*

Elpee (short for **L** inear **P** rogramming) is a Python library for students and academics to viusalize the steps and iterations required to solve constrained linear optimization problems using linear programming methods.

## Documentation

Follow the documentation to get the best use of [elpee](https://elpee.readthedocs.io/).

## Install
To use elpee Python library, install it using [pip](https://pypi.org/project/elpee/):
```
(.venv) $ pip install elpee
```

## Example Problem
Define the Linear Programming Problem to be solved using the All Stack Starting Method by defining the Objective Function and the Constraint Expressions.
```
from elpee import LinearProblem

# set up a maximization problem
problem = LinearProblem(is_maximization=True)

# define the objective function
problem.add_objective('x + y')

# add the constraints to the problem
problem.add_constraint('-x + y <= 2')
problem.add_constraint('6*x + 4*y >= 24')
problem.add_constraint('y >= 1')
```

Add additional configurations to apply Big-M or Dual Simplex Method
```
problem.use_dual_simplex() # use to configure problem to use dual simplex method
problem.use_bigM() # use to configure problem to use big M method
```

Apply the Solver to solve the Linear Problem. The iterations to produce the results will be printed on the command line.
```
from elpee import ElpeeSolver

solution = ElpeeSolver.solve(problem)
```
Sample Output will be as follows (using dual_simplex).
```
...Generating Initial Feasible Solution for
     MIN           x            y            S1           S2           S3          Sol
      P           -1.0         -1.0          0            0            0            0
      S1          -1.0         1.0           1            0            0           2.0
      S2          -6.0         -4.0          0            1            0          -24.0
      S3           0           -1.0          0            0            1           -1.0
===========================================================================================

Taking S2 = 0; Entering x as a new basic variable;

...Generating Initial Feasible Solution for
     MIN           x            y            S1           S2           S3          Sol
      P           0.0         -0.333        0.0         -0.167        0.0          4.0
      S1          0.0         1.667         1.0         -0.167        0.0          6.0
      x           1.0         0.667         -0.0        -0.167        -0.0         4.0
      S3           0           -1.0          0            0            1           -1.0
===========================================================================================

Taking S3 = 0; Entering y as a new basic variable;

Feasible Solution # 1
     MIN           x            y            S1           S2           S3          Sol
      P           0.0          0.0          0.0         -0.167       -0.333       4.333
      S1          0.0          0.0          1.0         -0.167       1.667        4.333
      x           1.0          0.0          0.0         -0.167       0.667        3.333
      y           -0.0         1.0          -0.0         -0.0         -1.0         1.0
===========================================================================================

Optimized Solution Received!
```
And obtain an interpretation to the solution
```
Minimum Value for Objective Function = 4.333

Values for Decision Variables :
      x       = 3.333
      y       = 1.0

Surplus & Slack variables
  Constraint #1 Surplus    = 4.333 units
  Constraint #2 Surplus    : Satisfied at Boundary
  Constraint #3 Surplus    : Satisfied at Boundary
```
