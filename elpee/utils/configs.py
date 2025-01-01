# Copyright 2024-2025 Navindu De Silva
# SPDX-License-Identifier: Apache-2.0

import yaml
import importlib.resources

package_name = "elpee"
config_file_name = "configs.yaml"
DEFAULT_DECIMAL_SIZE = 2
DEFAULT_CELL_WIDTH = 13

def load_config():
    """
    Load configuration settings

    Return
    ------
    A dictionary with configuration settings
    """
    with importlib.resources.open_text(package_name, config_file_name) as file:
        config = yaml.safe_load(file)
    return config

def set_config_values(setting_name: str, new_value : int):
    """
    Update the configuration values to `new_value` for the `setting_name`

    Parameters
    ----------
    setting_name : `str`
        Name of the configuration setting to be updated
    new_value : `int`
        New value to be updated
    """
    # Load the existing config
    with importlib.resources.open_text(package_name, config_file_name) as file:
        config = yaml.safe_load(file)
    
    # Update the DECIMALS value
    config['settings'][setting_name] = new_value
    
    # Write the updated config back to the file
    with importlib.resources.path(package_name, config_file_name) as file_path:
        with open(file_path, 'w') as file:
            yaml.safe_dump(config, file)
        

def set_decimal_size(num_decimals: int = DEFAULT_DECIMAL_SIZE):
    """
    Set the max number of decimal places to display for solutions as a configuration

    Parameters
    ----------
    num_decimals : `int`
        The max number of decimal places to display. If no input, sets to default value `num_decimals`=2 
    """
    set_config_values("DECIMALS", num_decimals)

def set_cell_width(char_width_size: int = DEFAULT_CELL_WIDTH):
    """
    Set the width size of a cell in the simplex table displayed on the command terminal

    Parameters
    ----------
    char_width_size : `int`
        width size of a cell in the simplex table displayed in character spaces. If no input, sets to default value to `char_width_size`=13 
    """
    set_config_values("WIDTH", char_width_size)