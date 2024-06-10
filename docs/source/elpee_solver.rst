==================
elpee.elpee_solver
==================

The Solver constructed to solve Linear Programming Problems

Import
------

.. code-block:: python

   from elpee import elpee_solver

Methods
-------

.. data:: solve(lp_problem: Union[StandardProblem, LinearProblem], single_iter : bool = False, show_steps : bool =True, show_interpret : bool =True, create_yaml: str = None) -> StandardProblem

Apply the Linear Programming solution methods to solve a given `elpee.StandardProblem` or `elpee.LinearProblem`  problem

**Parameters**

    - lp_problem : `elpee.LinearProblem` | `elpee.StandardProblem`
        LP problem to be solved 
    - single_iter : `bool` (default : `False`)
        Apply LP methods to generate only next feasible solution. Else solve lp_problem completely
    - show_steps : `bool` (default = `True`)
        Display all iterations occurring in the simplex matrix
    - show_interpret : `bool` (default : `True`)
        Display the interpretation of the solution at each iteration
    - create_yaml : `str` (default : `None`) (Options : `[ "all" , "final" , None ]` ) 
        Save the steps in the solved LP problem. Expected options are 
        
            - `"all"`   : For saving all steps
            - `"final"` : For saving final result only
            - `None`    : No saving

**Return**

    `elpee.StandardProblem` object after optimizing using the all stack starting 
    method. Will return a suboptimal or infeasible `elpee.StandardProblem` object 
    if the problem cannot be optimized. 