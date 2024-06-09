===
API
===

.. autosummary::
   :toctree: generated

   elpee

===================
elpee.LinearProblem
===================

Class to represent the linear programming optimization problem 
with its objective function, constraints and other conditions

.. autoclass:: LinearProblem
   :show-inheritance:

elpee.LinearProblem(is_maximization: bool = True)
-------------------------------------------------

.. data:: __init__(self, is_maximization: bool = True, objective_expr: str=None) -> None:

Creates an empty `LinearProblem` to be solved with sense either 
Maximize (`True`) or Minimize (`False`).

Example Code ::
   lp_problem = LinearProblem(is_maximization=True)

.. data:: add_objective(self, objective_expr: str) -> None:

Define the objective function expression into the linear 
programming problem. Replaces previous objective function.

**Parameters**
objective_expr : str
   String expression of the objective function of LP Problem 

**Exceptions**
   ValueError is thrown when objective function expression is not
   valid