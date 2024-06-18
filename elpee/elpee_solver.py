# Copyright 2024-2025 Navindu De Silva
# SPDX-License-Identifier: Apache-2.0

from typing import Union

from elpee.algorithms.all_stack_starter import AllStackStarter
from elpee.datahandler.data_handler import save_file
from elpee.utils.protocols.lp_problem import LinearProblem
from elpee.utils.protocols.st_problem import StandardProblem
from elpee.utils.printer import SimplexPrinter


class ElpeeSolver():
    """
    The Solver constructed to solve Linear Programming Problems
    
    Methods
    -------
    solve() -> elpee.StandardProblem
        Solves the given LP problem under defined configurations
    """

    @classmethod
    def solve(
        self,
        lp_problem: Union[StandardProblem, LinearProblem], 
        single_iter : bool = False, 
        show_steps : bool =True, 
        show_interpret : bool =True,
        file_format: str = None,
        freq: str = None) -> StandardProblem:
        """
        Apply the Linear Programming solution methods to solve a given problem.

        Parameters
        ---------
        lp_problem : `elpee.LinearProblem` | `elpee.StandardProblem`
            LP problem to be solved 
        single_iter : bool (default : False)
            Apply LP methods to generate only next feasible solution. Else solve lp_problem completely
        show_steps : bool (default = True)
            Display all iterations occurring in the simplex matrix
        show_interpret : bool (default : True)
            Display the interpretation of the solution at each iteration
        file_format : `str` (default : `None`) (Options : ["yaml","json",`None`]) 
            Save the steps on solution in `json` or `yaml` file formats if provided
        freq : str (default : None) (Options : ["all","final",`None`]) 
            Save the steps in the solved LP problem. The freuency is 
            overidden to None if the file_format is `None`. Expected 
            options are 
            "all"   : For saving all steps
            "final" : For saving final result only
            None    : No saving

        Return
        ------
        `elpee.StandardProblem` object after optimizing using the all stack starting 
        method. Will return a suboptimal or infeasible `elpee.StandardProblem` object 
        if the problem cannot be optimized. 
        """

        if file_format == None:
            freq = None
        
        # convert the LinearProblem object to StandardProblem
        if isinstance(lp_problem, LinearProblem):
            lp_problem = lp_problem.standardize_problem()

        # configure all stack starter method to solve problem
        solver_app = AllStackStarter(lp_problem)

        lp_solution = solver_app.solver(do_step=single_iter, show_steps=show_steps, show_interpret=show_interpret, 
                                        file_format=file_format, freq=freq)

        if not (show_interpret):
            SimplexPrinter().interpret_problem(lp_solution)

        if (freq == "final") & (file_format != None):
            save_file(lp_solution, file_format=file_format, file_path=f"solution\\final_sol.{file_format}")

        return lp_solution