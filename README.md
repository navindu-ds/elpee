# Elpee

A linear programming library with step by step implementation. 

Define the Linear Programming Problem to be solved using the All Stack Starting Method by defining the Objective Function and the Constraint Expressions.
```
from elpee import LinearProblem
from elpee.algorithms import AllStackStarter

# set up a maximization problem
prob = LinearProblem(is_maximization=True)

# define the objective function
prob.add_objective('x + y')

# add the constraints to the problem
prob.add_constraint('-x + y <= 2')
prob.add_constraint('-6*x -4*y <= 24')
prob.add_constraint('-y <= -1')
```

Add additional configurations to apply Big-M or Dual Simplex Method
```
prob.use_dual_simplex() # use to configure problem to use dual simplex method
prob.use_bigM() # use to configure problem to use big M method
```

Apply the All Stack Method Solver to solve the Linear Problem. The iterations to produce the results will be printed on the command line.
```
solver = AllStackStarter(prob)
solution = solver.solver()
```
Sample Output will be as follows.
```
...Generating Initial Feasible Solution for
     MIN           x            y            S1           S2           S3           A1          Sol
      P           -1.0         -1.0          0            0            0            -M           0
      S1          -1.0         1.0           1            0            0            0           2.0
      S2          -6.0         -4.0          0            1            0            0           24.0
      A1           0           1.0           0            0            -1           1           1.0

Feasible Solution # 1
     MIN           x            y            S1           S2           S3           A1          Sol
      P           -1.0     1.0*M - 1.0       0            0            -M           0          1.0*M
      S1          -1.0         1.0           1            0            0            0           2.0
      S2          -6.0         -4.0          0            1            0            0           24.0
      A1           0           1.0           0            0            -1           1           1.0

Taking A1 = 0; Entering y as a new basic variable;

Feasible Solution # 2
     MIN           x            y            S1           S2           S3           A1          Sol
      P           -1.0          0            0            0           -1.0     1.0 - 1.0*M      1.0
      S1          -1.0         0.0          1.0          0.0          1.0          -1.0         1.0
      S2          -6.0         0.0          0.0          1.0          -4.0         4.0          28.0
      y            0           1.0           0            0            -1           1           1.0

Optimized Solution Received!
```
Each iteration can be individually run using `do_step=True` parameter
```
solver = AllStackStarter(prob)
iteration1 = solver.solver(do_step=True)
```