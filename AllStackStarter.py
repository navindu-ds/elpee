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
        self.n_cols = len(problem.matrix[0][:-1])
        self.n_constraints = len(self.problem.matrix) - 1
        self.feasible_count = 0
        self.simplex_printer = SimplexPrinter()

    def __is_optimal(self):
        """
        Returns true if the objective row of the matrix (first row without solution value) indicates optimal solution 
        """
        # substituting for M with large number (1,000,000) before doing comparision

        if self.is_max:
            # for maximization, all coefficients of objective row should be non-negative
            return all(element >= 0 for element in subsitute_big_M_for_row(self.problem.matrix[0][:-1]))
        else:
            # for minimization, all coefficients of objective row should be non-positive
            return all(element <= 0 for element in subsitute_big_M_for_row(self.problem.matrix[0][:-1]))

    def __optimize(self):
        """
        Core function for optimizing the matrix by changing the basic variables
        When matrix cannot be optimized will return None
        """
        M = 1000000
        blocked_cols = []
        while len(blocked_cols) < self.n_cols:
            pivot_col_var = select_pivot_col(self.problem.matrix[0][:-1], self.is_max, blocked_cols)
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
        return self.__make_feasible()
    
    def __optimize_step(self):
        """
        Function that contains 1 iteration of the optimization step
        """
        old_basic_vars = self.problem.basic_vars.copy()
        optimizable = self.__optimize()
        if not optimizable:
            print("\nCannot be optimized further")
            return False
        self.simplex_printer.print_entering_leaving_vars(old_basic_vars, self.problem)
        return True
    
    def __make_feasible(self):
        """
        Function that converts the optimal solution to a feasible optimal solution
        """
        old_basic_vars = self.problem.basic_vars.copy()
        self.problem.basic_vars, self.problem.matrix = get_feasible(self.problem)
        if self.problem.matrix == None:
            if self.feasible_count != 0:
                print("\nNo further feasible solution found")
            else:
                print("\nNo feasible solution found")
            return False
        self.simplex_printer.print_entering_leaving_vars(old_basic_vars, self.problem)
        return True

    def __increment_feasible_sol_num(self):
        self.feasible_count = self.feasible_count + 1

    def __display_new_feasible_sol(self):
        self.__increment_feasible_sol_num()
        print(f"\nFeasible Solution # {self.feasible_count}")
        self.simplex_printer.print_simplex_table_cli(self.problem)

    def solver(self):
        """
        Main executing function to run the linear programming methodology for 
        all stack starting and dual simplex methods 
        """

        while not(is_feasible(self.problem.basic_vars, self.problem.matrix)):
            obtained_feasible = self.__generate_initial_feasible_sol_step()
            if not obtained_feasible:
                # no feasible solution
                return False
        
        self.__display_new_feasible_sol()
        
        while not(self.__is_optimal()):
            obtained_optimizable = self.__optimize_step()
            if not obtained_optimizable:
                # cannot be optimized
                return False
        
            obtained_feasible = self.__make_feasible()
            if not obtained_feasible:
                # no further feasible solution
                return False
            
            self.__display_new_feasible_sol()

        if (check_artificial_basic_vars(self.problem.basic_vars, self.problem.matrix[0][:-1], self.n_decision_vars, self.n_artificials)):
            print("\nArtificial variables found in optimal soltion.\nProblem is infeasible.")
            return False
        else:
            print("\nOptimized Solution Received!")

        if check_alternate_solutions(self.problem.matrix[0][:-1], self.n_constraints):
            # obtain list of variables for generating alternate solutions
            alternate_cols = get_entering_cols_for_alternates(self.problem.basic_vars, self.problem.matrix[0][:-1])
            alterations_combo_list = get_subsets(alternate_cols)[1:]
            print(f"There are {len(alterations_combo_list)} Alternate Solutions for this problem!")
            print(f">> Use alternate_solutions.extract_alternate_solution() method using version numbers from 1 to {len(alterations_combo_list)}.")
            print(f">> Use alternate_solutions.display_all_alternate_solutions() method to display all alternate solutions")

        # round off coefficients in matrix
        self.problem.matrix = round_off_simplex_matrix(self.problem.matrix)
        return True

            