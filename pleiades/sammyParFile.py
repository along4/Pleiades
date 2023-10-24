import re
import pathlib
from typing import Tuple, List, Dict, Any

class ParFile:
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
        self._filename = filename
        self._rename = rename

        self.par_file_data = {}
                        
        # Same column numbers from card 10.2 of SAMMY manual
        # removing 1 from the starting index, since python index starts with 0 
        self._SPIN_GROUP_FORMAT = {"group_number":slice(1-1,3),
                                 "exclude":slice(5-1,5),
                                 "n_entrance_channel":slice(8-1,10),
                                 "n_exit_channel":slice(13-1,15),
                                 "spin":slice(16-1,20),
                                 "isotopic_abundance":slice(21-1,30)}

        self._SPIN_CHANNEL_FORMAT = {"channel_number":slice(3-1,5),
                                   "channel_name":slice(8-1,15),
                                   "exclude":slice(18-1,18),
                                   "L_spin":slice(19-1,20),
                                   "channel_spin":slice(21-1,30),
                                   "boundary_condition":slice(31-1,40),
                                   #"effective_radius":slice(41-1,50),
                                   "effective_radius":slice(42-1,52),
                                   #"true_radius":slice(51-1,60)}
                                   "true_radius":slice(53-1,63)}


    def read(self) -> None:
        """ Reads SAMMY .par file into data-structures that allow updating values
        """
        self._filepath = pathlib.Path(self._filename)
        with open(self._filepath,"r") as fid:
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
                
                # read resonance data cards
                if line.upper().startswith("RESONANCE PARAM"):
                    # loop until the end of resonance params
                    resonance_params = []
                    line = next(fid)
                    while line.strip():
                        resonance_params.append(line.replace("\n","")) 
                        line = next(fid)

                # read channel radii cards
                if line.upper().startswith('CHANNEL RADII IN KEY') or \
                   line.upper().startswith('CHANNEL RADIUS PARAMETERS FOLLOW'):
                    
                    # next line is the channel radii card
                    channel_radii = line = next(fid).replace("\n"," ").strip() 

                    channel_groups = [] # empty holders for channel-group mapping cards
                    # loop until the end of the channel groups cards
                    while line.strip():
                        if line.strip().startswith("Group"):
                            channel_groups.append(line.replace("\n"," ").strip()) 
                        line = next(fid)

                    
        self._particle_pair_cards = particle_pairs
        self._spin_group_cards = spin_groups
        self._resonance_params_cards = resonance_params
        self._channel_radii_cards = channel_radii
        self._channel_group_cards = channel_groups
    
        # parse cards
        self._parse_particle_pair_cards()
        self._parse_spin_group_cards()
        self._parse_channel_radii_cards()

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
        for num, particle_pair in enumerate(self._particle_pair_cards):
            # assign key-word pairs according to regex pattern
            pp_dict = dict(re.findall(pp_pattern, particle_pair))

            # assign new name for the particle-pair reaction
            if self._rename=="auto" and len(self._particle_pair_cards)==1:
                pp_dict["Name"] = self._filepath.stem[:8]
            elif self._rename=="auto" and len(self._particle_pair_cards)>1:
                pp_dict["Name"] = self._filepath.stem[:6] + f"_{num+1}"
            elif self._rename!="auto" and len(self._particle_pair_cards)==1:
                pp_dict["Name"] = self._filepath.stem[:8]
            elif self._rename!="auto" and len(self._particle_pair_cards)>1:
                pp_dict["Name"] = self._filepath.stem[:6] + f"_{num+1}"
            pp_dicts.append(pp_dict)
    
        self._particle_pair_data = pp_dicts

        self.par_file_data.update({"particle_pair":self._particle_pair_data})

    def _parse_spin_group_cards(self) -> None:
        """ parse a list of spin_group cards, sort the key-word pairs of groups and channels

            Args: 
                - spin_group_cards (list): list of strings containing the lines associated with spin-groups and/or spin-channels

            Returns: (list of dicts): list containing groups, each group is a dictionary containing key-value dicts for spin_groups and channels
        """
        spin_groups = []
        lines = (line for line in self._spin_group_cards) # convert to a generator object
        
        for line in lines:
            # read each line
            spin_group_dict = self._read_spin_group(line)
            # prepare a key-label for the dict entry in the format "group 1"
            group_label = f"group {int(spin_group_dict['group_number'])}"
            # store the spin_group and later the associate channels
            spin_group = {group_label:spin_group_dict}
            
            # number of channels for this group
            n_channels = int(spin_group_dict['n_entrance_channel']) + int(spin_group_dict['n_exit_channel'])
            
            # loop over channels
            for n in range(n_channels):
                line = next(lines)
                # read the spin-channel line
                spin_channel_dict = self._read_spin_channel(line)
                # prepare a key-label for the dict entry in the format "channel 1"
                channel_label = f"channel {int(spin_channel_dict['channel_number'])}"
                # store the associate channels
                spin_group[channel_label] = spin_channel_dict

            spin_groups.append(spin_group)

        self._spin_group_data = spin_groups

        self.par_file_data.update({"spin_group":self._spin_group_data})


    def _parse_channel_radii_cards(self) -> None:
        """ parse a list of channel-radii and channel-groups cards and sort the key-word pairs
        """
        cr_pattern = r'Radii=\s*([\d.]+),\s*([\d.]+)\s*Flags=\s*([\d]+),\s*([\d]+)'
        # Using re.search to find the pattern in the line
        match = re.search(cr_pattern, self._channel_radii_cards)

        cr_data = {"radii": [match.group(1).strip(),match.group(2).strip()],
                   "flags": [match.group(3).strip(),match.group(4).strip()]}

        self._channel_radii_data = cr_data

        # parse channel groups using regex
        cg_pattern = r'Group=(\d+) (?:Chan|Channel)=([\d, ]+),'

        cg_data = []
        for channel_group in self._channel_group_cards:
            # assign key-word pairs according to regex pattern
            match = re.search(cg_pattern, channel_group)

            group = int(match.group(1))  # Extract Group as an integer
            channels = [int(ch) for ch in match.group(2).split(',')]  # Extract Channels as a list of integers

            cg_data.append({"Group": group,"Channels": channels})
                           
        self._channel_group_data = cg_data

        self.par_file_data.update({"channel_group":self._channel_group_data,
                                   "channel_radii":self._channel_radii_data})



    def _read_spin_group(self,spin_group_line: str) -> dict:
        # parse key-word pairs from a spin_group line
        spin_group_dict = {key:spin_group_line[value] for key,value in self._SPIN_GROUP_FORMAT.items()}
        return spin_group_dict
    

    def _write_spin_group(self,spin_group_dict: dict) -> str:
        # write a formated spin_group line from dict with the key-word spin_group values
        new_text = [" "]*40 # 40 characters long list of spaces to be filled
        for key,slice_value in self._SPIN_GROUP_FORMAT.items():
            word_length = slice_value.stop - slice_value.start
            # assign the fixed-format position with the corresponding key-word value
            new_text[slice_value] = list(str(spin_group_dict[key])[:word_length])
        return "".join(new_text)

    
    def _read_spin_channel(self,spin_channel_line: str) -> dict:
        # parse key-word pairs from a spin-channel line
        spin_channel_dict = {key:spin_channel_line[value] for key,value in self._SPIN_CHANNEL_FORMAT.items()}
        return spin_channel_dict


    def _write_spin_channel(self,spin_channel_dict: dict) -> str:
        # write a formated spin-channel line from dict with the key-word channel values
        new_text = [" "]*70 # 70 characters long list of spaces to be filled
        for key,slice_value in self._SPIN_CHANNEL_FORMAT.items():
            word_length = slice_value.stop - slice_value.start
            # assign the fixed-format position with the corresponding key-word value
            new_text[slice_value] = list(str(spin_channel_dict[key])[:word_length])
        return "".join(new_text)
    

    def _write_channel_group(self,channel_group_dict: dict) -> str:
        # write a formated channel-group line from dict with the channel-group key-word
        # this is a free format key-word so there is no template
        group_string = f"{channel_group_dict['Group']}"
        channel_string = ", ".join([f"{ch}" for ch in channel_group_dict["Channels"]])
        return f"Group={group_string} Chan={channel_string},"
    

    def _write_channel_radii(self,channel_radii_dict: dict) -> str:
        # write a formated channel_radii line from dict with the channel_radii key-word
        # this is a free format key-word so there is no template
        radii_string = ", ".join(channel_radii_dict["radii"])
        flag_string = ", ".join(channel_radii_dict["flags"])
        return f"Radii= {radii_string}    Flags= {flag_string}"



if __name__=="__main__":

    par = ParFile("/sammy/samexm/samexm/endf_to_par/archive/Ar_40/results/Ar_40.par")
    par.read()
    print(par.par_file_data)



