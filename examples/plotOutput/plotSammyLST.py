import sys

import pleiades.sammyPlotter as psp

def main(input_file=None, output_file=None, plot_type=None):
    
    # currently testing only the LST plot
    with open(input_file) as f:
        lines = f.readlines()
              

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None,
         sys.argv[2] if len(sys.argv) > 2 else None,
         sys.argv[3] if len(sys.argv) > 3 else None)
    