Working with Alternate Optimal Solutions 
========================================

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
---------------------------------------------

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
-------------------------------------

Select an alternate optimal solution as a variable using,

.. code-block:: python

    from elpee.algorithms import Alternator 

    # select the 2nd Alternate Optimal Solution - out of 3 possible solutions as shown above
    alternate_2_sol = Alternator.extract_alternate_solution(solution, 2) 