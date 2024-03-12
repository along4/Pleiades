import sys, os
import pleiades.sammyInput as psi   #  
import pleiades.nucData as pnd      # grabbing nucData for Pleiades.

def main(config_file=None):
    
    # Use the InputFile method to generate the input file
    inputFile = psi.InputFile()

    # Read cards from config file
    if config_file != None:
        card1 = inputFile.Card1(config_file=config_file)
        card2 = inputFile.Card2(config_file=config_file)
        card3 = inputFile.Card3(config_file=config_file)
        card5 = inputFile.Card5(config_file=config_file)
        card6 = inputFile.Card6(card5_instance=card5,config_file=config_file)
        card7 = inputFile.Card7(config_file=config_file)
        card8 = inputFile.Card8(config_file=config_file)
        card10 = inputFile.Card10(config_file=config_file)
    # Otherwise, use default values
    else:
        card1 = inputFile.Card1()
        card2 = inputFile.Card2()
        card3 = inputFile.Card3()
        card5 = inputFile.Card5()
        card6 = inputFile.Card6(card5_instance=card5)   # card6 depends on card5
        card7 = inputFile.Card7()
        card8 = inputFile.Card8()
        card10 = inputFile.Card10()
        
    # Write cards to input file
    inputFile.write_to_file("inputExample.txt", card1, card2, card3, card5, card7, card8, card10)

if __name__ == "__main__":

    main(sys.argv[1] if len(sys.argv) > 1 else None)
