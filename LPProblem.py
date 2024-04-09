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

    def __get_n_slack_vars(self):
        """
        Class method to calculate the number of slack variables used for the problem (S1, S2, etc..)
        """
        return len(self.matrix[0][:-1]) - self.n_decision_vars - self.n_artificials
