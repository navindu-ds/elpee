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
    file_path : string
        File path of file to be created 
    """
    if file_format == "json":
        json_handler.write_json(problem, file_path)
    elif file_format == "yaml":
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