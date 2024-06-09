Usage
=====

Solving LP problems with Steps 
------------------------------------------------

1. Set-up the Linear Programming (LP) problem to be solved according to maximization or minimization

.. code-block:: python

    from elpee import LinearProblem

    # set up a maximization problem
    problem = LinearProblem(is_maximization=True)

2. Define the Objective function for the LP problem to be optimized
    
.. code-block:: python

    # define the objective function
    problem.add_objective('x + y')

3. Define all constraints (either a `>=`, `<=` or `=` mathematical expression) for the LP problem to be optimized

.. code-block:: python

    # add the constraints to the problem
    problem.add_constraint('-x + y <= 2')
    problem.add_constraint('6*x + 4*y >= 24')
    problem.add_constraint('y >= 1')

4. [Optional] Add additional configurations to apply Big-M or Dual Simplex Method. The configuration will change the nature of the steps needed to solve problems with `>=` or `=` constraints.

For using dual simplex method

.. code-block:: python

    # use to configure problem to use dual simplex method
    problem.use_dual_simplex()

*Or* For using big-M method

.. code-block:: python

    # use to configure problem to use big M method
    problem.use_bigM()

5. Apply the Solver to solve the Linear Problem. The iterations to produce the results will be printed on the command line.

.. code-block:: python

    from elpee import ElpeeSolver

    solution = ElpeeSolver.solve(problem)

The output received will follow the format below

.. code-block:: console

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

    Minimum Value for Objective Function = 4.333

    Values for Decision Variables :
        x       = 3.333
        y       = 1.0

    Surplus & Slack variables
    Constraint #1 Surplus    = 4.333 units
    Constraint #2 Surplus    : Satisfied at Boundary
    Constraint #3 Surplus    : Satisfied at Boundary



Working with Alternate Optimal Solutions 
--------------------------------------------------

An alternate optimal solutions occur when the given problem has more than one solution. All such solutions reach the same optimum value with different combinations of decision variable values. 

Any optimized solution can be tested to check for the presence of alternate optimal solutions. 

First make sure to obtain an optimized solution (variable - `solution`) as shown in the above steps.

.. code-block:: console

    ## let the solution obtained for a LP problem be

    Feasible Solution # 1
       MAX           X1           X2           X3           X4           S1           S2          Sol     
        P            0            0            0            0            2            1           1827    
        X1           1            1            0            2            1            2            39     
        X3           0            1            1            3            0            4            48     
    ========================================================================================================

    Optimized Solution Received!
    There are 3 Alternate Solutions for this problem!

    Maximum Value for Objective Function = 1827

    Values for Decision Variables :
        X1      = 39
        X2      = 0
        X3      = 48
        X4      = 0

    Surplus & Slack variables
    Constraint #1 Surplus    : Satisfied at Boundary
    Constraint #2 Surplus    : Satisfied at Boundary

Find all alternate solutions for a LP problem
~~~~~~~~~~~

.. code-block:: python

    from elpee.algorithms import Alternator

    # visualize all alternate solutions  
    Alternator.display_all_alternate_solutions(solution)

And we can see the alternate solutions, and the changes required to obtain them too.

.. code-block:: console

    Displaying all Alternate Optimal Solutions for LP Problem provided...

    Alternate Solution #1
    Taking X1 = 0 for & setting X2 as a Basic Variable for the alternate solution

    Maximum Value for Objective Function = 1827

    Values for Decision Variables :
        X1      = 0
        X2      = 39
        X3      = 9
        X4      = 0

    Surplus & Slack variables
    Constraint #1 Surplus    : Satisfied at Boundary
    Constraint #2 Surplus    : Satisfied at Boundary
    ========================================================================================================

    Alternate Solution #2
    Taking X3 = 0 for & setting X4 as a Basic Variable for the alternate solution

    Maximum Value for Objective Function = 1827

    Values for Decision Variables :
        X1      = 7.0
        X2      = 0
        X3      = 0
        X4      = 16.0

    Surplus & Slack variables
    Constraint #1 Surplus    : Satisfied at Boundary
    Constraint #2 Surplus    : Satisfied at Boundary
    ========================================================================================================

    Alternate Solution #3
    Taking X1 = 0 for & setting X2 as a Basic Variable for the alternate solution
    Taking X4 = 0 for & setting X4 as a Basic Variable for the alternate solution

    Maximum Value for Objective Function = 1827

    Values for Decision Variables :
        X1      = 0
        X2      = 21.0
        X3      = 0
        X4      = 9.0

    Surplus & Slack variables
    Constraint #1 Surplus    : Satisfied at Boundary
    Constraint #2 Surplus    : Satisfied at Boundary
    ========================================================================================================

Extract an Alternate Optimal Solution
~~~~~~~~~~~~~

Select an alternate optimal solution as a variable using,

.. code-block:: python

    from elpee.algorithms import Alternator 

    # select the 2nd Alternate Optimal Solution - out of 3 possible solutions as shown above
    alternate_2_sol = Alternator.extract_alternate_solution(solution, 2) 