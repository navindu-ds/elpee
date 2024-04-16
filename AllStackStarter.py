from FeasibleHandler import FeasibleHandler
import LPProblem
from alternate_solutions import check_alternate_solutions, get_entering_cols_for_alternates
from bigM_handler import check_artificial_basic_vars
from utilities import create_ratio_col, get_feasible, get_subsets, is_feasible, round_off_simplex_matrix, select_pivot_col, subsitute_big_M_for_row
from SimplexPrinter import SimplexPrinter

class AllStackStarter():
    """
    Class Description for the All Stack Starting Method of solving 
    Linear Programming Optimization Problems
    Acts as the base code for all other LP optimization problems
    """

    def __init__(self, problem: LPProblem):
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

    def __is_optimal(self):
        """
        Returns true if the objective row of the matrix (first row without solution value) indicates optimal solution 
        """
        # substituting for M with large number (1,000,000) before doing comparision

        if self.is_max:
            # for maximization, all coefficients of objective row should be non-negative
            return all(element >= 0 for element in subsitute_big_M_for_row(self.problem.obj_row))
        else:
            # for minimization, all coefficients of objective row should be non-positive
            return all(element <= 0 for element in subsitute_big_M_for_row(self.problem.obj_row))

    def __optimize(self):
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
    
    def __generate_initial_feasible_sol_step(self):
        """
        Function to obtain the initial feasible solutions step by step
        """
        print("\n...Generating Initial Feasible Solution for")
        self.simplex_printer.print_simplex_table_cli(self.problem) # XXX format inputs to be encapsulated within self
        self.__make_feasible()
    
    def __optimize_step(self):
        """
        Function that contains 1 iteration of the optimization step
        """
        old_basic_vars = self.problem.basic_vars.copy()
        optimizable = self.__optimize()
        if not optimizable:
            print("\nCannot be optimized further")
            self.problem.update_optimal_reachability_status(False)
        else:
            self.simplex_printer.print_entering_leaving_vars(old_basic_vars, self.problem)
            self.problem.update_optimal_reachability_status(True)
    
    def __make_feasible(self):
        """
        Function that converts the optimal solution to a feasible optimal solution
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

    def __increment_feasible_sol_num(self):
        self.feasible_count = self.feasible_count + 1

    def __display_new_feasible_sol(self):
        self.__increment_feasible_sol_num()
        print(f"\nFeasible Solution # {self.feasible_count}")
        self.simplex_printer.print_simplex_table_cli(self.problem)

    def __set_infeasible_status(self):
        self.problem.update_feasible_status(False)
        self.problem.update_optimal_reachability_status(False)
        self.problem.update_optimal_status(False)

    def solver(self):
        """
        Main executing function to run the linear programming methodology for 
        all stack starting and dual simplex methods 
        """

        while not(is_feasible(self.problem.basic_vars, self.problem.matrix)):
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

        if check_alternate_solutions(self.problem.obj_row, self.n_constraints):
            # obtain list of variables for generating alternate solutions
            alternate_cols = get_entering_cols_for_alternates(self.problem.basic_vars, self.problem.obj_row)
            alterations_combo_list = get_subsets(alternate_cols)[1:]
            print(f"There are {len(alterations_combo_list)} Alternate Solutions for this problem!")
            print(f">> Use alternate_solutions.extract_alternate_solution() method using version numbers from 1 to {len(alterations_combo_list)}.")
            print(f">> Use alternate_solutions.display_all_alternate_solutions() method to display all alternate solutions")

        # round off coefficients in matrix
        self.problem.matrix = round_off_simplex_matrix(self.problem.matrix)
        return self.problem

            