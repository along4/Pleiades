import sys

sys.path.append('../libs') 
import sammyInput as samin


def main():
    # Create card instances
    card1 = samin.InputFile.Card1("Sample Fortran Input Title")
    card2 = samin.InputFile.Card2("Oxygen", 15.9994, 0.1, 100.0, 100, 5, 2, 3, 2, 1, 0, 2, 1, 0)

    # Use the InputFile method to generate the input file
    inputFile = samin.InputFile()
    inputFile.write_to_file("inputExample.txt", card1, card2)

if __name__ == "__main__":
    main()
