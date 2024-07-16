# Copyright 2024-2025 Navindu De Silva
# SPDX-License-Identifier: Apache-2.0

from elpee.utils.feasible import FeasibleHandler
from elpee import StandardProblem
from elpee.utils.printer import SimplexPrinter
from elpee.utils.utilities import create_ratio_col, get_subsets

class AlternateSolver():
    """
    A class to assist the generation of alternate solutions for the given optimal problems

    Attributes
    ----------
    problem : elpee.StandardProblem
        The optimized problem given to find alternate solutions
    n_alternates : int
        Number of alternate solutions available for given optimal StandardProblem
    simplex_printer : elpee.utils.SimplexPrinter 
        An instance of printer to visualize the simplex table
        of given LP problem
    feasible_handler : elpee.utils.FeasibleHandler
        An instance of handler object to retain feasibility of
        LP problem and its solutions

    Methods
    -------
    check_alternate_solutions() -> bool
        Returns True/False if any alternate solutions are present
    extract_alternate_solution(version_num) -> elpee.StandardProblem
        Returns one of the alternate solutions. Version num is in the range of
        1 to n_alternates inclusive
    display_all_alternate_solutions() -> None
        Displays all alternate solutions for given optimal problem
    """

    def __init__(self, problem:StandardProblem, show_simplex_table : bool = True, show_interpret : bool = True):
        self.problem = problem
        self.printer = SimplexPrinter(show_steps=show_simplex_table, show_interpret=show_interpret)
        self.feasible_handler = FeasibleHandler()
        self.n_alternates = len(self.get_alterations_combo_list())
        self.__update_num_alternates()

    def __update_num_alternates(self):
        self.problem.set_num_alternates(self.n_alternates)
        
    def __get_entering_cols_for_alternates(self):
        """
        Returns a list of columns that can be used to create alternative optimal solutions
        Returns a list of column indexes with 0 in the objective row except in basic variable columns
        """

        cols_for_alternates = []
        for i in range(len(self.problem.obj_row)):
            if i+1 not in self.problem.basic_vars:
                if self.problem.obj_row[i] == 0:
                    cols_for_alternates.append(i+1)
        return cols_for_alternates
    
    def __apply_simplex_update(self, pivot_col_var):
        """
        Applies simplex update for the given pivot col to get an updated simplex table
        Returns updated basic_vars list and matrix
        """

        M = 1000000
        
        new_var_name = self.printer.print_var_name(pivot_col_var, self.problem)
        # create a ratio column for the pivot col provided
        ratio_col = create_ratio_col(self.problem.matrix, pivot_col_var)
        if min(ratio_col) == M:
            return None, None 
            # TODO #XXX An error if a solution has says having alternate solutions - but turns out it is not feasible
        else:
            # selecting the leaving variable
            pivot_row = ratio_col.index(min(ratio_col)) + 1
        pivot_row_name = self.printer.print_var_name(self.problem.basic_vars[pivot_row], self.problem)
        print(f"Taking {pivot_row_name} = 0 for & setting {new_var_name} as a Basic Variable for the alternate solution")
        # make the change in basic variables list
        self.problem.basic_vars[pivot_row] = pivot_col_var
        
        # apply feasibility fixes for the matrix with basic variables updated
        self.problem = self.feasible_handler.get_feasible(self.problem)
        if self.problem.matrix == None: 
            return None, None
        
        # return the updated basic_vars, matrix after simplex updates
        return self.problem.basic_vars, self.problem.matrix
    
    def get_alternate_solutions(self, alteration_combo):
        """
        For a given set of columns for which an alternate solution can be derived,
        apply simplex updates to all the columns provided in alteration combo list and prints final alternate solution
        """

        for pivot_col in alteration_combo:
            self.problem.basic_vars, self.problem.matrix = self.__apply_simplex_update(pivot_col)
            if self.problem.matrix == None:
                print("\nFeasible alternate solution not found")
                return None, None
        # print the final alternate solution based on set of columns provided
        self.printer.print_simplex_table_cli(self.problem)
    
    def get_alterations_combo_list(self):
        """
        Provides the combinations of changes done to the original LP problem 
        to derive alternate optimal solutions
        """
        
        # obtain list of variables for generating alternate solutions
        alternate_cols = self.__get_entering_cols_for_alternates()
        # obtain a list of combinations of columns for creating all possible alternate solutions
            # exclude the null set when extracting the subsets
        alterations_combo_list = get_subsets(alternate_cols)[1:]
        return alterations_combo_list


