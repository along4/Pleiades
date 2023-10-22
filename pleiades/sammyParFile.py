import re
import pathlib
from typing import Tuple, List, Dict, Any

class parFile:
    """ parFile class for the Sammy par file.
    """

    
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
                        
        # Same column numbers from card 10.2 of SAMMY manual
        # removing 1 from the starting index, since python index starts with 0 
        self.SPINGROUP_FORMAT = {"group_number":slice(1-1,3),
                                 "exclude":slice(5-1,5),
                                 "n_entrance_channel":slice(8-1,10),
                                 "n_exit_channel":slice(13-1,15),
                                 "spin":slice(16-1,20),
                                 "isotopic_abundance":slice(21-1,30)}

        self.SPINCHANNEL_FORMAT = {"channel_number":slice(3-1,5),
                                   "channel_name":slice(8-1,15),
                                   "exclude":slice(18-1,18),
                                   "L_spin":slice(19-1,20),
                                   "channel_spin":slice(21-1,30),
                                   "boundary_condition":slice(31-1,40),
                                   "effective_radius":slice(41-1,50),
                                   "true_radius":slice(51-1,60)}


    def read(self) -> None:
        """ Reads SAMMY .par file into data-structures that allow updating values
        """
        self.filepath = pathlib.Path(self.filename)
        with open(self.filepath,"r") as fid:
            for line in fid:
                
                # read particle pair cards
                if line.upper().startswith("PARTICLE PAIR DEF"):
                    # loop until the end of the P-Pair cards
                    particle_pair = particle_pairs = [] # empty holders for particle pairs
                    line = next(fid)
                    while line.strip():
                        if line.startswith("Name"):
                            if particle_pair:
                                particle_pair = " ".join(particle_pair).replace("\n"," ").strip()
                                particle_pairs.append(particle_pair) # stack particle pairs in list
                            particle_pair = []
                        particle_pair.append(line) 
                        line = next(fid)
                    particle_pair = " ".join(particle_pair).replace("\n"," ").strip()
                    particle_pairs.append(particle_pair) # stack the final particle pairs in list

                # read spin group and channel cards
                if line.upper().startswith("SPIN GROUP INFO"):
                    # loop until the end of spin groups info
                    spin_groups = []
                    line = next(fid)
                    while line.strip():
                        spin_groups.append(line.replace("\n","")) 
                        line = next(fid)
                    
        self.particle_pair_cards = particle_pairs
        self.spingroup_cards = spin_groups
    
        # parse cards
        self._parse_particle_pair_cards()

        return

    def _parse_particle_pair_cards(self) -> None:
        """ parse a list of particle pair cards, sort the key-word pairs specifying reactions

            Args: 
                - particle_pair_cards (list): list of strings containing the lines associated with particle-pair cards
                - name (string): if "auto", the particle pair is assigned according to the par filename, 
                                otherwise, the upto 6 characters long 'name' will be assigned.  

            Returns: (list of dicts): list containing particle pairs, each entry is a dictionary containing key-value dicts with the associate parameters
        """
        pp_pattern = r'\s*(\b[\w\s]+\b)\s*=\s*([\w.]+)'
        # Find all key-value pairs using regex
        pp_dicts = []
        for num, particle_pair in enumerate(self.particle_pair_cards):
            # assign key-word pairs according to regex pattern
            pp_dict = dict(re.findall(pp_pattern, particle_pair))

            # assign new name for the particle-pair reaction
            if self.rename=="auto" and len(self.particle_pair_cards)==1:
                pp_dict["Name"] = self.filepath.stem[:8]
            elif self.rename=="auto" and len(self.particle_pair_cards)>1:
                pp_dict["Name"] = self.filepath.stem[:6] + f"_{num+1}"
            elif self.rename!="auto" and len(self.particle_pair_cards)==1:
                pp_dict["Name"] = self.filepath.stem[:8]
            elif self.rename!="auto" and len(self.particle_pair_cards)>1:
                pp_dict["Name"] = self.filepath.stem[:6] + f"_{num+1}"
            pp_dicts.append(pp_dict)
    
        self.particle_pair_data = pp_dicts

