import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def process_and_plot_lst_file(filename, residual=False, quantity='cross-section'):
    """
    Reads an LST file, determines the number of columns, processes the data based on plot_type, and plots the data.

    Args:
        filename (str): The path to the LST file.
        plot_type (str): Type of plot. Options: 'cross-section', 'Transmission'
    """
    # Read the file into a DataFrame. The separator is whitespace, and the file may not have headers.
    data = pd.read_csv(filename, sep="\s+", header=None)
    
    num_columns = data.shape[1]
    print(f"Number of columns in the file: {num_columns}")
    
    if quantity == 'cross-section' and num_columns >= 5:
        plot_cross_section(data, residual=residual)
        
    elif quantity == 'Transmission' and num_columns >= 10:
        plot_transmission(data, residual=residual)
    
    
def plot_cross_section(data, residual=False):
    """
    Plots the cross section data from the LST file.

    Args:
        data (DataFrame): The DataFrame containing the LST file data.
        residual (bool): If True, the difference between the theoretical and experimental cross sections will be plotted.
    """
    energy = data.iloc[:, 0]
    exp_cs = data.iloc[:, 2]
    theo_cs_initial = data.iloc[:, 4]
    theo_cs_final = data.iloc[:, 5]
    
    if residual:
        diff_initial = exp_cs - theo_cs_initial
        diff_final = exp_cs - theo_cs_final 
        
        fig, ax = plt.subplots(2,2, sharey=False,figsize=(8,6),gridspec_kw={"width_ratios":[5,1], "height_ratios":[5,2]})
        ax = np.ravel(ax)
        ax[0].plot(energy, exp_cs, label='Experimental Cross Section', marker='o', linestyle='-')
        ax[0].plot(energy, theo_cs_initial, label='Theoretical Cross Section (Initial)', marker='x', linestyle='--')
        ax[0].plot(energy, theo_cs_final, label='Theoretical Cross Section (Final)', marker='x', linestyle='--')
        ax[0].set_ylabel('Cross Section (barns)')
        ax[0].legend()
        
        plt.plot(energy, diff, label='Difference', marker='o', linestyle='-')
        plt.ylabel('Difference (barns)')
        
    else:
        fig, ax = plt.subplots(1,1, figsize=(6,6))
        ax.plot(energy, exp_cs, label='Experimental Cross Section', marker='o', linestyle='-')
        ax.plot(energy, theo_cs_initial, label='Theoretical Cross Section (Initial)', marker='x', linestyle='--')
        ax.plot(energy, theo_cs_final, label='Theoretical Cross Section (Final)', marker='x', linestyle='--')
        ax.set_ylabel('Cross Section (barns)')
        ax.legend()
        plt.show()
    
        
def plot_transmission(data, residual=False):
    """
    Plots the transmission data from the LST file.

    Args:
        data (DataFrame): The DataFrame containing the LST file data.
        residual (bool): If True, the difference between the theoretical and experimental transmission will be plotted.
    """
    energy = data.iloc[:,0]
    exp_trans = data.iloc[:,6]
    theo_trans_initial = data.iloc[:,8]
    theo_tran_final = data.iloc[:,9]
    
    if residual:
        diff_initial = exp_trans - theo_trans_initial
        diff_final = exp_trans - theo_tran_final

def read_data(filename):
    # Load the data
    data = np.loadtxt(filename, delimiter=' ', skiprows=1)  # Assuming space delimited and one header row

    # Check number of columns
    num_cols = data.shape[1]
    if num_cols != 13:
        raise ValueError("Incorrect number of columns. Expected 13 but got {}".format(num_cols))
    
    return data

def plot_data(data):
    # Extract necessary columns
    energy = data[:, 0]
    experimental_cross_section = data[:, 1]
    final_theoretical_cross_section = data[:, 4]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(energy, experimental_cross_section, label='Experimental Cross Section', marker='o', linestyle='-')
    plt.plot(energy, final_theoretical_cross_section, label='SAMMY Cross Section', marker='x', linestyle='--')

    plt.xlabel('Energy')
    plt.ylabel('Cross Section (barns)')
    plt.title('Experimental vs. Final Theoretical Cross Section')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    filename = input("Enter the filename: ")
    data = read_data(filename)
    plot_data(data)
