from typing import List
from elpee.utils.protocols.lp_problem import LPProblem

M = 1000000

class DualSimplexSolver():
    """
    Class Description of Dual Simplex Solving Algorithm
    Used when the solution column of the matrix has negative values
    """
    def __init__(self, problem: LPProblem):
        self.problem = problem

    def __select_pivot_col_dual_simplex(self, ratio_row:List, blocked_cols:List):
        """
        Selects the pivot column based on ratio row and not in blocked list
        """
        sorted_idx = sorted(range(len(ratio_row)), key=lambda k: ratio_row[k])
        for n in sorted_idx:
            pivot_col_var = n + 1
            if pivot_col_var not in blocked_cols:
                return pivot_col_var
        print("\nNo suitable pivot column - Choosing another pivot row")
        return -1

    def __select_pivot_row_dual_simplex(self, blocked_rows):
        """
        Selects the appropriate pivot row that has a negative solution value and not in blocked list
        """
        sol_col = []
        neg_sol = 0
        for i, row in enumerate(self.problem.matrix):
            if i !=0:
                sol_col.append(row[-1])
                if row[-1] < 0:
                    neg_sol += 1
        sorted_idx = sorted(range(len(sol_col)), key=lambda k: sol_col[k])

        for i in range(neg_sol):
            if self.problem.basic_vars[sorted_idx[i]+1] not in blocked_rows:
                return sorted_idx[i]+1
        print("\nNo suitable pivot row - Cannot make feasible solution")
        return -1
    
    def __create_ratio_row(self, pivot_row:int, pivot_row_var:int):
        """
        Creates the ratio row given the selected pivot row as 
            absolute value of (objective_row / pivot row)
        Marks 0 and infinity ratios as M
        """
        obj_row = self.problem.obj_row
        ratio_row = [0]*len(obj_row)
        for i in range(len(obj_row)):
            if self.problem.matrix[pivot_row][i] == 0:
                ratio_row[i] = M
            elif obj_row[i] == 0:
                ratio_row[i] = M
            else:
                ratio_row[i] = abs(obj_row[i] / self.problem.matrix[pivot_row][i])
        ratio_row[pivot_row_var-1] = M
        return ratio_row
    
    def __set_infeasible_status(self):
        self.problem.update_feasible_status(False)
        self.problem.update_optimal_reachability_status(False)
        self.problem.update_optimal_status(False)
    
    def solver(self):
        """
        Main executing function to execute dual simplex adjustments to the simplex matrix
        """
        blocked_rows = []
        n_rows = self.problem.n_constraints + 1
        n_cols = len(self.problem.obj_row)
        while len(blocked_rows) < n_rows:
            pivot_row = self.__select_pivot_row_dual_simplex(blocked_rows)
            if pivot_row == -1:
                # print("\nNo further feasible solution")
                self.__set_infeasible_status()
                return self.problem
            pivot_row_var = self.problem.basic_vars[pivot_row]

            blocked_cols = []

            ratio_row = self.__create_ratio_row(pivot_row, pivot_row_var)
            
            j = 1
            while (j <= n_cols) & (sorted(ratio_row)[j-1] != M): 
                pivot_col_var = self.__select_pivot_col_dual_simplex(ratio_row, blocked_cols)
                if pivot_col_var != -1:
                    pivot_cell = self.problem.matrix[pivot_row][pivot_col_var-1]
                    if pivot_cell > 0:
                        blocked_cols.append(pivot_col_var)
                        j += 1
                    else:
                        self.problem.basic_vars[pivot_row] = pivot_col_var
                        self.problem.update_feasible_status(True)
                        return self.problem
                else:
                    continue
            blocked_rows.append(pivot_row)
        # print("\nNo further feasible solution")
        self.__set_infeasible_status()
        return self.problem
