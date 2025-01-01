# Copyright 2024-2025 Navindu De Silva
# SPDX-License-Identifier: Apache-2.0

from typing import Literal
import yaml
from pathlib import Path
CONFIG_FILE = Path(__file__).parent / "configs.yaml"

DEFAULT_DECIMAL_SIZE = 2
DEFAULT_CELL_WIDTH = 13

def load_config():
    """
    Load configuration settings

    Return
    ------
    A dictionary with configuration settings
    """
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Configuration file not found at {CONFIG_FILE}")
    with open(CONFIG_FILE, "r") as file:
        return yaml.safe_load(file)

def set_config_values(setting_name: Literal["DECIMALS", "WIDTH"], new_value : int):
    """
    Update the configuration values to `new_value` for the `setting_name`

    Parameters
    ----------
    setting_name : `str`
        Name of the configuration setting to be updated
    new_value : `int`
        New value to be updated
    """
    config = load_config()
    config[setting_name] = new_value
    with open(CONFIG_FILE, "w") as file:
        yaml.safe_dump(config, file)

def set_decimal_size(num_decimals: int = DEFAULT_DECIMAL_SIZE):
    """
    Set the max number of decimal places to display for solutions as
    a configuration

    Parameters
    ----------
    num_decimals : `int`
        The max number of decimal places to display. If no input, sets 
        to default value `num_decimals`=2 
    """
    set_config_values("DECIMALS", num_decimals)

def set_cell_width(char_width_size: int = DEFAULT_CELL_WIDTH):
    """
    Set the width size of a cell in the simplex table displayed on the 
    command terminal

    Parameters
    ----------
    char_width_size : `int`
        width size of a cell in the simplex table displayed in character 
        spaces. If no input, sets to default value to `char_width_size`=13 
    """
    set_config_values("WIDTH", char_width_size)