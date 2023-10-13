Examples
========

Here are several examples illustrating the use of several utilities within the PLEIADES package.

Example 1: Simulating a neutron transmission spectrum
-----------------------------------------------------
Simulating a neutron transmission spectrum using the pleiades.simulate module

This example is located in the examples directory under ```examples/plotTransmission/```

It has the following files:

* ```plotTrans.py```: A python script that uses the pleiades.simulate module to simulate a neutron transmission spectrum
* ```isotope.ini``` : A configuration file that contains the isotopic information needed to simulate the neutron transmission spectrum

The isotope.ini file contains the following information:
.. code-block:: ini

    [Isotope1]
    name = U-238
    thickness = 0.01
    thickness_unit = cm
    abundance = 0.99
    xs_file_location = ../../nucDataLibs/xSections/u-n.tot
    density = 19.1
    density_unit = g/cm3
    ignore = false
    
Example 2: SAMMY input files
----------------------------
Making a SAMMY input file with the pleiades.sammyInput module

This example is located in the examples directory under ```examples/makeSammyInput/```

It has the following files:

* ```makeInputFile.py```: A python script that uses the pleiades.sammyInput module to create a SAMMY input file
* ```config.ini``` : A configuration file that contains the information needed to create the SAMMY input file
