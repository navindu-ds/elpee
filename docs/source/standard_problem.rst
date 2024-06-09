===================
elpee.StandardProblem
===================

Class to represent the standardized linear programming
optimization Problem to be solved 

.. autoclass:: StandardProblem
   :show-inheritance:

Import
------

.. code-block:: python::

   from elpee import StandardProblem

Methods
-------

.. data:: __init__(matrix: List[List[int]], basic_vars: List[int], n_decision_vars: int, is_max: bool = True, n_artificials: int = 0, var_name_list: List[str] = None)

Initializes a `elpee.StandardProblem` designed for computational purposes to be solved.

**Parameters**

    - matrix : `List` [ `List` [ `int` ]]
        The simplex matrix representation of the LinearProblem
    - basic_vars : `List` [ `int` ]
        The ordered list of indices mapped to the basic variables in the Linear Problem
    - n_decision_vars : `int`
        The number of decision variables in the Linear Problem
    - is_max : `int` [default = `True`]
        Sets a maximization LP problem when `True`. Else sets a minimization problem when `False`.
    - n_artificials : `int` [default = 0]
        The number of artificial variables used to set up the simplex matrix representation
    - var_name_list : `List` [ `str` ] [Optional] [default = `None`]
        The names / symbols of all decision variables 