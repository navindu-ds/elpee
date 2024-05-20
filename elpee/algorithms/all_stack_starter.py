from elpee.utils.feasible import FeasibleHandler
from elpee.utils.protocols.st_problem import StandardProblem
from elpee.algorithms.alternator import AlternateSolver
from elpee.algorithms.big_m import check_artificial_basic_vars
from elpee.utils.utilities import create_ratio_col, round_off_simplex_matrix, select_pivot_col, subsitute_big_M_for_row
from elpee.utils.printer import SimplexPrinter

class AllStackStarter():
    """
    A class used to solve problems using All Stack Starting Method

    Attributes
    ----------
    problem : elpee.StandardProblem
        The problem given to the AllStackSolver to be solved
    is_max : bool
        Whether given LP problem is a maximization or 
        minimization problem
    n_decision_vars : int
        Number of decision variables (X_i) in given LP problem
    n_slack_vars : int
        Number of slack variables (S_i) in given LP problem
    n_artificials : int
        Number of artificial variables (A_i) in LP problem
    n_cols : int
        Number of variables present in the simplex table of 
        the LP problem
    n_constraints : int
        Number of constraints in given LP problem
    feasible_count : int
        Step counter to optimal solution counting number of
        intermediate feasible solutions generated
    simplex_printer : elpee.utils.SimplexPrinter 
        An instance of printer to visualize the simplex table
        of given LP problem
    feasible_handler : elpee.utils.FeasibleHandler
        An instance of handler object to retain feasibility of
        LP problem and its solutions

    Methods
    -------
    solver() -> elpee.StandardProblem
        Solves the Standardized LP problem given to AllStackStarter instance
    """

    def __init__(self, problem: StandardProblem):
        """
        Parameters
        ----------
        problem : elpee.StandardProblem
            Standardized LP problem to be solved using All Stack Starting Method
        """
        
        self.problem = problem
        self.is_max = problem.is_max
        self.n_decision_vars = problem.n_decision_vars
        self.n_slack_vars = problem.n_slack_vars
        self.n_artificials = problem.n_artificials
        self.n_cols = len(problem.obj_row)
        self.n_constraints = problem.n_constraints
        self.feasible_count = 0
        self.simplex_printer = SimplexPrinter()
        self.feasible_handler = FeasibleHandler()

    def __is_optimal(self) -> bool:
        """
        Returns true if the objective row of the matrix (first row without 
        solution value) indicates optimal solution 
        """

        # substituting for M with large number (1,000,000) before doing comparision

        if self.is_max:
            # for maximization, all coefficients of objective row should be non-negative
            return all(element >= 0 for element in subsitute_big_M_for_row(self.problem.obj_row))
        else:
            # for minimization, all coefficients of objective row should be non-positive
            return all(element <= 0 for element in subsitute_big_M_for_row(self.problem.obj_row))

    def __optimize(self) -> bool:
        """
        Core function for optimizing the matrix by changing the basic variables
        When matrix cannot be optimized will return None
        """

        M = 1000000
        blocked_cols = []
        while len(blocked_cols) < self.n_cols:
            pivot_col_var = select_pivot_col(self.problem.obj_row, self.is_max, blocked_cols)
            if pivot_col_var == -1:
                # No suitable pivot column available
                print("\nNo suitable entering varaible for selection")
                
                # unsuccessfully optimized
                return False
            ratio_col = create_ratio_col(self.problem.matrix, pivot_col_var)
            if min(ratio_col) == M:
                # invalid ratio column with no suitable selections to be made
                # will block the pivot col from being selected again 
                # and find an alternate entering variable
                blocked_cols.append(pivot_col_var)
            else:
                # leaving varaible identified
                pivot_row_var = ratio_col.index(min(ratio_col)) + 1
                break
        self.problem.basic_vars[pivot_row_var] = pivot_col_var
        
        # successfully optimized
        return True
    
    def __generate_initial_feasible_sol_step(self) -> None:
        """
        Function to obtain the initial feasible solutions step by step
        """

        print("\n...Generating Initial Feasible Solution for")
        self.simplex_printer.print_simplex_table_cli(self.problem) # XXX format inputs to be encapsulated within self
        self.__make_feasible()
    
    def __optimize_step(self) -> None:
        """
        Function that contains 1 iteration of the optimization step
        """

        old_basic_vars = self.problem.basic_vars.copy()
        optimizable = self.__optimize()
        if not optimizable:
            print("\nCannot be optimized further")
        else:
            self.simplex_printer.print_entering_leaving_vars(old_basic_vars, self.problem)
        self.problem.update_optimal_reachability_status(optimizable)
    
    def __make_feasible(self) -> None:
        """
        Function that converts the optimal solution to a feasible optimal 
        solution
        """

        old_basic_vars = self.problem.basic_vars.copy()
        self.problem = self.feasible_handler.get_feasible(self.problem)
        if self.problem.is_feasible == False:
            if self.feasible_count != 0:
                print("\nNo further feasible solution found")
            else:
                print("\nNo feasible solution found")
        else:
            self.simplex_printer.print_entering_leaving_vars(old_basic_vars, self.problem)

    def __increment_feasible_sol_num(self) -> None:
        """
        Function to increment the number of feasible solutions count
        """
        
        self.feasible_count = self.feasible_count + 1

    def __display_new_feasible_sol(self) -> None:
        """
        Function to display the current contents of the StandardProblem object
        as a simplex table 

        This function is called only after generating a feasible solution 
        at each iteration of the all stack starting method
        """

        self.__increment_feasible_sol_num()
        print(f"\nFeasible Solution # {self.feasible_count}")
        self.simplex_printer.print_simplex_table_cli(self.problem)

    def __set_infeasible_status(self) -> None:
        """
        Function to update the status attributes of the StandardProblem object
        when the problem is infeasible to be solved
        """

        self.problem.update_feasible_status(False)
        self.problem.update_optimal_reachability_status(False)
        self.problem.update_optimal_status(False)

    def solver(self) -> StandardProblem:
        """
        Executing function to solve the linear programming problems using 
        all stack starting method 

        Return
        ------
        StandardProblem object after optimizing using the all stack starting 
        method. May return a suboptimal or infeasible StandardProblem object if
        the problem cannot be optimized. 
        """

        while not(self.feasible_handler.is_feasible(self.problem)):
            self.__generate_initial_feasible_sol_step()
            if not self.problem.is_feasible:
                self.problem.matrix = round_off_simplex_matrix(self.problem.matrix)
                # no feasible solution
                return self.problem
        
        self.__display_new_feasible_sol()
        
        while not(self.__is_optimal()):
            self.__optimize_step()
            if not self.problem.is_optimal_reachable:
                self.problem.matrix = round_off_simplex_matrix(self.problem.matrix)
                # cannot be optimized
                return self.problem
        
            self.__make_feasible()
            if not self.problem.is_feasible:
                self.problem.matrix = round_off_simplex_matrix(self.problem.matrix)
                # no further feasible solution
                return self.problem
            
            self.__display_new_feasible_sol()

        if (check_artificial_basic_vars(self.problem)):
            self.problem.matrix = round_off_simplex_matrix(self.problem.matrix)
            self.__set_infeasible_status()
            print("\nArtificial variables found in optimal soltion.\nProblem is infeasible.")
            return self.problem
        else:
            self.problem.update_optimal_status(True)
            print("\nOptimized Solution Received!")
        
        alternator = AlternateSolver(self.problem)
        if alternator.n_alternates != 0:
            print(f"There are {alternator.n_alternates} Alternate Solutions for this problem!")
            # print(f">> Use alternate_solutions.extract_alternate_solution() method using version numbers from 1 to {num_alternate_sols}.")
            # print(f">> Use alternate_solutions.display_all_alternate_solutions() method to display all alternate solutions")

        # round off coefficients in matrix
        self.problem.matrix = round_off_simplex_matrix(self.problem.matrix)
        return self.problem

            