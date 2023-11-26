import re
import pathlib
from typing import Tuple, List, Dict, Any

class ParFile:
    """ parFile class for the Sammy par file.
    """

    
    def __init__(self,filename: str="Ar_40.par", 
                      name: str="auto",
                      weight: float = 1.,
                      emin: float = 0.001,
                      emax: float = 100) -> None:
        """
        Class utility to read, parse and combine par files to allow fitting of compounds
            
        Args:
            - filename (string): parameter file , e.g. 'U_238/results/U_238.par'
            - name (string):  (str, optional): 'auto' will pick a name automatically based on the filename
                                "none" will keep the original name (PPair1 usually)
                               otherwise, reaction name will be renamed according to 'name'
            - weight (float): the weight/abundance of the isotope in the target
            - emin (float): minimum energy [eV] to include in par file, default 1 meV
            - emax (float): maximum energy [eV] to include in par file, default 100 eV
        """
        self.filename = filename
        self.weight = weight
        self.name = name
        self.emin = emin
        self.emax = emax

        self.data = {}
        self.data["fudge_factor"] = 0.1

        # group all update methods in the Update class (and the `update`` namespace)
        self.update = Update(self)
                        
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
                                        "igroup":slice(66-1,67)}
        
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
        
        self._ISOTOPIC_MASSES_FORMAT = {"atomic_mass":slice(1-1,10),
                                        "abundance":slice(11-1,20),
                                        "abundance_uncertainty":slice(21-1,30),
                                        "vary_abundance":slice(31-1,35),
                                        "spin_groups":slice(36-1,78)}
        
        self._NORMALIZATION_FORMAT = {"normalization":slice(1-1,10),
                                     "constant_bg":slice(11-1,20),
                                     "one_over_v_bg":slice(21-1,30),
                                     "sqrt_energy_bg":slice(31-1,40),
                                     "exponential_bg":slice(41-1,50),
                                     "exp_decay_bg":slice(51-1,60),
                                     "vary_normalization":slice(61-1,62),
                                     "vary_constant_bg":slice(63-1,64),
                                     "vary_one_over_v_bg":slice(65-1,66),
                                     "vary_sqrt_energy_bg":slice(67-1,68),
                                     "vary_exponential_bg":slice(69-1,70),
                                     "vary_exp_decay_bg":slice(71-1,72)}
        
        self._BROADENING_FORMAT = {"channel_radius":slice(1-1,10),
                                     "temperature":slice(11-1,20),
                                     "thickness":slice(21-1,30),
                                     "flight_path_spread":slice(31-1,40),
                                     "deltag_fwhm":slice(41-1,50),
                                     "deltae_us":slice(51-1,60),
                                     "vary_channel_radius":slice(61-1,62),
                                     "vary_temperature":slice(63-1,64),
                                     "vary_thickness":slice(65-1,66),
                                     "vary_flight_path_spread":slice(67-1,68),
                                     "vary_deltag_fwhm":slice(69-1,70),
                                     "vary_deltae_us":slice(71-1,72)}
        


    def read(self) -> 'ParFile':
        """Reads SAMMY .par file into data-structure that allows updating values

        Returns:
            ParFile: the ParFile instance
        """
        self._filepath = pathlib.Path(self.filename)

        particle_pair = particle_pairs = [] # empty holders for particle pairs
        resonance_params = []  
        spin_groups = []
        channel_radii = []
        isotopic_masses = []

        with open(self._filepath,"r") as fid:
            for line in fid:
                
                # read particle pair cards

                if line.upper().startswith("PARTICLE PAIR DEF"):

                    # loop until the end of the P-Pair cards
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
                    line = next(fid)
                    while line.strip():
                        spin_groups.append(line.replace("\n","")) 
                        line = next(fid)
                
                # read resonance data cards
              
                if line.upper().startswith("RESONANCE PARAM"):
                    # loop until the end of resonance params
                    line = next(fid)
                    while line.strip():
                        resonance_params.append(line.replace("\n","")) 
                        line = next(fid)

                # read channel radii cards
                if line.upper().startswith('CHANNEL RADII IN KEY'):
                    # next line is the channel radii card
                    line = next(fid).replace("\n"," ") 
                    # loop until the end of the channel groups cards
                    while line.strip():
                        channel_radii.append(line.replace("\n"," ")) 
                        line = next(fid)

                # read isotopic_masses cards
                if line.upper().startswith("ISOTOPIC MASSES"):
                    # loop until the end of isotopic_masses cards
                    line = next(fid)
                    while line.strip():
                        isotopic_masses.append(line.replace("\n","")) 
                        line = next(fid)
           
        self._particle_pairs_cards = particle_pairs
        self._spin_group_cards = spin_groups
        self._resonance_params_cards = resonance_params
        self._channel_radii_cards = channel_radii
        self._isotopic_masses_cards = isotopic_masses
    
        # parse cards
        self._parse_particle_pairs_cards()
        self._parse_spin_group_cards()
        self._parse_channel_radii_cards()
        self._parse_resonance_params_cards()
        self._parse_isotopic_masses_cards()

        # rename
        # the option name=="none" is saved for the purpose of tests
        if self.name!="none":
            self._rename()
            self.update.isotopic_weight()
            self.update.limit_energies_of_parfile()
            self.update.isotopic_masses_abundance()
            self.update.toggle_vary_all_resonances(False)
            self.update.normalization()
            self.update.broadening()
            

        return self
    

    def write(self,filename: str="compound.par") -> None:
        """ writes the data stored in self.data dictionary into a SAMMY .par file

            Args:
                - filename (string): the par file name to write to
        """
        
        if not self.data:
            raise RuntimeError("self.data is emtpy, please run the self.read() method first")
        
        lines = []

        # particle pairs
        lines.append("PARTICLE PAIR DEFINITIONS")

        for card in self.data["particle_pairs"]:
            lines.append(self._write_particle_pairs(card))
        lines.append(" ")

        # spin_groups
        lines.append("SPIN GROUP INFORMATION")

        for card in self.data["spin_group"]:
            # first line is the spin group info
            lines.append(self._write_spin_group(card[0]))
            # number of channels for this group
            n_channels = int(card[0]['n_entrance_channel']) + int(card[0]['n_exit_channel'])
            for channel in range(1,n_channels+1):
                lines.append(self._write_spin_channel(card[channel]))
        lines.append(" ")   

        # resonance params
        lines.append("RESONANCE PARAMETERS")

        for card in self.data["resonance_params"]:
            lines.append(self._write_resonance_params(card))
        lines.append(" "*80)
        lines.append(f"{self.data['fudge_factor']:<11}")
        lines.append(" "*80)

        # channel radii
        lines.append("Channel radii in key-word format".ljust(80))

        for card in self.data["channel_radii"]:
            lines += self._write_channel_radii(card)

        lines.append(" "*80)
        lines.append("")

        # isotopic masses
        if self.data["isotopic_masses"]:
            lines.append("ISOTOPIC MASSES AND ABUNDANCES FOLLOW".ljust(80))
            for card in self.data["isotopic_masses"]:
                lines.append(self._write_isotopic_masses(card))
            lines.append(" "*80)
            lines.append("")

        # normalization
        if self.data["normalization"]:
            lines.append("NORMALIZATION AND BACKGROUND FOLLOW".ljust(80))
            card = self.data["normalization"]
            lines.append(self._write_normalization(card))
            lines.append(" "*80)
            lines.append("")

        # broadening
        if self.data["broadening"]:
            lines.append("BROADENING PARAMETERS MAY BE VARIED".ljust(80))
            card = self.data["broadening"]
            lines.append(self._write_broadening(card))
            lines.append(" "*80)
            lines.append("")

        
        with open(filename,"w") as fid:
            fid.write("\n".join(lines))    
        
    def _rename(self) -> None:
        """rename the isotope and particle-pair names
        """

        pp_count = len(self.data["particle_pairs"])
            

        for num, reaction in enumerate(self.data["particle_pairs"]):
            old_name = reaction["name"]
            if   self.name == "auto" and pp_count==1:
                name = self._filepath.stem[:8]
                new_name = name
            elif self.name == "auto" and pp_count>1:
                name = self._filepath.stem[:6]
                new_name = name + f"_{num+1}"
            elif self.name != "auto" and pp_count==1:
                name = self.name[:8]
                new_name = name
            elif self.name != "auto" and pp_count>1:
                name = self.name[:6]
                new_name = name + f"_{num+1}"
                
            
            for group in self.data["spin_group"]:
                for channel in group[1:]:
                    if channel["channel_name"].strip()==old_name.strip():
                        channel["channel_name"] = new_name

            reaction["name"] = new_name

        self.name = name


    def __add__(self,isotope: 'ParFile') -> 'ParFile':
        """adds the data of another ParFile instance to form a nuclei

        Args:
            isotope (parFile): a parFile instance of another isotope to be added

        Returns:
            parFile: combined parFile instance
        """
        from copy import deepcopy
        compound = deepcopy(self)

        # only add an isotope if resonances exists in the specified energy range
        if isotope.data["resonance_params"]:

            # find the last group number and bump up the group number of the added isotope
            last_group_number = int(compound.data["spin_group"][-1][0]["group_number"])
            isotope.update.bump_group_number(increment=last_group_number)

            last_igroup_number = int(compound.data["resonance_params"][-1]["igroup"])
            isotope.update.bump_igroup_number(increment=last_igroup_number)

            # update particle pairs
            compound.data["particle_pairs"] += isotope.data["particle_pairs"]

            # update spin_groups
            compound.data["spin_group"] += isotope.data["spin_group"]

            # update resonance_params
            compound.data["resonance_params"] += isotope.data["resonance_params"]

            # update channel_radii
            compound.data["channel_radii"] += isotope.data["channel_radii"]

            # update isotopic_masses
            compound.data["isotopic_masses"] += isotope.data["isotopic_masses"]

        return compound



    def _parse_particle_pairs_cards(self) -> None:
        """ parse a list of particle_pairs cards, sort the key-word values
        """
        rp_dicts = []
        for card in self._particle_pairs_cards:
            rp_dicts.append(self._read_particle_pairs(card))

        self.data.update({"particle_pairs":rp_dicts})

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

        self.data.update({"spin_group":sg_dict})


    def _parse_channel_radii_cards(self) -> None:
        """ parse a list of channel-radii and channel-groups cards and sort the key-word pairs
        """

        cr_data = []
        cards = (card for card in self._channel_radii_cards) # convert to a generator object

        # parse channel radii and groups using regex
        cr_pattern = r'Radii=\s*([\d.]+),\s*([\d.]+)\s*Flags=\s*([\d]+),\s*([\d]+)'
        cg_pattern = r'Group=(\d+) (?:Chan|Channel)=([\d, ]+),'

        card = next(cards)
        # Using re.search to find the pattern in the line
        while match:=re.search(cr_pattern, card):
            cr_dict = {"radii": [match.group(1).strip(),match.group(2).strip()],
                        "flags": [match.group(3).strip(),match.group(4).strip()]}


            cg_data = []
            card = next(cards)
            while match:=re.search(cg_pattern, card):
                group = int(match.group(1))  # Extract Group as an integer
                channels = [int(ch) for ch in match.group(2).split(',')]  # Extract Channels as a list of integers

                cg_data.append([group] + channels)

                try:
                    card = next(cards)
                except StopIteration:
                    break


            cr_dict["groups"] = cg_data

            cr_data.append(cr_dict)

        self.data.update({"channel_radii":cr_data})
        

    def _parse_resonance_params_cards(self) -> None:
        """ parse a list of resonance_params cards, sort the key-word values
        """
        rp_dicts = []
        for card in self._resonance_params_cards:
            rp_dicts.append(self._read_resonance_params(card))

        self.data.update({"resonance_params":rp_dicts})


    def _parse_isotopic_masses_cards(self) -> None:
        """ parse a list of isotopic_masses cards, sort the key-word values
        """
        im_dicts = []
        for card in self._isotopic_masses_cards:
            im_dicts.append(self._read_isotopic_masses(card))

        self.data.update({"isotopic_masses":im_dicts})


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
            new_text[slice_value] = list(str(particle_pairs_dict[key]).ljust(word_length))
        return "".join(new_text).replace("\n ","\n")


    def _read_spin_group(self,spin_group_line: str) -> dict:
        # parse key-word pairs from a spin_group line
        spin_group_dict = {key:spin_group_line[value] for key,value in self._SPIN_GROUP_FORMAT.items()}
        return spin_group_dict
    

    def _write_spin_group(self,spin_group_dict: dict) -> str:
        # write a formated spin_group line from dict with the key-word spin_group values
        new_text = [" "]*80 # 80 characters long list of spaces to be filled
        for key,slice_value in self._SPIN_GROUP_FORMAT.items():
            word_length = slice_value.stop - slice_value.start
            # assign the fixed-format position with the corresponding key-word value
            new_text[slice_value] = list(str(spin_group_dict[key]).ljust(word_length))
        return "".join(new_text)

    
    def _read_spin_channel(self,spin_channel_line: str) -> dict:
        # parse key-word pairs from a spin-channel line
        spin_channel_dict = {key:spin_channel_line[value] for key,value in self._SPIN_CHANNEL_FORMAT.items()}
        return spin_channel_dict


    def _write_spin_channel(self,spin_channel_dict: dict) -> str:
        # write a formated spin-channel line from dict with the key-word channel values
        new_text = [" "]*80 # 80 characters long list of spaces to be filled
        for key,slice_value in self._SPIN_CHANNEL_FORMAT.items():
            word_length = slice_value.stop - slice_value.start
            # assign the fixed-format position with the corresponding key-word value
            new_text[slice_value] = list(str(spin_channel_dict[key]).ljust(word_length))
        return "".join(new_text)
    

    def _write_channel_radii(self,channel_radii_dict: dict) -> str:
        # write a formated channel_radii line from dict with the channel_radii key-word
        radii_string = ", ".join(channel_radii_dict["radii"])
        flag_string = ", ".join(channel_radii_dict["flags"])
        cards = [f"Radii= {radii_string}    Flags= {flag_string}".ljust(80)]

        for card in channel_radii_dict['groups']:
            group_string = f"{card[0]}"
            channel_string = ", ".join([f"{ch}" for ch in card[1:]])
            cards.append(f"    Group={group_string} Chan={channel_string},".ljust(80))
            
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
            new_text[slice_value] = list(str(resonance_params_dict[key]).ljust(word_length))
        return "".join(new_text)
    
    def _read_isotopic_masses(self,isotopic_masses_line: str) -> None:
        # parse key-word pairs from a isotopic-masses line
        isotopic_masses_dict = {key:isotopic_masses_line[value] for key,value in self._ISOTOPIC_MASSES_FORMAT.items()}
        return isotopic_masses_dict
    
    def _write_isotopic_masses(self,isotopic_masses_dict: dict) -> str:
        # write a formated isotopic_masses line from dict with the key-word channel values
        new_text = [" "]*80 # 80 characters long list of spaces to be filled
        for key,slice_value in self._ISOTOPIC_MASSES_FORMAT.items():
            word_length = slice_value.stop - slice_value.start
            # assign the fixed-format position with the corresponding key-word value
            new_text[slice_value] = list(str(isotopic_masses_dict[key]).ljust(word_length))
        return "".join(new_text)
    
    def _write_normalization(self,normalization_dict: dict) -> str:
        # write a formated normalization line from dict with the key-word normalization values
        new_text = [" "]*80 # 80 characters long list of spaces to be filled
        for key,slice_value in self._NORMALIZATION_FORMAT.items():
            word_length = slice_value.stop - slice_value.start
            # assign the fixed-format position with the corresponding key-word value
            new_text[slice_value] = list(str(normalization_dict[key]).ljust(word_length))
        return "".join(new_text)

    def _write_broadening(self,broadening_dict: dict) -> str:
        # write a formated broadening line from dict with the key-word broadening values
        new_text = [" "]*80 # 80 characters long list of spaces to be filled
        for key,slice_value in self._BROADENING_FORMAT.items():
            word_length = slice_value.stop - slice_value.start
            # assign the fixed-format position with the corresponding key-word value
            new_text[slice_value] = list(str(broadening_dict[key]).ljust(word_length))
        return "".join(new_text)
    






