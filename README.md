<img src="https://github.com/navindu-ds/elpee/assets/114894532/81c9a74a-435d-4dd7-bef4-e9d88708cffb">

# Elpee

A linear programming library with step by step implementation. 

Setup the environment using the following steps with [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).
```
# create new conda environment
conda create -n <env_name>
# select yes to allow installation

# activate conda environment
conda activate <env_name>

# install the requirements for the library
pip install -r requirements.txt
```

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
