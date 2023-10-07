import argparse
import matplotlib.pyplot as plt
import numpy as np
import pleiades.simData as psd

def main(config_file='config.ini', energy_min=1, energy_max=10000, energy_points=1000):
    info = psd.Isotopes(config_file)
    
    # Generate an energy grid
    energy_grid = np.logspace(np.log10(energy_min), np.log10(energy_max), energy_points)
    
    plt.figure()
    
    for isotope in info.isotopes:
        # Generate transmission data
        transmission_data = psd.create_transmission(
            energy_grid, 
            isotope.xs_data, 
            isotope.thickness, 
            isotope.thickness_unit, 
            isotope.density, 
            isotope.density_unit
        )
        
        # Unpack energy and transmission values
        energies, transmissions = zip(*transmission_data)
        
        # Plot the transmission data
        plt.plot(energies, transmissions, label=isotope.name)
    
    # Add labels and title
    plt.xlabel('Energy (eV)')
    plt.ylabel('Transmission')
    plt.title('Transmission for Various Isotopes')
    plt.legend()
    
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process config file for isotopes and plot transmission.')
    parser.add_argument('--config', type=str, default='config.ini', help='Path to the config file')
    parser.add_argument('--energy_min', type=float, default=1, help='Minimum energy for the plot')
    parser.add_argument('--energy_max', type=float, default=10000, help='Maximum energy for the plot')
    parser.add_argument('--energy_points', type=int, default=1000, help='Number of energy points for the plot')
    
    args = parser.parse_args()
    main(args.config, args.energy_min, args.energy_max, args.energy_points)
