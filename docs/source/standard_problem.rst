.. image:: assets/ElpeeBanner.png
   :alt: Elpee Logo
   :width: 200px
   :align: right

=====================
elpee.StandardProblem
=====================

Class to represent the standardized linear programming
optimization Problem to be solved 

.. autoclass:: StandardProblem
   :show-inheritance:

Import
------

.. code-block:: python

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

.. data:: interpret() 

Obtain a dictionary of variables and values corresponding to the generated `elpee.StandardProblem`

**Returns**

Dictionary containing the following keys
- Sol : The value of the objective function
- All basic variables & Decision variables

.. code-block::
    
    # sample dictionary output
    {
        'Sol' : optimal_value,
        'Decision_var_1' : x1_value,
        'Decision_var_2' : x2_value,
        'Slack_1' : S1_value,
        'Slack_2' : S2_value,
        'Artificial_1' : A1_value
    }
    # Only non-zero slack and artificial variable values will be provided


**Example Code**

.. code-block:: python

   standard_problem.interpret()

   # Example Output
   # {'Sol': 25.0, 'x': 5.0, 'y': 0, 'Slack_2': 22.0, 'Slack_3': 18.0}

