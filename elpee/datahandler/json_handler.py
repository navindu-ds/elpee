# Copyright 2024-2025 Navindu De Silva
# SPDX-License-Identifier: Apache-2.0

import os
import shutil
from typing import Any
from sympy import Symbol
import json

from elpee.utils.printer import SimplexPrinter
from elpee.utils.protocols.st_problem import StandardProblem
from elpee.utils.utilities import convert_M_to_sympy, convert_sympy_to_text
from elpee.datahandler.data_handler import DataHandler

M = Symbol('M')

class JSONHandler(DataHandler):
    """
    A class for reading & writing LP problem configurations from json files.

    Attributes
    ---------
    create_json : string (default : None)
        Configures the frequency of saving the iterations of the LP solution generation
        Options allowed are [`"all"`, `"final"`, `None`]    
    """

    def __init__(self, create_json: str = None) -> None:
        super().__init__(freq=create_json)
        
        if create_json not in ["all", "final", None]:
            raise ValueError(f"{create_json} is an invalid argument for create_json parameter.") 

        self.create_json = create_json
        
        # create the folder to store json file solutions
        if (create_json == "all") | (create_json == "final"):
            self.__create_solution_folder()

    def __create_solution_folder(self):
        """
        Creates a folder in root to store the LP solutions as json files
        """

        # If the folder exists, delete it and its contents
        solution_folder_path = "solution"

        if os.path.exists(solution_folder_path):
            shutil.rmtree(solution_folder_path)
        # Create a new, empty folder
        os.makedirs(solution_folder_path)

def read_json(json_path: str) -> StandardProblem:
    """
    Read the standardized problem configuration from the json file

    Parameters
    ----------
    json_path : str
        File path to the json file containing LP problem to be read   

    Returns
    -------
    StandardProblem object of the LP problem in the json file
    """
        
    # Load config from json file
    with open(json_path, 'r') as file:
        config = json.load(file)

    variable_names = __read_optional_configs(config, "variable_names", None)

    # Access the values and create a new StandardProblem
    return StandardProblem(
        matrix=convert_M_to_sympy(config['matrix']),
        basic_vars=config['basic_vars'],
        n_decision_vars=config['n_decision_vars'],
        n_artificials=config['n_artificials'],
        is_max=config['is_max'],
        var_name_list=variable_names
    )

def __read_optional_configs(config: Any, property: str, default_value: Any):
    """
    Function to read values from the json file if existing  
    """
    try:
        value = config[property]
    except KeyError:
        value = default_value
    return value


def write_json(problem:StandardProblem, json_path:str):
    """
    Save the standardized problem configurations to json file 

    Parameters
    ----------
    problem : StandardProblem
        Standardized LP problem to be saved into json file
    json_path : string
        File path of json file to be written 
    """

    data = {
        "matrix": convert_sympy_to_text(problem.matrix),
        "basic_vars": problem.basic_vars,
        "n_decision_vars": problem.n_decision_vars,
        "n_artificials": problem.n_artificials,
        "is_max": problem.is_max,
        "variable_names": problem.var_name_list,
        "feasibility": problem.is_feasible,
        "optimal_status": problem.is_optimal,
        "reachability_of_optimal": problem.is_optimal_reachable,
        "n_alternates": problem.num_alternates
    }

    # Save data to json file
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=2)

def print_lp_problem_from_json(json_path:str, show_interpreter: bool=True) -> None:
    """
    A function to print the StandardProblem from the json to command terminal

    Parameters
    ----------
    json_path : str
        File path to the json file containing LP problem to be read   
    show_interpreter : bool (default = True)
        Provides interpretation of values in simplex table when True
    """

    problem = read_json(json_path)

    printer = SimplexPrinter(show_interpret=show_interpreter)
    printer.print_simplex_table_cli(problem)