# Copyright 2024-2025 Navindu De Silva
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod
import json
import os
import shutil
from sympy import Symbol
import yaml

from elpee.datahandler import json_handler, yaml_handler
from elpee.utils.printer import SimplexPrinter
from elpee.utils.protocols.st_problem import StandardProblem

M = Symbol('M')

class DataHandler(ABC):
    """
    An abstract class for reading & writing LP problem configurations files

    Subclasses
    ----------
    JsonHandler
        For handling and saving solution steps from LP problems in JSON format
    YamlHandler 
        For handling and saving solution steps from LP problems in YAML format

    Attributes
    ---------
    create_json : string (default : None)
        Configures the frequency of saving the iterations of the LP solution generation
        Options allowed are [`"all"`, `"final"`, `None`]    
    """

    def __init__(self, freq : str = None) -> None:
        if freq not in ["all", "final", None]:
            raise ValueError(f"{freq} is an invalid argument for freq parameter.") 

        self.create_json = freq
        
        # create the folder to store json file solutions
        if (freq == "all") | (freq == "final"):
            self.__create_solution_folder()

    def __create_solution_folder(self):
        """
        Creates a folder in root to store the LP solutions into files
        """

        # If the folder exists, delete it and its contents
        solution_folder_path = "solution"

        if os.path.exists(solution_folder_path):
            shutil.rmtree(solution_folder_path)
        # Create a new, empty folder
        os.makedirs(solution_folder_path)

def __check_file_type(file_path: str):
    """
    Check if the file type given is a yaml or json file
    """

    with open(file_path, 'r') as file:
        first_char = file.read(1).strip()
        file.seek(0)
        
        if first_char in ('{', '['):
            # Try parsing as JSON
            try:
                json.load(file)
                return "JSON"
            except json.JSONDecodeError as e:
                return e
        else:
            # Try parsing as YAML
            try:
                yaml.safe_load(file)
                return "YAML"
            except yaml.YAMLError as e:
                return e

def read_file(file_path: str) -> StandardProblem:
    """
    Read the standardized problem configuration from the json/yaml file

    Parameters
    ----------
    file_path : str
        File path to the file containing LP problem to be read   

    Returns
    -------
    StandardProblem object of the LP problem in the file
    """

    file_type = __check_file_type(file_path)
    config = None
    if file_type == "json":
        return json_handler.read_json(file_path)
    elif file_type == "yaml":
        return yaml_handler.read_yaml(file_path)
    else:
        raise ValueError("Incorrect File Type received. File should be json or yaml type")

def save_file(problem: StandardProblem, file_format: str, file_path:str):
    """
    Save the standardized problem configurations to specified file format 

    Parameters
    ----------
    problem : StandardProblem
        Standardized LP problem to be saved into yaml file
    file_format : string (Options: ["json", "yaml"])
        Specifies file type used for saving solution 
    yaml_path : string
        File path of yaml file to be written 
    """
    if file_format == "json":
        json_handler.write_json(problem, file_path)
    elif file_path == "yaml":
        yaml_handler.write_yaml(problem, file_path)
    else:
        raise ValueError("Incorrect File Type received. File should be json or yaml type")


def print_lp_problem(file_path: str, show_interpreter: bool=True):
    """
    A function to print the StandardProblem from the file to command terminal

    Parameters
    ----------
    file_path : str
        File path to the solution file containing LP problem to be read   
    show_interpreter : bool (default = True)
        Provides interpretation of values in simplex table when True
    """
    problem = read_file(file_path)

    printer = SimplexPrinter(show_interpret=show_interpreter)
    printer.print_simplex_table_cli(problem)