from typing import List
from sympy import Symbol, sympify

M = Symbol('M')

class LPProblem():
    """
    Class to represent the problem description of any Linear Programming
    Optimization Problem to be solved
    """
    def __init__(self, matrix: List[List], basic_vars: List[int], n_decision_vars: int, 
                 is_max: bool = True, n_artificials: int = 0):
        self.matrix = matrix
        self.basic_vars = basic_vars
        self.n_decision_vars = n_decision_vars
        self.is_max = is_max
        self.n_artificials = n_artificials
        self.n_slack_vars = self.__get_n_slack_vars()
        self.n_constraints = self.__get_n_constraints()

    def __get_n_slack_vars(self):
        """
        Class method to calculate the number of slack variables used for the problem (S1, S2, etc..)
        """
        return len(self.obj_row) - self.n_decision_vars - self.n_artificials

    def __get_n_constraints(self):
        """
        Class method to calculate the number of constraints used for the problem
        """
        return len(self.matrix) - 1
    
    @property
    def obj_row(self):
        """
        Public class function to obtain the objective row in the matrix
        """
        return self.matrix[0][:-1]
