# Copyright 2024-2025 Navindu De Silva
# SPDX-License-Identifier: Apache-2.0

from elpee.utils.protocols.st_problem import StandardProblem
from elpee.utils.utilities import convert_num_to_padded_text, extract_elem_from_simplex_matrix
from elpee.utils.configs import load_config

class SimplexPrinter():
    """
    Class Description for all functions for printing the contents of the LP Problem sent
    """
    def __init__(self, show_steps : bool = True, show_interpret : bool = True):
        self.show_steps = show_steps
        self.show_interpret = show_interpret

    def __print_slack_var_name(self, var_num:int, problem:StandardProblem):
        """
        Print variable name for Slack variables for interpretation
        """
        var_idx = var_num
        var_idx -= problem.n_decision_vars
        if var_idx <= problem.n_slack_vars:
            return f"Constraint #{var_idx} Surplus"
        return "Unknown"

    def print_var_name(self, var_num:int, problem: StandardProblem):
        """
        Prints the variable name as Decision, Slack or Artificial variable using the general index of the variable
        """
        var_idx = var_num
        if var_idx <= problem.n_decision_vars:
            return problem.var_name_list[var_idx-1]
        var_idx -= problem.n_decision_vars
        if var_idx <= problem.n_slack_vars:
            return f"S{var_idx}"
        var_idx -= problem.n_slack_vars
        if var_idx <= problem.n_artificials:
            return f"A{var_idx}"
        return "Unknown"
    
    def print_entering_leaving_vars(self, old_basic_vars, problem:StandardProblem):
        """
        Prints the entering and leaving variable used after each iteration of optimization or dual simplex
        by comparing the previous basic_vars list and updated basic_vars list
        If no basic variables were changed, nothing is printed.
        """
        for before_var_idx, after_var_idx in zip(old_basic_vars, problem.basic_vars):
            if before_var_idx != after_var_idx:
                leaving_var = self.print_var_name(before_var_idx, problem)
                entering_var = self.print_var_name(after_var_idx, problem)

                print(f"\nTaking {leaving_var} = 0; Entering {entering_var} as a new basic variable;")
                return  

    def __get_var_list(self, problem : StandardProblem):
        """
        Creates names of variables used in the problem
        Creates the list of variables including objective, decision, slack and artificial variables
        """
        WIDTH = load_config().get('WIDTH')

        var_names = ['P'.center(WIDTH)]
        for i in range(problem.n_decision_vars):
            var_names.append((problem.var_name_list[i]).center(WIDTH))
        for i in range(problem.n_slack_vars):
            var_names.append(("S"+str(i+1)).center(WIDTH))
        for i in range(problem.n_artificials):
            var_names.append(("A"+str(i+1)).center(WIDTH))
        var_names.append("Sol".center(WIDTH))
        return var_names
    
    def __get_simplex_table_text(self, problem: StandardProblem):
        """
        Creates a list of text strings to display contents of the simplex table
        """
        config = load_config()
        DECIMALS = config.get('DECIMALS')
        WIDTH = config.get('WIDTH')

        var_names = self.__get_var_list(problem)

        rows_list = []

        # prepare first row
        if problem.is_max:
            head_simplex_row = "MAX".center(WIDTH)
        else:
            head_simplex_row = "MIN".center(WIDTH)
        head_simplex_row += "".join(map(str, var_names[1:]))
        rows_list.append(head_simplex_row)

        # for other rows representing constraint rows
        for i in range(problem.n_constraints+1):
            simplex_row = var_names[problem.basic_vars[i]].ljust(WIDTH)
            # convert each number/element in row into padded text for printing
            matrix_row_str = convert_num_to_padded_text(problem.matrix[i], WIDTH, DECIMALS)
            simplex_row += "".join(map(str, matrix_row_str))
            rows_list.append(simplex_row)

        # return the list of rows saved as text
        return rows_list
    
    def interpret_problem(self, problem:StandardProblem):
        """
        Prints the Intepretation of the variables given by the partially/ fully solved
        LP standard problem
        """
        config = load_config()
        DECIMALS = config.get('DECIMALS')
        WIDTH = config.get('WIDTH')

        decision_variables = problem.var_name_list
        basic_vars_idx = problem.basic_vars
        matrix = problem.matrix

        objective_value = convert_num_to_padded_text([problem.matrix[0][-1]], 1, DECIMALS)
        print(f"\n{'Maximum' if problem.is_max else 'Minimum'} Value for Objective Function = {objective_value[0]}")

        print("\nValues for Decision Variables : ")
        for i, var in enumerate(decision_variables):
            if (i+1) in basic_vars_idx:
                sol_val = convert_num_to_padded_text([matrix[basic_vars_idx.index(i+1)][-1]], 1, DECIMALS)
                print(f"{str(var).center(WIDTH)} = {sol_val[0]}")
            else:
                print(f"{str(var).center(WIDTH)} = 0")
        
        print("\nSurplus & Slack variables")
        start_slack_var_idx = problem.n_decision_vars + 1
        end_slack_var_idx = start_slack_var_idx + problem.n_slack_vars -1
        num_artificials_in_basic_vars = sum(item > end_slack_var_idx for item in basic_vars_idx)
        for other_var in range(start_slack_var_idx, end_slack_var_idx+1):
            if other_var in basic_vars_idx:
                print(f"{str(self.__print_slack_var_name(other_var, problem)).center(WIDTH*2)} = {extract_elem_from_simplex_matrix(matrix, basic_vars_idx.index(other_var), -1)} units")
            else:
                if num_artificials_in_basic_vars > 0:
                    pass
                else:
                    print(f"{str(self.__print_slack_var_name(other_var, problem)).center(WIDTH*2)} : Satisfied at Boundary")

        if num_artificials_in_basic_vars > 0:
            print(f"\n There are {num_artificials_in_basic_vars} Artificial variable(s) to be handled")
        
    
    def print_simplex_table_cli(self, problem:StandardProblem):
        """
        Prints the simplex table onto the command line interface
        """
        WIDTH = load_config().get('WIDTH')

        if self.show_steps:
            rows_list = self.__get_simplex_table_text(problem)
            for row in rows_list:
                print(row)

        if self.show_interpret:
            self.interpret_problem(problem=problem)   

        if (self.show_interpret | self.show_steps):
            print("="*(len(problem.matrix[0])+1)*WIDTH)