import pandas
import argparse, sys
import shutil
import matplotlib.pyplot as plt

import pleiades.sammyInput as psi 
import pleiades.sammyRunner as psr 
import pleiades.sammyParFile as pspf



def main(config_inp_file: str="config_inp.ini"):
    
    # Creating file names for SAMMY inputs and parameters. 
    run_name = config_inp_file.split(".")[0]
    sammy_inp_file_name = run_name+".inp"
    sammy_par_file_name = run_name+".par"
    
    # Use the InputFile methods read config file, process it into a input, and write an inp file
    sammy_input = psi.InputFile(config_inp_file)
    sammy_input.process()      
    sammy_input.write(sammy_inp_file_name)    

    # Use the run_endf in sammyRunner to generate the needed par file.
    psr.run_endf(inpfile=sammy_inp_file_name)
    
    #psr.run(archivename=run_name,inpfile=sammy_inp_file_name,parfile=sammy_par_file_name,datafile="u235_1_to_100eV.twenty") 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process config file for sammy input, run sammy, and plot results.')
    parser.add_argument('--sammyConfig', type=str, default='config.ini', help='Path to the sammy config file')
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    else:
        args = parser.parse_args()
        main(args.sammyConfig)
