import sys, os
import pleiades.sammyInput as psi   #  
import pleiades.nucData as pnd      # grabbing nucData for Pleiades.

def main(config_file=None):

    # read config files 
    sammy_input = psi.InputFile("config.ini")
    sammy_input.process()
    sammy_input.write("example.inp")


if __name__ == "__main__":

    main(sys.argv[1] if len(sys.argv) > 1 else None)
