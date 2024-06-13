.. image:: assets/ElpeeBanner.png
   :alt: Elpee Logo
   :width: 200px
   :align: right


================
elpee.alternator
================

Module to assist the generation of alternate solutions for the given optimal problems

Import Functions
----------------

.. code-block:: python

    from elpee.alternator import *

Functions
---------

.. data:: check_alternate_solutions(problem: StandardProblem) -> bool

Checks if the optimized `elpee.StandardProblem` has other alternate optimal solutions

**Parameters**

    - problem : `elpee.StandardProblem`
        Optimized LP problem to check for alternate optimal solutions
        
**Return**

    Returns `True` when other alternate optimal solutions exist. Else `False`

**Example Code**

.. code-block:: python

    from elpee.alternator import check_alternate_solutions

    # optimized_sol is an optimized solution obtained from elpee.ElpeeSolver.solve() 

    has_alternates = check_alternate_solutions(optimized_sol)



.. data:: extract_alternate_solution(problem: StandardProblem, version_num: int, show_simplex_table : bool = True, show_interpret : bool = True) -> StandardProblem

Extracts an alternate solution based on `version_num` provided

**Parameters**

    - problem : `elpee.StandardProblem`
        Optimized LP problem to check for alternate optimal solutions
    - version_num : `int`
        index of the alternate solution to generate in the range 1 to `num_alternates`
    - show_simplex_table : `bool` [default = `True` ]
        Display the simplex tables of all alternate optimal solutions
    - show_interpret : `bool` [default : `True` ]
        Provide interpretation of all alternate optimal solutions
    
**Return**

    `elpee.StandardProblem` containing alternate solution based on given index

**Example Code**

.. code-block:: python

    from elpee.alternator import extract_alternate_solution

    # optimized_sol is an optimized solution obtained from elpee.ElpeeSolver.solve() 

    # returns the 2nd alternate solution
    alternate_2_sol = extract_alternate_solution(optimized_sol, 2)



.. data:: display_all_alternate_solutions(problem : StandardProblem, show_simplex_table : bool = True, show_interpret : bool = True) -> None:

Display all alternate solutions for given optimal problem

**Parameters**

    - problem : `elpee.StandardProblem`
        Optimized LP problem to display alternate optimal solutions
    - show_simplex_table : `bool` [default : `True` ]
        Display the simplex tables of all alternate optimal solutions
    - show_interpret : `bool` [default : `True` ]
        Provide interpretation of all alternate optimal solutions

**Example Code**

.. code-block:: python

    from elpee.alternator import display_all_alternate_solutions 

    # optimized_sol is an optimized solution obtained from elpee.ElpeeSolver.solve() 

    display_all_alternate_solutions(optimized_sol)

