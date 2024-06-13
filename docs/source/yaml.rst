.. image:: assets/ElpeeBanner.png
   :alt: Elpee Logo
   :width: 200px
   :align: right

==================
elpee.yaml_handler
==================

A module for reading & writing LP problem configurations with yaml files.

Import
------

.. code-block:: python

    from elpee import yaml_handler


Methods
-------

.. data:: read_yaml(yaml_path: str) -> StandardProblem

Read the standardized problem configuration from the yaml file
  
**Parameters**

    - yaml_path : `str`
        File path to the yaml file containing LP problem to be read   

**Return**

    `elpee.StandardProblem` object of the LP problem in the yaml file

**Example Code**

.. code-block:: python

    from elpee import yaml_handler

    yaml_handler.read_yaml("file/path/to/elpee/problem.yaml")



.. data:: write_yaml(problem:StandardProblem, yaml_path:str)

Save the standardized problem configurations to yaml file 

**Parameters**

    - problem : `elpee.StandardProblem`
        Standardized LP problem to be saved into yaml file
    - yaml_path : `str`
        File path of yaml file to be written 

**Example Code**

.. code-block:: python

    from elpee import yaml_handler

    # let lp_solution be the solution obtained from an elpee problem

    yaml_handler.write(lp_solution, "file/path/to/save/solution.yaml")



.. data:: print_lp_problem_from_yaml(yaml_path:str, show_interpreter: bool=True)

A function to print the `elpee.StandardProblem` from the yaml

**Parameters**

    - yaml_path : `str`
        File path to the yaml file containing LP problem to be read   
    - show_interpreter : `bool` (default = `True`)
        Provides interpretation of values in simplex table when True
    
**Example Code**

.. code-block:: python

    from elpee import yaml_handler

    # let lp_solution be the solution obtained from an elpee problem

    yaml_handler.print_lp_problem_from_yaml("file/path/to/save/solution.yaml")
