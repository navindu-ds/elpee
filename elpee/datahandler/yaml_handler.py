# Copyright 2024-2025 Navindu De Silva
# SPDX-License-Identifier: Apache-2.0

import os
import shutil
from typing import Any
from sympy import Symbol
import yaml

from elpee.utils.printer import SimplexPrinter
from elpee.utils.protocols.st_problem import StandardProblem
from elpee.utils.utilities import convert_M_to_sympy, convert_sympy_to_text, get_basic_vars_names, get_column_list

M = Symbol('M')
        
# TODO part of the refactor of handlers

def read_yaml(yaml_path: str) -> StandardProblem:
    """
    Read the standardized problem configuration from the yaml file

    Parameters
    ----------
    yaml_path : str
        File path to the yaml file containing LP problem to be read   

    Returns
    -------
    StandardProblem object of the LP problem in the yaml file
    """
        
    # Load config from YAML file
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)

    variable_names = __read_optional_configs(config, "variable_names", None)

    # Access the values and create a new StandardProblem
    st_problem = StandardProblem(
        matrix=convert_M_to_sympy(config['matrix']),
        basic_vars=config['basic_vars'],
        n_decision_vars=config['n_decision_vars'],
        n_artificials=config['n_artificials'],
        is_max=config['is_max'],
        var_name_list=variable_names
    )

    is_feasible = __read_optional_configs(config, "feasibility", True)    
    st_problem.update_feasible_status(is_feasible)

    is_optimal = __read_optional_configs(config, "optimal_status", False)
    st_problem.update_optimal_status(is_optimal)

    can_reach_optimal = __read_optional_configs(config, "reachability_of_optimal", True)
    st_problem.update_optimal_reachability_status(can_reach_optimal)

    n_alternates = __read_optional_configs(config, "n_alternates", 0)
    st_problem.set_num_alternates(n_alternates)

    return st_problem

def __read_optional_configs(config: Any, property: str, default_value: Any):
    """
    Function to read values from the yaml file if existing  
    """
    try:
        value = config[property]
    except KeyError:
        value = default_value
    return value


def write_yaml(problem:StandardProblem, yaml_path:str):
    """
    Save the standardized problem configurations to yaml file 

    Parameters
    ----------
    problem : StandardProblem
        Standardized LP problem to be saved into yaml file
    yaml_path : string
        File path of yaml file to be written 
    """

    data = {
        "matrix": convert_sympy_to_text(problem.matrix),
        "basic_vars": problem.basic_vars,
        "basic_vars_names": get_basic_vars_names(problem),
        "matrix_columns": get_column_list(problem),
        "n_decision_vars": problem.n_decision_vars,
        "n_artificials": problem.n_artificials,
        "is_max": problem.is_max,
        "variable_names": problem.var_name_list,
        "feasibility": problem.is_feasible,
        "optimal_status": problem.is_optimal,
        "reachability_of_optimal": problem.is_optimal_reachable,
        "n_alternates": problem.num_alternates
    }

    # Save data to YAML file
    with open(yaml_path, 'w') as file:
        yaml.dump(data, file)

def print_lp_problem_from_yaml(yaml_path:str, show_interpreter: bool=True) -> None:
    """
    A function to print the StandardProblem from the yaml to command terminal

    Parameters
    ----------
    yaml_path : str
        File path to the yaml file containing LP problem to be read   
    show_interpreter : bool (default = True)
        Provides interpretation of values in simplex table when True
    """

    problem = read_yaml(yaml_path)

    printer = SimplexPrinter(show_interpret=show_interpreter)
    printer.print_simplex_table_cli(problem)