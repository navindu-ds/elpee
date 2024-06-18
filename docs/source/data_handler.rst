.. image:: assets/ElpeeBanner.png
   :alt: Elpee Logo
   :width: 200px
   :align: right

==================
elpee.data_handler
==================

A generalized module for reading & writing LP problem configurations into json or yaml files.

Import
------

.. code-block:: python

    from elpee import data_handler


Methods
-------

.. data:: read_file(file_path: str) -> StandardProblem

Read the standardized problem configuration from the given file path
  
**Parameters**

    - file_path : `str`
        File path to the file containing LP problem to be read   

**Return**

    `elpee.StandardProblem` object of the LP problem in the file

**Example Code**

.. code-block:: python

    from elpee import data_handler

    # reading from a json file
    data_handler.read_file("file/path/to/elpee/problem.json")

    # reading from a yaml file
    data_handler.read_file("file/path/to/elpee/problem.yaml")



.. data:: save_file(problem:StandardProblem, file_format: str, file_path:str)

Save the standardized problem configurations to specified file format 

**Parameters**

    - problem : `elpee.StandardProblem`
        Standardized LP problem to be saved into file
    - file_format : `str` (Options: ["json", "yaml"])
        Specifies file type used for saving solution 
    - file_path : `str`
        File path of file to be saved 

**Example Code**

.. code-block:: python

    from elpee import data_handler

    # let lp_solution be the solution obtained from an elpee problem to be saved to a json file

    data_handler.save_file(lp_solution, file_format="json", file_path="file/path/to/save/solution.json")



.. data:: print_lp_problem(file_path:str, show_interpreter: bool=True)

A function to print the `elpee.StandardProblem` from the file

**Parameters**

    - file_path : `str`
        File path to the file containing LP problem to be read   
    - show_interpreter : `bool` (default = `True`)
        Provides interpretation of values in simplex table when True
    
**Example Code**

.. code-block:: python

    from elpee import data_handler

    # let lp_solution be the solution obtained from an elpee problem from a yaml file

    data_handler.print_lp_problem("file/path/to/save/solution.yaml")
