import numpy as np
import sys
import pleiades.sammyInput as psi
import pleiades.nucData as pnd
import pathlib

PWD = pathlib.Path(__file__).parent # get the location of this py file

def main(config_inp_file: str="config_inp.ini"):
    
    # Use the InputFile method to generate the input file
    inputFile = psi.InputFile()

    # Read cards from config file
    if config_inp_file:
        card1 = inputFile.Card1(config_file=config_inp_file)
        card2 = inputFile.Card2(config_file=config_inp_file)
        card3 = inputFile.Card3(config_file=config_inp_file)
        card5 = inputFile.Card5(config_file=config_inp_file)
        card6 = inputFile.Card6(card5_instance=card5,
                                config_file=config_inp_file)
        card7 = inputFile.Card7(config_file=config_inp_file)
        card8 = inputFile.Card8(config_file=config_inp_file)
        card10 = inputFile.Card10(config_file=config_inp_file)

        
    # Write cards to input file
    inputFile.write_to_file("inputExample.txt", card1, card2, card3, card5, card7, card8, card10)

if __name__ == "__main__":

    main(PWD / "config_inp.ini")