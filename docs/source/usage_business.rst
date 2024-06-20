Apply Linear Programming Optimization for Business Use Cases
============================================================

Here we will discuss some examples of applying linear programming to optimize business & production operations with the help of the `elpee` python library.

Identifying the Optimal Production Plan
---------------------------------------

Example Problem ❓
~~~~~~~~~~~~~~~~~~

A local paint company produces four types of paints (A, B, C, and D) by using three types of raw 
materials (R1, R2, and R3) with different compositions. The following tabulation shows the 
relevant production and market information. 

.. list-table:: Raw Material Requirement & Profit for each Paint Product
   :widths: 15 15 15 15 15
   :header-rows: 1

   * - 
     - RM1 (kg)
     - RM2 (kg)
     - RM3 (kg)
     - Profit/liter ($)
   * - Paint A
     - 3
     - 1
     - 4
     - 19
   * - Paint B
     - 2
     - 1
     - 3
     - 13
   * - Paint C
     - 1
     - 1
     - 3
     - 12
   * - Paint D
     - 2
     - 1
     - 4
     - 17
   * - Available (kg)
     - 225
     - 117
     - 420
     - 

The above table shows how much kilograms from raw materials RM1, RM2, RM3 are required to produce
1 liter of paint.

*For example, to produce 1 liter of paint A, it requires 3kg of RM1, 1kg of RM2 and 4kg of RM3. 1 liter of Paint A can earn a profit of $19.*

Define the Objective 💵
~~~~~~~~~~~~~~~~~~~~~~~

We require to find the amount of paint in liters to be produced for each of Paint A, B, C and D 
to maximize profit.

Since this is a (profit) maximization problem, let's define a new `LinearProblem` to be solved.

.. code-block:: python

    from elpee import LinearProblem

    production_problem = LinearProblem(is_maximization=True)

The objective function or the total profit equation can be obtained by adding up the profits earned 
by each paint type. Let the `V_{paint_id}` be the volume of paint to be produced for each type.

.. code-block:: python

    ## profit from paint A = 19*V_1
    ##                   B = 13*V_2
    ##                   C = 12*V_3
    ##                   D = 17*V_4

    total_profit_eq = '19*V_1 + 13*V_2 + 12*V_3 + 17*V_4'
    production_problem.add_objective(total_profit_eq)

Provide the constraints ⛔
~~~~~~~~~~~~~~~~~~~~~~~~~~

The constraints for production is the limitation of raw materials. 
The amount of raw materials used by all 4 paint types should be less than 
the avaialble (kg) of paint present.

.. list-table:: Raw Material Usage
   :widths: 10 20 20
   :header-rows: 1
   
   * - Raw Material
     - Used amount of Raw Material (kg)
     - Max Available Raw Material (kg)
   * - RM1
     - 3*V_1 + 2*V_2 + 1*V_3 + 2*V_4
     - 225
   * - RM2 
     - 1*V_1 + 1*V_2 + 1*V_3 + 1*V_4
     - 117
   * - RM3
     - 4*V_1 + 3*V_2 + 3*V_3 + 4*V_4
     - 420

Since there are 3 raw materials used for production of the paint items,
we can create three `less than or equal` (<=) constraints to be added to this production problem. 

.. code-block:: python

    constraint_rm1 = "3*V_1 + 2*V_2 + V_3 + 2*V_4 <= 225"
    constraint_rm2 = "V_1 + V_2 + V_3 + V_4 <= 117"
    constraint_rm3 = "4*V_1 + 3*V_2 + 3*V_3 + 4*V_4 <= 420"

    production_problem.add_constraint(constraint_rm1)
    production_problem.add_constraint(constraint_rm2)
    production_problem.add_constraint(constraint_rm3)

Find the best plan 📜
~~~~~~~~~~~~~~~~~~~~~

Now the production problem is defined, we can use `elpee` to find the solution. If you want the quick solution, 
we can set ``show_steps = False`` & ``show_interpret = False``.

.. code-block:: python

    from elpee import elpee_solver

    production_solution = elpee_solver.solve(
        lp_problem= production_problem,
        show_steps= False,
        show_interpret= False
    ) 

To which we get the output with the production plan as follows in the end,

.. code-block:: 

    Optimized Solution Received!

    Maximum Value for Objective Function = 1827.0

    Values for Decision Variables :
        V_1      = 39.0
        V_2      = 0
        V_3      = 48.0
        V_4      = 30.0

    Surplus & Slack variables
    Constraint #1 Surplus    : Satisfied at Boundary
    Constraint #2 Surplus    : Satisfied at Boundary
    Constraint #3 Surplus    : Satisfied at Boundary

With this, it indicates that ``39 liters of Paint A``, ``48 liters of Paint B`` and ``30 liters of Paint D`` will be produced. 
``Paint B will not be produced`` if we want the most profit to be generated.

If you like to see the steps for finidng the production plan set ``show_steps = True`` & ``show_interpret = True`` (or leave the parameters as default)

.. code-block:: python

    from elpee import elpee_solver

    production_solution = elpee_solver.solve(
        lp_problem= production_problem,
        show_steps= True,
        show_interpret= True
    ) 
