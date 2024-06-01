# Copyright 2024-2025 Navindu De Silva
# SPDX-License-Identifier: Apache-2.0

from typing import List
from sympy import Symbol

M = Symbol('M')

class StandardProblem():
    """
    Class to represent the standardized linear programming
    pptimization Problem to be solved 
    """
    
    def __init__(self, matrix: List[List], basic_vars: List[int], n_decision_vars: int, 
                 is_max: bool = True, n_artificials: int = 0, var_name_list: List[str] = None):
        self.matrix = matrix
        self.basic_vars = basic_vars
        self.n_decision_vars = n_decision_vars
        self.is_max = is_max
        self.n_artificials = n_artificials
        self.n_slack_vars = self.__get_n_slack_vars()
        self.n_constraints = self.__get_n_constraints()
        self.var_name_list = var_name_list
        self.__is_feasible = True # default
        self.__is_optimal = False # deafult
        self.__reachable_optimal = True # default - does the LP Problem reach an optimal solution
        self.__n_alternates = 0 # default

        if self.var_name_list != None:
            # if list of variable names are provided - the number of names provided should match 
            # with number of decision variables
            if len(self.var_name_list) != self.n_decision_vars:
                raise ValueError(f"Number of variable names provided {len(self.var_name_list)} and" +
                                  f" Number of Decision Variables {self.n_decision_vars} do not match.")

        # if no variable name list is created, use a default naming of variables as X1, X2, X3, ...
        else:
            self.var_name_list = [f'X{i}' for i in range(1, self.n_decision_vars + 1)]

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
    
    def update_feasible_status(self, feasibility_status):
        """
        Class method to update the feasibility status to True/False depending on the checks
        """
        self.__is_feasible = feasibility_status

    def update_optimal_reachability_status(self, reachability_status):
        """
        Class method to update the whether the problem can reach optimal status to True/False depending on the optimization steps
        """
        self.__reachable_optimal = reachability_status

    def update_optimal_status(self, optimal_status):
        """
        Class method to update the status of problem of having reached the final optimal solution
        """
        self.__is_optimal = optimal_status

    def set_num_alternates(self, n_alternates):
        """
        Class method to update if the optimal problem has alternate optimal solutions
        """
        self.__n_alternates = n_alternates

    @property
    def is_feasible(self):
        return self.__is_feasible
    
    @property
    def is_optimal_reachable(self):
        return self.__reachable_optimal
    
    @property
    def is_optimal(self):
        return self.__is_optimal
    
    @property
    def num_alternates(self):
        return self.__n_alternates
    
    @property
    def obj_row(self):
        """
        Public class function to obtain the objective row in the matrix
        """
        return self.matrix[0][:-1]
    
    def copy(self):
        return StandardProblem(
            matrix=self.matrix.copy(),
            basic_vars=self.basic_vars.copy(),
            n_decision_vars=self.n_decision_vars,
            is_max=self.is_max,
            n_artificials=self.n_artificials
        )
    
    def __eq__(self, other: object) -> bool:
        """
        Compares between two objects in StandardProblem class for similarity
        """
        if isinstance(other, StandardProblem):
            return (self.matrix == other.matrix) & \
            (self.basic_vars == other.basic_vars) & \
            (self.n_decision_vars == other.n_decision_vars) & \
            (self.is_max == other.is_max) & \
            (self.n_artificials == other.n_artificials) & \
            (self.n_slack_vars == other.n_slack_vars) & \
            (self.n_constraints == other.n_constraints) & \
            (self.is_feasible == other.is_feasible) & \
            (self.is_optimal_reachable == other.is_optimal_reachable) & \
            (self.is_optimal == other.is_optimal) & \
            (self.num_alternates == other.num_alternates)
        return False
