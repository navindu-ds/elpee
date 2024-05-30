import re
from typing import Dict, List

from sympy import Symbol
from elpee.utils.protocols.st_problem import StandardProblem
from elpee.utils.utilities import convert_gte_to_lte, obtain_coefficient_from_dict, transform_to_positive_constraints


class LinearProblem():
    """
    Class to represent the linear programming optimization problem
    with its objective function, constraints and other conditions

    Methods
    -------
    add_objective(objective_expr:str)
        Defines the new objective function expression for the LP problem
    add_constraint(constraint_expr:str)
        Defines a new constraint to be added to the LP problem
    use_dual_simplex()
        Configures the problem to be solved using Dual Simplex method
    use_bigM()
        Configures the problem to be solved using big M method
    standardize_problem() -> StandardProblem
        Converts the LinearProblem into standardized form for computation 
    """
    
    def __init__(self, is_maximization: bool = True, objective_expr: str=None) -> None:
        self._objective =  objective_expr
        self._standard_objective = {}
        self._constraints = []
        self._standard_constraints = []
        self._variables = []
        self._use_dual_simplex = False
        self.is_max = is_maximization
        self._n_slack_vars = 0
        self._n_artificials = 0
        self._basic_vars = []

    def add_objective(self, objective_expr: str) -> None:
        """
        Define the objective function expression into the linear 
        programming problem. Replaces previous objective function.

        Parameters
        ----------
        objective_expr : str
            String expression of the objective function of LP Problem 

        Exceptions
        ----------
        ValueError is thrown when objective function expression is not
        valid
        """
        
        self.__check_objective(objective_expr)
        self._objective = objective_expr
        self.__standardize_objective()
        self.__update_variable_list_with_objective()

    
    def add_constraint(self, constraint_expr: str) -> None:
        """
        Add a new constraint to existing LP Problem.

        Parameters
        ----------
        constraint_expr : str
            String expression of a mathematical inequality of equality 
            to represent as a new constraint
        
        Exceptions
        ----------
        ValueError is thrown when constraint expression is not valid
        """

        self.__check_constraint(constraint_expr)
        self._constraints.append(constraint_expr)
        self.__generate_standard_constraint_list()
        self.__update_variable_list_with_constraint()

    def use_dual_simplex(self):
        """
        Configures the LP problem to be solved using Dual Simplex method
        """
        
        self._use_dual_simplex = True
    
    def use_bigM(self):
        """
        Configures the LP problem to be solved using big M method
        """

        self._use_dual_simplex = False

    def __standardize_objective(self) -> None:
        """
        Standardizes the objective function for computation
        """

        self._standard_objective = {}
        obj_expr = self._objective.strip()
        matches = re.finditer(r'([+-]?\s*\d*\.?\d*)\s*\*?\s*([a-zA-Z]\w*)', obj_expr)
        for match in matches:
            coefficient = match.group(1).replace(' ', '')
            variable = match.group(2)
            
            # Convert coefficient to float
            coefficient = float(coefficient) if coefficient not in ('', '+', '-') else 1.0 * (-1 if coefficient == '-' else 1)
            self._standard_objective[variable] = coefficient

    def __check_objective(self, obj_expr:str) -> None:
        """
        Verifies the objective function expression. Throws a ValueError 
        if the objective function is not valid.
        """

        symbols = ['<=', '>=','=','>','<']
        occurrences = {symbol: obj_expr.count(symbol) for symbol in symbols}
        total_occurrences = sum(occurrences.values())
        if total_occurrences > 0:
            raise ValueError("Objective Function cannot have equality or inequality operators") 

    def __check_constraint(self, constraint_expr: str) -> None:
        """
        Verifies the constraint expression. Throws a ValueError 
        if the constraint is not valid.
        """

        symbols = ['<=', '>=','=','>','<']
        occurrences = {symbol: constraint_expr.count(symbol) for symbol in symbols}
        total_occurrences = sum(occurrences.values())
        if total_occurrences > 1:
            total_occurrences = occurrences['<=']*occurrences['=']*occurrences['<'] + occurrences['>=']*occurrences['=']*occurrences['>']
        if total_occurrences != 1:
            raise ValueError("The constraint must contain exactly one equality or inequality operator")
        
    def __generate_standard_constraint_list(self):
        """
        Generates the standardized constraint list for computation
        """

        self._standard_constraints = []
        for constraint in self._constraints:
            # Determine the type of inequality or equation
            if '<=' in constraint:
                inequality = '<='
            elif '>=' in constraint:
                inequality = '>='
            elif '=' in constraint:
                inequality = '='
            elif '<' in constraint:
                inequality = '<'
            elif '>' in constraint:
                inequality = '>'
            
            # Split the expression into the left-hand side and the right-hand side
            lhs, rhs = re.split(f'{inequality}', constraint)
            lhs = lhs.strip()
            rhs = float(rhs.strip())

            # Initialize the result dictionary
            result = {inequality: {}}
            
            # Find all the coefficients and variables
            matches = re.finditer(r'([+-]?\s*\d*\.?\d*)\s*\*?\s*([a-zA-Z]\w*)', lhs)

            for match in matches:
                coefficient = match.group(1).replace(' ', '')
                variable = match.group(2)
                
                # Convert coefficient to float
                coefficient = float(coefficient) if coefficient not in ('', '+', '-') else 1.0 * (-1 if coefficient == '-' else 1)
                
                # Add the variable and its coefficient to the dictionary
                result[inequality][variable] = coefficient
            
            # Add the right-hand side value
            result[inequality]['sol'] = rhs

            if inequality == '<':
                coefficient_dict = result[inequality]
                for key, value in coefficient_dict.items():
                    coefficient_dict[key] = -value
                result = {'>=':coefficient_dict}
            elif inequality == '>':
                coefficient_dict = result[inequality]
                for key, value in coefficient_dict.items():
                    coefficient_dict[key] = -value
                result = {'<=':coefficient_dict}

            self._standard_constraints.append(result)

    def __update_variable_list_with_constraint(self):
        """
        Updates the list of variables used in the Linear Programming Problem
        after new constraint is added
        """

        unique_vars = set(self._variables)
        for _, variables in self._standard_constraints[-1].items():
            for var in variables:
                if var != 'sol':
                    unique_vars.add(var)
        self._variables = sorted(list(unique_vars))

    def __update_variable_list_with_objective(self):
        """
        Updates the list of variables used in the Linear Programming Problem
        after objective is added
        """

        unique_vars = set(self._variables)
        for var in self._standard_objective:
            unique_vars.add(var)
        self._variables = sorted(list(unique_vars))

    def __create_objective_row_from_lp(self) -> List:
        """
        Generates the contents of the objective row to be added to simplex matrix
        """
        
        obj_row = []
        # adding the coefficients of the variables in the objective function
        for var in self._variables:
            obj_coefficient = -obtain_coefficient_from_dict(self._standard_objective, var)
            obj_row.append(obj_coefficient)

        # adding the values for the slack variable columns
        for _ in range(self._n_slack_vars):
            obj_row.append(0)

        M = Symbol('M')

        # adding the big M values to the artificial variable columns
        for _ in range(self._n_artificials):
            if self.is_max:
                # if maximization problem, set value as 1*M
                sign = 1
            else:
                # if minimization problem, set value as (-1*M)
                sign = -1
            obj_row.append(sign*M)
        
        # add initial solution value of 0
        obj_row.append(0)

        # add basic variable for objective
        self._basic_vars.append(0)

        # return objective row
        return obj_row
    
    def __create_constraint_row_from_lp(self, constraint : Dict, constraint_id : int) -> List:
        """
        Generates the contents of the given constraint row to be added to simplex matrix
        """

        row_list = []
        operator = next(iter(constraint)) # operator of type >=, <= or =
        coefficient_dict = constraint[operator] # dictionary of decision variables and coefficients

        # counter for adding the basic var id
        var_count = 1

        # adding the coefficients of each decision variable
        for var in self._variables:
            coeff_var = obtain_coefficient_from_dict(coefficient_dict, var)
            row_list.append(coeff_var)
            var_count += 1

        # marking the relevant slack variable for each constraint based on constraint id
        for i in range(self._n_slack_vars):
            if i == constraint_id:
                if operator == '<=':
                    row_list.append(1)

                    # add basic variable id for slack variable
                    self._basic_vars.append(var_count)
                elif operator == '>=':
                    row_list.append(-1)
            else:
                row_list.append(0)
            var_count += 1
        
        # marking the relevant artificial variable for constraints with >= or =
        for j in range(self._n_artificials):
            if operator in ['>=', '=']:
                if j == self._artificial_count:
                    row_list.append(1)

                    # add basic variable id for artificial variable
                    self._basic_vars.append(var_count)
                    
                    self._artificial_count += 1
                    for _ in range(self._n_artificials - self._artificial_count):
                        row_list.append(0)
                    
                    break
                else:
                    row_list.append(0)

            else:
                row_list.append(0)
            var_count += 1

        # add the RHS value of each constraint
        row_list.append(coefficient_dict['sol'])
        
        # return the constraint row to add to simplex matrix
        return row_list

    def standardize_problem(self) -> StandardProblem:
        """
        Convert the given Linear Programming problem into a Standardized Linear 
        Programming Problem for computation

        Return
        ---
        StandardProblem object with LinearProblem converted for computation
        """
        
        # calculating number of slack variables required
        slack_var_operators = ['>=', '<=']
        self._n_slack_vars = 0 
        for constraint in self._standard_constraints:
            for operator in constraint:
                if operator in slack_var_operators:
                    self._n_slack_vars += 1

        # if using dual simplex, convert all >= constraints to <=
        if self._use_dual_simplex:
            self._standard_constraints = convert_gte_to_lte(self._standard_constraints)

        # if using bigM method, convert all constraints to have a positive solution / RHS value
        else:
            self._standard_constraints = transform_to_positive_constraints(self._standard_constraints)

        # calculating number of artificial variables required
        artificial_var_operators = ['=','>=']
        self._n_artificials = 0 
        for constraint in self._standard_constraints:
            for operator in constraint:
                if operator in artificial_var_operators:
                    self._n_artificials += 1

        # initialize simplex matrix
        simplex_matrix = []

        # generate objective row and add to simplex matrix
        obj_row = self.__create_objective_row_from_lp()
        simplex_matrix.append(obj_row)

        self._artificial_count = 0           # auxillary counter to mark position of each 
                                                # artificial variables in the simplex matrix
        
        # generate the constraint row to add to simplex matrix 
        for c_id, constraint in enumerate(self._standard_constraints):
            row_list = self.__create_constraint_row_from_lp(constraint, c_id)
            simplex_matrix.append(row_list)
        
        # create the Standard Problem object
        return StandardProblem(
            matrix= simplex_matrix,
            basic_vars= self._basic_vars,
            n_decision_vars= len(self._variables),
            is_max= self.is_max,
            n_artificials= self._n_artificials,
            var_name_list= self._variables
        )