.. image:: assets/ElpeeBanner.png
   :alt: Elpee Logo
   :width: 200px
   :align: right

===================
elpee.LinearProblem
===================

Class to represent the linear programming optimization problem 
with its objective function, constraints and other conditions

.. autoclass:: LinearProblem
   :show-inheritance:

Import
------

.. code-block:: python

   from elpee import LinearProblem

Methods
-------

.. data:: __init__(is_maximization: bool = True, objective_expr: str=None) -> None

Creates an empty `elpee.LinearProblem` to be solved with sense either 
Maximize (`True`) or Minimize (`False`).

**Parameters**

    - is_maximization : `bool` [Default = `True`]
        Sets a maximization LP problem when `True`. Else sets a minimization LP problem.
    - objective_expr : `str` [Optional]
        String expression of the objective function of LP Problem 


**Example Code**

.. code-block:: python

   lp_problem = LinearProblem(is_maximization=True)



.. data:: add_objective(objective_expr: str) -> None

Define the objective function expression into the linear 
programming problem. Replaces previous objective function.

**Parameters**

    - objective_expr : str
        String expression of the objective function of LP Problem 

**Exceptions**
   
   `ValueError` is thrown when objective function expression is not
   valid

**Example Code**

.. code-block:: python

   lp_problem.add_objective("5*x1 + 4*x2")



.. data:: add_constraint(constraint_expr: str) -> None

Add a new constraint to existing LP Problem.

**Parameters**

    - constraint_expr : `str``
        String expression of a mathematical inequality of equality 
        to represent as a new constraint

**Exceptions**
   
   `ValueError` is thrown when objective function expression is not
   valid

**Example Code**

.. code-block:: python

   lp_problem.add_constraint("6*x1 + 4*x2 <= 24")
   lp_problem.add_constraint("x1 + 2*x2 <= 6")



.. data:: use_bigM() -> None

Configures the LP problem to be solved using big M method



.. data:: use_dual_simplex() -> None

Configures the LP problem to be solved using Dual Simplex method



.. data:: standardize_problem() -> `elpee.StandardProblem`

Convert the given Linear Programming problem into a Standardized Linear 
Programming Problem for computation

**Returns**

`elpee.StandardProblem` object with LinearProblem converted for computation

**Example Code**

.. code-block:: python

   lp_problem.standardize_problem()