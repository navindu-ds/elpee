from abc import ABC
import os
import shutil


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
    file_format : string (default : None) 
        Specifies the file format used for saving the solutions. 
        Options allowed are [`"json"`, `"yaml"`, `None`]

    freq : string (default : None)
        Configures the frequency of saving the iterations of the LP solution generation. 
        Options allowed are [`"all"`, `"final"`, `None`]. 
        The freuency is overidden to None if the file_format is `None`. 
    """

    def __init__(self, file_format : str = None, freq : str = None) -> None:
        if file_format not in ["json", "yaml", None]:
            raise ValueError(f"{freq} is an invalid argument for file_format parameter.") 
        
        self.file_format = file_format

        if file_format == None:
            freq = None
        
        if freq not in ["all", "final", None]:
            raise ValueError(f"{freq} is an invalid argument for freq parameter.") 

        self.freq = freq

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
        super().__init__(freq=create_json, file_format="json")


class YamlHandler(DataHandler):
    """
    A class for reading & writing LP problem configurations from yaml files.

    Attributes
    ---------
    create_yaml : string (default : None)
        Configures the frequency of saving the iterations of the LP solution generation
        Options allowed are [`"all"`, `"final"`, `None`]    
    """

    def __init__(self, create_yaml: str = None) -> None:
        super().__init__(freq=create_yaml, file_format="yaml")