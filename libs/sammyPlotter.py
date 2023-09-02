import numpy as np
import matplotlib.pyplot as plt

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
    plt.plot(energy, final_theoretical_cross_section, label='Final Theoretical Cross Section', marker='x', linestyle='--')

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
