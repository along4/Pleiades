Usage
=====

.. _installation:

Installation
------------

Currently, PLEIADES is not a python package, so you need to install it manually.

This can be done by cloning the repository and then copying the following in your ``.bashrc`` file:

.. code-block:: console

   export PYTHONPATH=$PYTHONPATH:[/PATH/TO/PLEIADES/DIR]

Make sure to source your ``.bashrc`` or ``.zshrc`` file after exporting the ``PYTHONPATH`` variable.

Once this is done, you can import the package in your python scripts:

.. code-block:: console

   import pleiades

Or you can import specific pleiades modules in your python scripts:

.. code-block:: console
   import pleiades.sammyInput as psi      # Module for creating SAMMY input files. 
   import pleiades.nucData as pnd         # Module for handling nuclear data.