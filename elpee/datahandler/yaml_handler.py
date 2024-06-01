# Copyright 2024-2025 Navindu De Silva
# SPDX-License-Identifier: Apache-2.0

from sympy import Symbol
import yaml

from elpee.utils.printer import SimplexPrinter
from elpee.utils.protocols.st_problem import StandardProblem
from elpee.utils.utilities import convert_M_to_sympy, convert_sympy_to_text

M = Symbol('M')

class YamlHandler:
    """
    A class for reading the problem configurations from a yaml file
    """

    @classmethod
    def read_yaml(self, yaml_path: str) -> StandardProblem:
        """
        Read the standardized problem configuration from the yaml file
        """
            
        # Load config from YAML file
        with open(yaml_path, 'r') as file:
            config = yaml.safe_load(file)

        # Access the values and create a new StandardProblem
        return StandardProblem(
            matrix=convert_M_to_sympy(config['matrix']),
            basic_vars=config['basic_vars'],
            n_decision_vars=config['n_decision_vars'],
            n_artificials=config['n_artificials'],
            is_max=config['is_max']
        )
    
    @classmethod
    def write_yaml(self, problem:StandardProblem, yaml_path:str):
        """
        Save the standardized problem configurations to yaml file 
        """

        data = {
            "matrix": convert_sympy_to_text(problem.matrix),
            "basic_vars": problem.basic_vars,
            "n_decision_vars": problem.n_decision_vars,
            "n_artificials": problem.n_artificials,
            "is_max": problem.is_max
        }

        # Save data to YAML file
        with open(yaml_path, 'w') as file:
            yaml.dump(data, file)

    @classmethod
    def print_lp_problem_from_yaml(self, yaml_path:str) -> None:
        """
        A function to print the StandardProblem from the yaml to command terminal
        """

        # Load config from YAML file
        with open(yaml_path, 'r') as file:
            config = yaml.safe_load(file)

        problem = StandardProblem(
            matrix=convert_M_to_sympy(config['matrix']),
            basic_vars=config['basic_vars'],
            n_decision_vars=config['n_decision_vars'],
            n_artificials=config['n_artificials'],
            is_max=config['is_max']
        )

        printer = SimplexPrinter()
        
        printer.print_simplex_table_cli(problem)
