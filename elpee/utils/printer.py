from elpee.utils.protocols.st_problem import StandardProblem
from elpee.utils.utilities import convert_num_to_padded_text

WIDTH = 13
DECIMALS = 3

class SimplexPrinter():
    """
    Class Description for all functions for printing the contents of the LP Problem sent
    """
    def __init__(self):
        pass

    def print_var_name(self, var_num, problem: StandardProblem):
        """
        Prints the variable name as Decision, Slack or Artificial variable using the general index of the variable
        """
        var_idx = var_num
        if var_idx <= problem.n_decision_vars:
            return f"X{var_num}"
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

    def __get_var_list(self, n_decision_vars, n_slack_vars, n_artificials):
        """
        Creates names of variables used in the problem
        Creates the list of variables including objective, decision, slack and artificial variables
        """
        var_names = ['P'.center(WIDTH)]
        for i in range(n_decision_vars):
            var_names.append(("X"+str(i+1)).center(WIDTH))
        for i in range(n_slack_vars):
            var_names.append(("S"+str(i+1)).center(WIDTH))
        for i in range(n_artificials):
            var_names.append(("A"+str(i+1)).center(WIDTH))
        var_names.append("Sol".center(WIDTH))
        return var_names
    
    def __get_simplex_table_text(self, problem: StandardProblem):
        """
        Creates a list of text strings to display contents of the simplex table
        """
        var_names = self.__get_var_list(problem.n_decision_vars, problem.n_slack_vars, problem.n_artificials)

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
    
    def print_simplex_table_cli(self, problem:StandardProblem):
        """
        Prints the simplex table onto the command line interface
        """
        rows_list = self.__get_simplex_table_text(problem)
        for row in rows_list:
            print(row)