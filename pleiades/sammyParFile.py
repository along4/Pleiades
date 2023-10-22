import re
import pathlib
from typing import Tuple, List, Dict, Any

class parFile:
    """ parFile class for the Sammy par file.
    """

    # Same column numbers from card 10.2 of SAMMY manual
    # removing 1 from the starting index, since python index starts with 0 
    SPINGROUP_FORMAT = {"group_number":slice(1-1,3),
                        "exclude":slice(5-1,5),
                        "n_entrance_channel":slice(8-1,10),
                        "n_exit_channel":slice(13-1,15),
                        "spin":slice(16-1,20),
                        "isotopic_abundance":slice(21-1,30)}

    SPINCHANNEL_FORMAT = {"channel_number":slice(3-1,5),
                        "channel_name":slice(8-1,15),
                        "exclude":slice(18-1,18),
                        "L_spin":slice(19-1,20),
                        "channel_spin":slice(21-1,30),
                        "boundary_condition":slice(31-1,40),
                        "effective_radius":slice(41-1,50),
                        "true_radius":slice(51-1,60)}
    
    def __init__(self,filename: str="Ar_40.par", rename: str="auto") -> None:
        """
        Class utility to read, parse and combine par files to allow fitting of compounds
            
        Args:
            - filename (string): parameter file , e.g. 'U_238/results/U_238.par'
            - rename (string): 'auto' will pick a name automatically based on the filename
                               otherwise, reaction name will be renamed according to 'name'
        """
        self.filename = filename
        self.rename = rename
