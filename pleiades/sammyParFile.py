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
        self._parse_spingroup_cards()

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

    def _parse_spingroup_cards(self) -> None:
        """ parse a list of spingroup cards, sort the key-word pairs of groups and channels

            Args: 
                - spingroup_cards (list): list of strings containing the lines associated with spin-groups and/or spin-channels

            Returns: (list of dicts): list containing groups, each group is a dictionary containing key-value dicts for spingroups and channels
        """
        spingroups = []
        lines = (line for line in self.spingroup_cards) # convert to a generator object
        
        for line in lines:
            # read each line
            spingroup_dict = self._read_spingroup(line)
            # prepare a key-label for the dict entry in the format "group 1"
            group_label = f"group {int(spingroup_dict['group_number'])}"
            # store the spingroup and later the associate channels
            spingroup = {group_label:spingroup_dict}
            
            # number of channels for this group
            n_channels = int(spingroup_dict['n_entrance_channel']) + int(spingroup_dict['n_exit_channel'])
            
            # loop over channels
            for n in range(n_channels):
                line = next(lines)
                # read the spin-channel line
                spinchannel_dict = self._read_spinchannel(line)
                # prepare a key-label for the dict entry in the format "channel 1"
                channel_label = f"channel {int(spinchannel_dict['channel_number'])}"
                # store the associate channels
                spingroup[channel_label] = spinchannel_dict

            spingroups.append(spingroup)

        self.spingroup_data = spingroups


    def _read_spingroup(self,spingroup_line: str) -> dict:
        # parse key-word pairs from a spingroup line
        spingroup_dict = {key:spingroup_line[value] for key,value in self.SPINGROUP_FORMAT.items()}
        return spingroup_dict
    

    def _write_spingroup(self,spingroup_dict: dict) -> str:
        # write a formated spingroup line from dict with the key-word spingroup values
        new_text = [" "]*40 # 40 characters long list of spaces to be filled
        for key,slice_value in self.SPINGROUP_FORMAT.items():
            word_length = slice_value.stop - slice_value.start
            # assign the fixed-format position with the corresponding key-word value
            new_text[slice_value] = list(str(spingroup_dict[key])[:word_length])
        return "".join(new_text)

    
    def _read_spinchannel(self,spinchannel_line: str) -> dict:
        # parse key-word pairs from a spin-channel line
        spinchannel_dict = {key:spinchannel_line[value] for key,value in self.SPINCHANNEL_FORMAT.items()}
        return spinchannel_dict


    def _write_spinchannel(self,spinchannel_dict: dict) -> str:
        # write a formated spin-channel line from dict with the key-word channel values
        new_text = [" "]*70 # 70 characters long list of spaces to be filled
        for key,slice_value in self.SPINCHANNEL_FORMAT.items():
            word_length = slice_value.stop - slice_value.start
            # assign the fixed-format position with the corresponding key-word value
            new_text[slice_value] = list(str(spinchannel_dict[key])[:word_length])
        return "".join(new_text)


