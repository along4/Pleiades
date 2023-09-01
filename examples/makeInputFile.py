import sys

sys.path.append('../libs') 
import sammyInput as samin


def main():
    # Create card instances
    card1 = samin.Input.Card1("Sample Fortran Input Title")
    card2 = samin.Input.Card2("Oxygen", 15.9994, 0.1, 100.0, 100, 5, 2, 3, 2, 1, 1234567890, 2, 1, 123456)

    # Generate Fortran input file
    with open("fortran_input.txt", 'w') as f:
        f.write(str(card1) + "\n")
        f.write(str(card2) + "\n")

if __name__ == "__main__":
    main()