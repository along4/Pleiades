import pleiades.sammyInput as psi
import pleiades.sammyRunner as psr
import pleiades.sammyParFile as pspf

import pathlib

PWD = pathlib.Path(__file__).parent # get the location of this py file

def main(config_inp_file: str="config_inp.ini"):
    
    # Use the InputFile methods read config files and write inp files
    sammy_input = psi.InputFile(config_inp_file)
    sammy_input.process()
    sammy_input.write("ENDF.inp")    

    psr.run_endf(inpfile="ENDF.inp")
    
if __name__ == "__main__":

    main(PWD / "config_inp.ini")