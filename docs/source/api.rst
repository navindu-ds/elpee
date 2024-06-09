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

Creates an empty `LinearProblem` to be solved with sense either Maximize (`True`) or Minimize (`False`).

.. data:: solve