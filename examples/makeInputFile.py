import sys

sys.path.append('../libs') 
import sammyInput as samin

def main(config_file=None):
    
    # Use the InputFile method to generate the input file
    inputFile = samin.InputFile()

    # Read cards from config file
    if config_file != None:
        card1 = inputFile.Card1(config_file)
        card2 = inputFile.Card2(config_file)
    # Otherwise, use default values
    else:
        card1 = inputFile.Card1()
        card2 = inputFile.Card2()
        
    # Write cards to input file
    inputFile.write_to_file("inputExample.txt", card1, card2)

if __name__ == "__main__":

    main(sys.argv[1] if len(sys.argv) > 1 else None)
