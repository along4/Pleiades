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
        
        self._RESONANCE_PARAMS_FORMAT = {"reosnance_energy":slice(1-1,11),
                                        "capture_width":slice(12-1,22),
                                        "neutron_width":slice(23-1,33),
                                        "fission1_width":slice(34-1,44),
                                        "fission2_width":slice(45-1,55),
                                        "vary_energy":slice(56-1,57),
                                        "vary_capture_width":slice(58-1,59),
                                        "vary_neutron_width":slice(60-1,61),
                                        "vary_fission1_width":slice(62-1,63),
                                        "vary_fission2_width":slice(64-1,65),
                                        "igroup":slice(56-1,67)}
        
        self._PARTICLE_PAIRS_FORMAT = {"name": slice(6-1,14),
                                       "particle_a": slice(30-1,38),
                                       "particle_b": slice(55-1,62),
                                       "charge_a": slice(9-1+64,10+64), # 64 is the length of raw1
                                       "charge_b": slice(22-1+64,23+64),
                                       "vary_penetrability": slice(38-1+64,38+64),
                                       "vary_shift": slice(50-1+64,50+64),
                                       "spin_a": slice(9-1+116,13+116),
                                       "spin_b": slice(22-1+116,27+116),
                                       "mass_a": slice(36-1+116,55+116),
                                       "mass_b": slice(64-1+116,83+116)} # 116 is the lengths of raw1 + raw2


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
                                particle_pair = " ".join(particle_pair)
                                particle_pairs.append(particle_pair) # stack particle pairs in list
                            particle_pair = []
                        particle_pair.append(line) 
                        line = next(fid)
                    particle_pair = " ".join(particle_pair)[:-1] # remove the last '\n' character
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
                if line.upper().startswith('CHANNEL RADII IN KEY'):
                    
                    # next line is the channel radii card
                    
                    line = next(fid).replace("\n"," ") 
                    channel_radii = [line]

                    # loop until the end of the channel groups cards
                    while line.strip():
                        if line.strip().startswith("Group"):
                            channel_radii.append(line.replace("\n"," ")) 
                        line = next(fid)

                    
        self._particle_pairs_cards = particle_pairs
        self._spin_group_cards = spin_groups
        self._resonance_params_cards = resonance_params
        self._channel_radii_cards = channel_radii
    
        # parse cards
        self._parse_particle_pairs_cards()
        self._parse_spin_group_cards()
        self._parse_channel_radii_cards()
        self._parse_resonance_params_cards()

        return

    def _parse_particle_pairs_cards(self) -> None:
        """ parse a list of particle_pairs cards, sort the key-word values
        """
        rp_dicts = []
        for card in self._particle_pairs_cards:
            rp_dicts.append(self._read_particle_pairs(card))

        self.par_file_data.update({"particle_pairs":rp_dicts})

    def _parse_spin_group_cards(self) -> None:
        """ parse a list of spin_group cards, sort the key-word pairs of groups and channels

            Args: 
                - spin_group_cards (list): list of strings containing the lines associated with spin-groups and/or spin-channels

            Returns: (list of dicts): list containing groups, each group is a dictionary containing key-value dicts for spin_groups and channels
        """
        sg_dict = []
        lines = (line for line in self._spin_group_cards) # convert to a generator object
        
        for line in lines:
            # read each line
            spin_group_dict = self._read_spin_group(line)

            # first entry is the spin_group
            spin_group = [spin_group_dict]
            
            # number of channels for this group
            n_channels = int(spin_group_dict['n_entrance_channel']) + int(spin_group_dict['n_exit_channel'])
            
            # loop over channels
            for n in range(n_channels):
                line = next(lines)
                # read the spin-channel line
                spin_channel_dict = self._read_spin_channel(line)
                # store the associate channels
                spin_group.append(spin_channel_dict)

            sg_dict.append(spin_group)

        self.par_file_data.update({"spin_group":sg_dict})


    def _parse_channel_radii_cards(self) -> None:
        """ parse a list of channel-radii and channel-groups cards and sort the key-word pairs
        """
        cr_pattern = r'Radii=\s*([\d.]+),\s*([\d.]+)\s*Flags=\s*([\d]+),\s*([\d]+)'

        # Using re.search to find the pattern in the line
        match = re.search(cr_pattern, self._channel_radii_cards[0])

        cr_data = {"radii": [match.group(1).strip(),match.group(2).strip()],
                   "flags": [match.group(3).strip(),match.group(4).strip()]}

        # parse channel groups using regex
        cg_pattern = r'Group=(\d+) (?:Chan|Channel)=([\d, ]+),'

        cg_data = []
        for card in self._channel_radii_cards[1:]:
            # assign key-word pairs according to regex pattern
            match = re.search(cg_pattern, card)

            group = int(match.group(1))  # Extract Group as an integer
            channels = [int(ch) for ch in match.group(2).split(',')]  # Extract Channels as a list of integers

            cg_data.append([group] + channels)

        cr_data["groups"] = cg_data

        self.par_file_data.update({"channel_radii":cr_data})
        

    def _parse_resonance_params_cards(self) -> None:
        """ parse a list of resonance_params cards, sort the key-word values
        """
        rp_dicts = []
        for card in self._resonance_params_cards:
            rp_dicts.append(self._read_resonance_params(card))

        self.par_file_data.update({"resonance_params":rp_dicts})


    def _read_particle_pairs(self,particle_pairs_line: str) -> dict:
        # parse key-word pairs from a particle_pairs line
        particle_pairs_dict = {key:particle_pairs_line[value] for key,value in self._PARTICLE_PAIRS_FORMAT.items()}
        return particle_pairs_dict
    
    def _write_particle_pairs(self,particle_pairs_dict: dict) -> str:
        # write a formated spin-channel line from dict with the key-word channel values
        new_text = """Name=             Particle a=              Particle b=        
      Za=          Zb=           Pent=1     Shift=0
      Sa=          Sb=           Ma=                         Mb=                    """
        new_text = list(str(new_text))
        for key,slice_value in self._PARTICLE_PAIRS_FORMAT.items():
            word_length = slice_value.stop - slice_value.start
            # assign the fixed-format position with the corresponding key-word value
            new_text[slice_value] = list(str(particle_pairs_dict[key])[:word_length])
        return "".join(new_text)


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
    

    def _write_channel_radii(self,channel_radii_dict: dict) -> str:
        # write a formated channel_radii line from dict with the channel_radii key-word
        radii_string = ", ".join(channel_radii_dict["radii"])
        flag_string = ", ".join(channel_radii_dict["flags"])
        cards = [f"Radii= {radii_string}    Flags= {flag_string}"]

        for card in channel_radii_dict['groups']:
            group_string = f"{card[0]}"
            channel_string = ", ".join([f"{ch}" for ch in card[1:]])
            cards.append(f"    Group={group_string} Chan={channel_string},")
            
        return cards
    

    def _read_resonance_params(self,resonance_params_line: str) -> dict:
        # parse key-word pairs from a resonance_params line
        resonance_params_dict = {key:resonance_params_line[value] for key,value in self._RESONANCE_PARAMS_FORMAT.items()}
        return resonance_params_dict
    

    def _write_resonance_params(self,resonance_params_dict: dict) -> str:
        # write a formated spin-channel line from dict with the key-word channel values
        new_text = [" "]*80 # 80 characters long list of spaces to be filled
        for key,slice_value in self._RESONANCE_PARAMS_FORMAT.items():
            word_length = slice_value.stop - slice_value.start
            # assign the fixed-format position with the corresponding key-word value
            new_text[slice_value] = list(str(resonance_params_dict[key])[:word_length])
        return "".join(new_text)



if __name__=="__main__":

    par = ParFile("/sammy/samexm/samexm/endf_to_par/archive/Ar_40/results/Ar_40.par")
    par.read()
    print(par.par_file_data)



