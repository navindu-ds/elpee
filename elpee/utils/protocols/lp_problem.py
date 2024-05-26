import re
from elpee.utils.protocols.st_problem import StandardProblem


class LPProblem():
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
    """
    
    def __init__(self, is_maximization: bool = True, objective_expr: str=None) -> None:
        self._objective =  objective_expr
        self._standard_objective = {}
        self._constraints = []
        self._standard_constraints = []
        self._variables = []
        self._use_dual_simplex = False
        self.is_max = is_maximization

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

    def standardize_problem(self) -> StandardProblem:

        pass