def check_alternate_solutions(problem: StandardProblem):
    """
    Checks if the given problem has alternate solutions

    Parameters
    ----------
    problem : `elpee.StandardProblem`
        Optimized LP problem to check for alternate optimal solutions

    Return
    ------
    True/False  
    """

    alternator = AlternateSolver(problem=problem)

    # Checks if the simplex matrix has any alternate optimal solutions
    # Compares and checks if there are higher number of zeros in the objective row
    # Returns True when there are alternative optimal solutions
    num_zeros = alternator.problem.obj_row.count(0)
    if alternator.problem.is_optimal:
        if num_zeros > alternator.problem.n_constraints:
            return True
        elif num_zeros == alternator.problem.n_constraints:
            return False
    else:
        print("\nSolution not optimal")
        return False
    
def extract_alternate_solution(problem: StandardProblem, version_num: int, 
                               show_simplex_table : bool = True, show_interpret : bool = True) -> StandardProblem:
    """
    Extracts an alternate solution based on version_num provided 

    Parameters
    ----------
    problem : `elpee.StandardProblem`
        Optimized LP problem to check for alternate optimal solutions
    version_num : int
        index of the alternate solution to generate in the range 1 to num_alternates
    show_simplex_table : bool (default : True)
        Display the simplex tables of all alternate optimal solutions
    show_interpret : bool (default : True)
        Provide interpretation of all alternate optimal solutions
    
    Return
    ------
    elpee.StandardProblem containing alternate solution based on given index
    """

    alternator = AlternateSolver(problem=problem, show_simplex_table=show_simplex_table, show_interpret=show_interpret)

    if not alternator.problem.is_optimal:
        print(f"\nGiven problem is not optimal. No alternate solutions exist.")
        return None

    if alternator.problem.num_alternates != 0:
        alterations_combo_list = alternator.get_alterations_combo_list()

        if version_num <= len(alterations_combo_list):
            print(f"\nAlternate Solution #{version_num}")
            alternator.get_alternate_solutions(alterations_combo_list[version_num-1])
            return alternator.problem
        else:
            print(f"\nThere are only {len(alterations_combo_list)} versions for Alternate Solutions!")
            print(f"Cannot return Alternate Solution #{version_num}")
            return None
    else:
        print("There are no alternate solutions!")
        return None

def display_all_alternate_solutions(problem : StandardProblem, show_simplex_table : bool = True, show_interpret : bool = True):
    """
    Display all alternate solutions for given optimal problem

    Parameters
    ----------
    problem : `elpee.StandardProblem`
        Optimized LP problem to display alternate optimal solutions
    show_simplex_table : bool (default : True)
        Display the simplex tables of all alternate optimal solutions
    show_interpret : bool (default : True)
        Provide interpretation of all alternate optimal solutions
    """

    alternator = AlternateSolver(problem=problem, show_simplex_table=show_simplex_table, show_interpret=show_interpret)
    
    print("\nDisplaying all Alternate Optimal Solutions for LP Problem provided...")

    if not alternator.problem.is_optimal:
        print("\nGiven problem is not optimal. No alternate solutions exist.")
    else:
        if alternator.problem.num_alternates != 0:
            alterations_combo_list = alternator.get_alterations_combo_list()
            initial_problem = alternator.problem.copy()

            for i, alteration_combo in enumerate(alterations_combo_list):
                print(f"\nAlternate Solution #{i+1}")
                alternator.get_alternate_solutions(alteration_combo)

                alternator.problem = initial_problem
        else:
            print("\nThere are no alternate solutions to display!")