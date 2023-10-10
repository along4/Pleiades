import argparse, sys
import matplotlib.pyplot as plt
import numpy as np
import pleiades.simData as psd

def main(config_file='config.ini', energy_min=1, energy_max=100, energy_points=10000):
    
    # Read the isotope config file
    info = psd.Isotopes(config_file)
    
    # Generate a linear energy grid
    energy_grid = np.linspace(energy_min, energy_max, energy_points)
    
    fig, ax = plt.subplots(2,1)
    
    for isotope in info.isotopes:
        
        energies, cross_sections = zip(*isotope.xs_data)
        ax[0].set_xlim(energy_min, energy_max)
        ax[0].loglog(energies, cross_sections, label=isotope.name)
        
        # Generate transmission data
        transmission_data = psd.create_transmission(energy_grid,isotope)
        grid_energies, interp_transmission = zip(*transmission_data)
        ax[1].semilogx(grid_energies, interp_transmission, label=isotope.name)
    
    plt.legend()
    plt.show()
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process config file for isotopes and plot transmission.')
    parser.add_argument('--config', type=str, default='config.ini', help='Path to the config file')
    parser.add_argument('--energy_min', type=float, default=1, help='Minimum energy for the plot [eV]')
    parser.add_argument('--energy_max', type=float, default=100, help='Maximum energy for the plot [eV]')
    parser.add_argument('--energy_points', type=int, default=100000, help='Number of energy points for the plot')
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    else:
        args = parser.parse_args()
        main(args.config, args.energy_min, args.energy_max, args.energy_points)
    
