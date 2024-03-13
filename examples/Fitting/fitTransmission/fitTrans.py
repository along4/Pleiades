import pandas
import argparse, sys
import matplotlib.pyplot as plt

import pleiades.sammyInput as psi 
import pleiades.sammyRunner as psr 
import pleiades.sammyParFile as pspf



def main(config_inp_file: str="config_inp.ini"):
    
    # Use the InputFile methods read config file, process it into a input, and write an inp file
    sammy_input = psi.InputFile(config_inp_file)
    sammy_input.process()      
    
    sammy_input_file_name = config_inp_file.split(".")[0]+".inp"
    sammy_input.write(sammy_input_file_name)    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process config file for sammy input, run sammy, and plot results.')
    parser.add_argument('--sammyConfig', type=str, default='config.ini', help='Path to the sammy config file')
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    else:
        args = parser.parse_args()
        main(args.sammyConfig)
