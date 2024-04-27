from elpee.algorithms.dual_simplex import DualSimplexSolver
from elpee.utils.protocols.lp_problem import LPProblem

DECIMALS = 3

class FeasibleHandler():
    """
    Class description for performing updates to Linear Programming Problem to have 
    feasible solutions by verifying and performing feasibility fixes if not feasible
    """
    def __init__(self):
        self.problem = None

    def __check_feasible_positive_sol(self):
        """
        Criteria 1 for feasibility
        Checks feasibility of matrix by checking the if the solution is positive for the constraint rows (not the objective row)
        If returns false --> matrix requires dual simplex handling 
        """
        n_rows = len(self.problem.matrix)

        for i in range(1, n_rows):
            if self.problem.matrix[i][-1] < 0:
                return False

        return True
    
    def __check_0_1_pattern(self):
        """
        Criteria 2 for feasibility
        Checks if the columns that correspond to the basic variables of the matrix contains the 0-1 pattern
        where the column has all zeros except at the row of the same basic variable
            i.e. matrix[basic_var][basic_var] = 1
            else for each row, matrix[row][basic_var] = 0
        If returns false --> requires to fix the pattern using linear algebraic row operations
        """
        for i, var in enumerate(self.problem.basic_vars[1:]):
            column = [row[var-1] for row in self.problem.matrix]

            if column[i+1] != 1 or (column.count(0) != (len(column) -1)):
                return False
        return True
    
    def is_feasible(self, problem:LPProblem):
        """
        Checks overall feasibility of the matrix based on the 2 criteria
        """
        self.problem = problem
        if self.__check_feasible_positive_sol():
            if self.__check_0_1_pattern():
                return True
        return False   

    def __fix_feasible_0_1_pattern(self):
        """
        Function to fix the 0-1 pattern for columns of basic variables
        Does scaled multiplication to the row of the basic variable if matrix[basic_var][basic_var] != 1
        Does scaled addition of the basic variable row onto rows where matrix[row][basic_var] != 0
        """
        n_rows = self.problem.n_constraints + 1
        for row_i ,basic_var in enumerate(self.problem.basic_vars):
            # no need to check 0-1 pattern for objective variable
            if basic_var == 0:
                continue

            # checking and fixing basic variables coefficient into 1
            if self.problem.matrix[row_i][basic_var-1] != 1:
                self.problem.matrix[row_i] = [element / self.problem.matrix[row_i][basic_var-1] for element in self.problem.matrix[row_i]]

            # checking if zeros are maintained for 0-1 pattern
            for i in range(n_rows):
                # except for row with the basic variable
                if i != row_i:  
                    if self.problem.matrix[i][basic_var-1] != 0:
                        scaled_piv_row = [element * self.problem.matrix[i][basic_var-1] for element in self.problem.matrix[row_i]]
                        self.problem.matrix[i] = [a-b for a,b in zip(self.problem.matrix[i], scaled_piv_row)]

    def get_feasible(self, problem:LPProblem):
        """
        Applies the functionalities for correcting the matrix table to obtain feasibility
        If no feasible solution exists --> return None
        """
        self.problem = problem
        ds_solver = DualSimplexSolver(problem)
        if not(self.__check_feasible_positive_sol()):
            self.problem = ds_solver.solver()
 
        if self.problem.is_feasible == True:
            self.__fix_feasible_0_1_pattern()
        
        return self.problem