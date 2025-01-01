.. image:: assets/ElpeeBanner.png
   :alt: Elpee Logo
   :width: 200px
   :align: right

=============
elpee.configs
=============

A module for setting and loading configurations used for displaying solutions

Import
------

.. code-block:: python

    from elpee import configs


Methods
-------

.. data:: set_decimal_size(num_decimals: int = DEFAULT_DECIMAL_SIZE) -> None

Set the max number of decimal places to display for solutions as a configuration
  
**Parameters**

    - num_decimals : `int`
        The max number of decimal places to display. If no input, sets to default value `num_decimals`=2

**Example Code**

.. code-block:: python

    from elpee import configs

    configs.set_decimal_size(num_decimals = 4)



.. data:: set_cell_width(char_width_size: int = DEFAULT_CELL_WIDTH)

Set the width size of a cell in the simplex table displayed on the command terminal

**Parameters**

    - char_width_size : `int`
        width size of a cell in the simplex table displayed in character spaces. If no input, sets to default value to `char_width_size`=13

**Example Code**

.. code-block:: python

    from elpee import configs

    configs.set_cell_width(char_width_size = 15)