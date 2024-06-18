.. image:: assets/ElpeeBanner.png
   :alt: Elpee Logo
   :width: 200px
   :align: right

==================
elpee.json_handler
==================

.. note::

   The functionalities of this module are moved to the `elpee.data_handler` module. Check :doc:`data_handler` for its implementation.

A module for reading & writing LP problem configurations with json files.

Import
------

.. code-block:: python

    from elpee import json_handler


Methods
-------

.. data:: read_json(json_path: str) -> StandardProblem

Read the standardized problem configuration from the json file
  
**Parameters**

    - json_path : `str`
        File path to the json file containing LP problem to be read   

**Return**

    `elpee.StandardProblem` object of the LP problem in the json file

**Example Code**

.. code-block:: python

    from elpee import json_handler

    json_handler.read_json("file/path/to/elpee/problem.json")



.. data:: write_json(problem:StandardProblem, json_path:str)

Save the standardized problem configurations to json file 

**Parameters**

    - problem : `elpee.StandardProblem`
        Standardized LP problem to be saved into json file
    - json_path : `str`
        File path of json file to be written 

**Example Code**

.. code-block:: python

    from elpee import json_handler

    # let lp_solution be the solution obtained from an elpee problem

    json_handler.write(lp_solution, "file/path/to/save/solution.json")



.. data:: print_lp_problem_from_json(json_path:str, show_interpreter: bool=True)

A function to print the `elpee.StandardProblem` from the json

**Parameters**

    - json_path : `str`
        File path to the json file containing LP problem to be read   
    - show_interpreter : `bool` (default = `True`)
        Provides interpretation of values in simplex table when True
    
**Example Code**

.. code-block:: python

    from elpee import json_handler

    # let lp_solution be the solution obtained from an elpee problem

    json_handler.print_lp_problem_from_json("file/path/to/save/solution.json")
