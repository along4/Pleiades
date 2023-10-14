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

In ```plotTrans.py```, the pleiades module, along with other needed modules, as loaded using the following code:

.. code-block:: python

    import argparse, sys            # For parsing command line arguments
    import pleiades.simulate as psd # For simulating neutron transmission spectra
    import numpy as np              # For generating energy grids

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

This file contains the information for one isotope. There can be multiple isotopes in the file where the information for each isotope is contained in separate sections, and the section names can be arbitrary, but unique. If any of the given fields are not listed, then defualt values are used. 

* ```name = U-238```: The name of the isotope, should be in the form of ```element-massNumber```
* ```thickness = 0.01``` : The thickness of the sample
* ```thickness_unit = cm```: The units of the thickness
* ```abundance = 0.99```: The abundance of the isotope. This can be used to simulate a mixture of isotopes.
* ```xs_file_location = ../../nucDataLibs/xSections/u-n.tot```: The location of the cross section file
* ```density = 19.1```: The density of the isotope
* ```density_unit = g/cm3```: The units of the density
* ```ignore = false```: A flag to ignore the isotope. If set to true, then the isotope is ignored.

To load the isotope.ini file, use the following code:

.. code-block:: python

    # Read the isotope config file
    isotope_info = psd.Isotopes(config_file)

Once loaded, the information can be accessed using the following code:

.. code-block:: python

    # Generate a linear energy grid
    energy_grid = np.linspace(energy_min, energy_max, energy_points)

    # Loop over all isotopes in isotope_info.isotopes
    for isotope in isotope_info.isotopes:
        
        # Generate transmission data
        transmission_data = psd.create_transmission(energy_grid,isotope)
        grid_energies, interp_transmission = zip(*transmission_data)

Here the main function of ```psd.create_transmission(energy_grid,isotope)``` is used to generate the transmission data. The first argument is the energy grid, and the second argument is the isotope information. The function returns a list of tuples where the first element of the tuple is the energy and the second element is the transmission. The ```zip(*transmission_data)``` function is used to unzip the list of tuples into two lists, one for the energy and one for the transmission.


Example 2: SAMMY input files
----------------------------
Making a SAMMY input file with the pleiades.sammyInput module

This example is located in the examples directory under ```examples/makeSammyInput/```

It has the following files:

* ```makeInputFile.py```: A python script that uses the pleiades.sammyInput module to create a SAMMY input file
* ```config.ini``` : A configuration file that contains the information needed to create the SAMMY input file