class Update():
# stores all the data updating methods of ParFile class
    def __init__(self,parent: "ParFile") -> None:
        self.parent = parent

    
    def bump_group_number(self, increment: int = 0) -> None:
        """bump up the group number in the data in a constant increment

        Args:
            increment (int, optional): a constant increment to add to all group numbers
        """

        # bump spin group data
        for group in self.parent.data["spin_group"]:
            group[0]["group_number"] = f"{int(group[0]['group_number'])+increment:>3}"


        # bump channel radii
        for rad in self.parent.data["channel_radii"]:
            for channel in rad["groups"]:
                channel[0] = channel[0] + increment  


        # bump isotopic masses
        if self.parent.data["isotopic_masses"]:
            for isotope in self.parent.data["isotopic_masses"]:
                spin_groups = [f"{group[0]['group_number'].strip():>5}" for group in self.parent.data["spin_group"]]
                    
                sg_formatted = "".join(spin_groups[:8]).ljust(43)
                L = (len(spin_groups) - 8)//15 if len(spin_groups)>8 else -1 # number of extra lines needed
                for l in range(0,L+1):
                    sg_formatted += "-1\n" + "".join(spin_groups[8+15*l:8+15*(l+1)]).ljust(78)
                isotope["spin_groups"] = sg_formatted


    def bump_igroup_number(self, increment: int = 0) -> None:
        """bump up the igroup number in the data in a constant increment

        igroup is a variable in resonance params, it has a differnet meaning than spin group

        Args:
            increment (int, optional): a constant increment to add to all group numbers
        """
        # bump resonance_params
        for res in self.parent.data["resonance_params"]:
            res["igroup"] = f"{int(res['igroup'])+increment:>2}"    


    def isotopic_weight(self) -> None:
        """Update the isotopic weight in the spin_group data
        """
        for group in self.parent.data["spin_group"]:
            group[0]["isotopic_abundance"] = f"{f'{self.parent.weight:.7f}':>10}"


    def isotopic_masses_abundance(self) -> None:
        """Update the isotopic masses data
        """
        if self.parent.data["isotopic_masses"]:
            for card in self.parent.data["isotopic_masses"]:
                card["abundance"] = f"{f'{self.parent.weight:.7f}':>9}"
        else:
            spin_groups = [f"{group[0]['group_number'].strip():>5}" for group in self.parent.data["spin_group"]]
                
            sg_formatted = "".join(spin_groups[:8]).ljust(43)
            L = (len(spin_groups) - 8)//15 if len(spin_groups)>8 else -1 # number of extra lines needed
            for l in range(0,L+1):
                sg_formatted += "-1\n" + "".join(spin_groups[8+15*l:8+15*(l+1)]).ljust(78)
                
            iso_dict = {"atomic_mass":f'{float(self.parent.data["particle_pairs"][0]["mass_b"]):>9}',
                        "abundance":f"{f'{self.parent.weight:.7f}':>9}",
                        "abundance_uncertainty":f"{f'{self.parent.weight*0.1:.7f}':>9}",
                        "vary_abundance":"1".ljust(5),
                        "spin_groups":sg_formatted}
            self.parent.data["isotopic_masses"].append(iso_dict)

    def toggle_vary_abundances(self,vary:bool =False) -> None:
        """toggles the vary flag on all abundances

        Args:
            vary (bool, optional): True will flag all abundances to vary
        """
        for isotope in self.parent.data["isotopic_masses"]:
            isotope["vary_abundance"] = f"{vary:<5}"


    def limit_energies_of_parfile(self) -> None:
        # remove all resonances and spin groups that are above or below the energy range specified in the inp file
        new_res_params = []
        igroups = set()
        for num, res in enumerate(self.parent.data["resonance_params"]):
            # cast all numbers such as "3.6700-5" to floats
            energy = "e-".join(res['reosnance_energy'].split("-")).lstrip("e").replace("+","e+") if not "e" in res['reosnance_energy'] else res['reosnance_energy']
            if self.parent.emin <=  float(energy) < self.parent.emax:
                new_res_params.append(res)
                igroups.add(res["igroup"].strip())
        
        self.parent.data["resonance_params"] = new_res_params

        # go through the remaining resonances to see if we can omit spin groups
        spin_groups = []
        for group in self.parent.data["spin_group"]:
            if group[0]['group_number'].strip() in igroups:
                spin_groups.append(group)
        self.parent.data["spin_group"] = spin_groups

        # go through the channel radii and omit those that correspond to unued spin groups
        channel_radii = []
        for radii in self.parent.data["channel_radii"]:
            useful_groups = []
            for groups_and_channels in radii["groups"]:
                if str(groups_and_channels[0]) in igroups:
                    useful_groups.append(groups_and_channels)
            if useful_groups:
                radii.update({"groups":useful_groups})
                channel_radii.append(radii)

        self.parent.data["channel_radii"] = channel_radii

        # reindex igroups
        igroups = set([])
        igroup = 0
        index_map = {}
        for res in self.parent.data["resonance_params"]:
            if res["igroup"].strip() not in igroups:
                igroups.add(res["igroup"].strip())
                igroup += 1
                index_map[res["igroup"].strip()] = f"{igroup}"
            res["igroup"] = f"{index_map[res['igroup'].strip()]:>2}"

        # reindex radii
        for radii in self.parent.data["channel_radii"]:
            for groups_and_channels in radii["groups"]:
                groups_and_channels[0] = int(index_map[str(groups_and_channels[0])])

        # reindex spin groups
        for group in self.parent.data["spin_group"]:
            group[0]['group_number'] = f"{index_map[group[0]['group_number'].strip()]:>3}"

        return

        

    def toggle_vary_all_resonances(self,vary: bool=False) -> None:
        """toggles the vary flag on all resonances

        Args:
            vary (bool, optional): True will flag all resonances to vary
        """
        for card in self.parent.data["resonance_params"]:
            card["vary_energy"] = f"{1:>2}" if vary else f"{0:>2}"
            card["vary_capture_width"] = f"{1:>2}" if vary else f"{0:>2}"
            card["vary_neutron_width"] = f"{1:>2}" if vary else f"{0:>2}"
            if card["fission1_width"].strip():
                card["vary_fission1_width"] = f"{1:>2}" if vary else f"{0:>2}"
            if card["fission2_width"].strip():
                card["vary_fission2_width"] = f"{1:>2}" if vary else f"{0:>2}"


    def normalization(self, vary:bool = False, **kwargs) -> None:
        """change or vary normalization parameters and vary flags

        Args:
              - vary (bool): if True all parameters are set to "vary", otherwise all set to "fixed"
              - normalization (float)
              - constant_bg (float)
              - one_over_v_bg (float)
              - sqrt_energy_bg (float)
              - exponential_bg (float)
              - exp_decay_bg (float)
              - vary_normalization (int) 0=fixed, 1=vary, 2=pup
              - vary_constant_bg (int) 0=fixed, 1=vary, 2=pup
              - vary_one_over_v_bg (int) 0=fixed, 1=vary, 2=pup
              - vary_sqrt_energy_bg (int) 0=fixed, 1=vary, 2=pup
              - vary_exponential_bg (int) 0=fixed, 1=vary, 2=pup
              - vary_exp_decay_bg (int) 0=fixed, 1=vary, 2=pup
        """
        if "normalization" not in self.parent.data:
            self.parent.data["normalization"] = {"normalization":1.,
                                                 "constant_bg":0.,
                                                 "one_over_v_bg":0.,
                                                 "sqrt_energy_bg":0.,
                                                 "exponential_bg":0.,
                                                 "exp_decay_bg":0.,
                                                 "vary_normalization":0,
                                                 "vary_constant_bg":0,
                                                 "vary_one_over_v_bg":0,
                                                 "vary_sqrt_energy_bg":0,
                                                 "vary_exponential_bg":0,
                                                 "vary_exp_decay_bg":0,}
        if vary:
            self.parent.data["normalization"].update({"vary_normalization":1,
                                                 "vary_constant_bg":1,
                                                 "vary_one_over_v_bg":1,
                                                 "vary_sqrt_energy_bg":1,
                                                 "vary_exponential_bg":1,
                                                 "vary_exp_decay_bg":1,}) 
        else:
            self.parent.data["normalization"].update({"vary_normalization":0,
                                                 "vary_constant_bg":0,
                                                 "vary_one_over_v_bg":0,
                                                 "vary_sqrt_energy_bg":0,
                                                 "vary_exponential_bg":0,
                                                 "vary_exp_decay_bg":0,})     
                       
        self.parent.data["normalization"].update(kwargs)


    def broadening(self, vary: bool=False, **kwargs) -> None:
        """change or vary broadening parameters and vary flags

        Args:
              - vary (bool): if True all parameters are set to "vary", otherwise all set to "fixed"
              - channel_radius (float) CRFN
              - temperature (float) TEMP
              - thickness (float) THICK
              - flight_path_spread (float) DELTAL
              - deltag_fwhm (float) DELTAG
              - deltae_us (float) DELTAE
              - vary_channel_radius (int) 0=fixed, 1=vary, 2=pup
              - vary_temperature (int) 0=fixed, 1=vary, 2=pup
              - vary_thickness (int) 0=fixed, 1=vary, 2=pup
              - vary_flight_path_spread (int) 0=fixed, 1=vary, 2=pup
              - vary_deltag_fwhm (int) 0=fixed, 1=vary, 2=pup
              - vary_deltae_us (int) 0=fixed, 1=vary, 2=pup
        """
        if "broadening" not in self.parent.data:
            self.parent.data["broadening"] = {"channel_radius":"",
                                                 "temperature":"296.",
                                                 "thickness":"",
                                                 "flight_path_spread":"",
                                                 "deltag_fwhm":"",
                                                 "deltae_us":"",
                                                 "vary_channel_radius":0,
                                                 "vary_temperature":0,
                                                 "vary_thickness":0,
                                                 "vary_flight_path_spread":0,
                                                 "vary_deltag_fwhm":0,
                                                 "vary_deltae_us":0,}
        if vary:
            self.parent.data["broadening"].update({"vary_channel_radius":1,
                                                 "vary_temperature":1,
                                                 "vary_thickness":1,
                                                 "vary_flight_path_spread":1,
                                                 "vary_deltag_fwhm":1,
                                                 "vary_deltae_us":1,}) 
        else:
            self.parent.data["broadening"].update({"vary_channel_radius":0,
                                                 "vary_temperature":0,
                                                 "vary_thickness":0,
                                                 "vary_flight_path_spread":0,
                                                 "vary_deltag_fwhm":0,
                                                 "vary_deltae_us":0,})     

        self.parent.data["broadening"].update(kwargs)

     

if __name__=="__main__":

    par = ParFile("/sammy/samexm/samexm/endf_to_par/archive/Ar_40/results/Ar_40.par")
    par.read()
    print(par.data)



