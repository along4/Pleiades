import configparser

class InputFile:
    """ InputFile class for the Sammy input file.
    """

    MAX_COLUMNS = 80
    
    @staticmethod
    def format_type_A(data, width):
        """ Format a string to be left-justified in a character field of the given width.

        Args:
            data (string): The string to be formatted.
            width (int): Integer width of the field.

        Returns:
            string: character field of the given width with the string left-justified.
        """
        return f"{data:<{width}}"

    @staticmethod
    def format_type_F(data, width):
        """ Format a float to be right-justified in a float field of the given width.

        Args:
            data (float): The float to be formatted.
            width (int): Integer width of the field.

        Returns:
            string: float field of the given width with the float right-justified.
        """
        # The ".4f" here denotes 4 decimal places. You can adjust if needed.
        return f"{data:>{width}.4f}"

    @staticmethod
    def format_type_I(data, width):
        """ Format an integer to be right-justified in an integer field of the given width.

        Args:
            data (int): integer to be formatted.
            width (int): Integer width of the field.

        Returns:
            _string: integer field of the given width with the integer right-justified.
        """
        return f"{data:>{width}d}"

    class Card1:
        """ Card1 class for the Sammy input file.
        """
        def __init__(self, config_file=None):
            """ Initialize Card1 instance.

            Args:
                config_file (string, optional): Path to the configuration file. Defaults to None.
            """
            self.TITLE = "Blank Sammy Input File Title"
            if config_file:
                self._read_from_config(config_file)
        
        def set(self, TITLE):
            """ Set the TITLE of the Card1 instance.

            Args:
                TITLE (string): The TITLE to set.
            """
            self.TITLE = TITLE
        
        def _read_from_config(self, config_file):
            config = configparser.ConfigParser()
            config.read(config_file)
            self.TITLE = config.get('Card1', 'TITLE', fallback=self.TITLE)
            
        def __str__(self):
            return InputFile.format_type_A(self.TITLE, InputFile.MAX_COLUMNS)

    class Card2:
        """ Card2 class for the Sammy input file. 
        """
        def __init__(self, config_file=None):
            # Default values
            self.ELMNT = "none"     # Element name
            self.AW = 0             # Atomic weight in amu
            self.EMIN = 0           # Minimum energy
            self.EMAX = 0           # Maximum energy
            self.NEPNTS = 10001     # Number of points to be used in generating artificial energy grid (default = 10001)
            self.ITMAX = 2          # Number of iterations (default = 2)
            self.ICORR = 50         # Correlation option (default = 50)
            self.NXTRA = 0          # Number of extra points to be added between each pair of data points for auxiliary energy grid (Default = 0)
            self.IPTDOP = 9         # Number of points to be added to auxiliary energy grid across small resonances (Default = 9)
            self.IPTWID = 5         # Determines the number of points to be added to auxiliary grid in tails of small resonances (Default = 5)
            self.IXXCHN = 0         # Number of energy channels in ODF-type data file to be ignored 
            self.NDIGIT = 2         # Number of digits for compact format for covariance matrix (Default = 2)
            self.IDROPP = 2         # The input resonanceparameter covariance matrix will be modified before being used in the fitting procedure. (Default = 2)
            self.MATNUM = 0         # ENDF Material number

            if config_file:
                self._read_from_config(config_file)
            
        def set(self, ELMNT=None, AW=None, EMIN=None, EMAX=None, NEPNTS=None, ITMAX=None, ICORR=None, NXTRA=None, IPTDOP=None, IPTWID=None, IXXCHN=None, NDIGIT=None, IDROPP=None, MATNUM=None):
            """ Set the Card2 instance values.

            Args:
                ELMNT (string, optional): Element name. Defaults to None.
                AW (float, optional): Atomic weight in amu. Defaults to 0.
                EMIN (float, optional): Minimum energy. Defaults to 0.
                EMAX (float, optional): Maximum energy. Defaults to 0.
                NEPNTS (int, optional): Number of points to be used in generating artificial energy grid. Defaults to 10001.
                ITMAX (int, optional): Number of iterations. Defaults to 2.
                ICORR (int, optional): Correlation option. Defaults to 50.
                NXTRA (int, optional): Number of extra points to be added between each pair of data points for auxiliary energy grid. Defaults to 0. 
                IPTDOP (int, optional): Number of points to be added to auxiliary energy grid across small resonances. Defaults to 9.
                IPTWID (int, optional): Determines the number of points to be added to auxiliary grid in tails of small resonances. Defaults to 5
                IXXCHN (int, optional): Number of energy channels in ODF-type data file to be ignored 
                NDIGIT (int, optional): Number of digits for compact format for covariance matrix (Default = 2)
                IDROPP (int, optional): The input resonanceparameter covariance matrix will be modified before being used in the fitting procedure. Defaults to 2
                MATNUM (int, optional): ENDF Material number. Defaults to 0.
            """
            if ELMNT is not None: self.ELMNT = ELMNT
            if AW is not None: self.AW = AW
            if EMIN is not None: self.EMIN = EMIN
            if EMAX is not None: self.EMAX = EMAX
            if NEPNTS is not None: self.NEPNTS = NEPNTS
            if ITMAX is not None: self.ITMAX = ITMAX
            if ICORR is not None: self.ICORR = ICORR
            if NXTRA is not None: self.NXTRA = NXTRA
            if IPTDOP is not None: self.IPTDOP = IPTDOP
            if IPTWID is not None: self.IPTWID = IPTWID
            if IXXCHN is not None: self.IXXCHN = IXXCHN
            if NDIGIT is not None: self.NDIGIT = NDIGIT
            if IDROPP is not None: self.IDROPP = IDROPP
            if MATNUM is not None: self.MATNUM = MATNUM

        def _read_from_config(self, config_file):
            config = configparser.ConfigParser()
            config.read(config_file)
            self.ELMNT = config.get('Card2', 'ELMNT', fallback=self.ELMNT)
            self.AW = config.getfloat('Card2', 'AW', fallback=self.AW)
            self.EMIN = config.getfloat('Card2', 'EMIN', fallback=self.EMIN)
            self.EMAX = config.getfloat('Card2', 'EMAX', fallback=self.EMAX)    
            self.AW = config.getfloat('Card2', 'AW', fallback=self.AW)
            self.NEPNTS = config.getint('Card2', 'NEPNTS', fallback=self.NEPNTS)
            self.ITMAX = config.getint('Card2', 'ITMAX', fallback=self.ITMAX)
            self.ICORR = config.getint('Card2', 'ICORR', fallback=self.ICORR)
            self.NXTRA = config.getint('Card2', 'NXTRA', fallback=self.NXTRA)
            self.IPTDOP = config.getint('Card2', 'IPTDOP', fallback=self.IPTDOP)
            self.IPTWID = config.getint('Card2', 'IPTWID', fallback=self.IPTWID)
            self.IXXCHN = config.getint('Card2', 'IXXCHN', fallback=self.IXXCHN)
            self.NDIGIT = config.getint('Card2', 'NDIGIT', fallback=self.NDIGIT)
            self.IDROPP = config.getint('Card2', 'IDROPP', fallback=self.IDROPP)
            self.MATNUM = config.getint('Card2', 'MATNUM', fallback=self.MATNUM)
            
        def __str__(self):
            return (
                InputFile.format_type_A(self.ELMNT, 10) +
                InputFile.format_type_F(self.AW, 10) +
                InputFile.format_type_F(self.EMIN, 10) +
                InputFile.format_type_F(self.EMAX, 10) +
                InputFile.format_type_I(self.NEPNTS, 5) +
                InputFile.format_type_I(self.ITMAX, 5) +
                InputFile.format_type_I(self.ICORR, 2) +
                InputFile.format_type_I(self.NXTRA, 3) +
                InputFile.format_type_I(self.IPTDOP, 2) +
                InputFile.format_type_I(self.IPTWID, 2) +
                InputFile.format_type_I(self.IXXCHN, 10) +
                InputFile.format_type_I(self.NDIGIT, 2) +
                InputFile.format_type_I(self.IDROPP, 2) +
                InputFile.format_type_I(self.MATNUM, 6)
            )

    class Card3:
        """ Card3 class for the Sammy input file.
        """
        
        # Some predefined command statements
        REICH_MOORE_FORM="REICH-MOORE FORMALISm is wanted"
        ORIG_REICH_MOORE_FORM = "ORIGINAL REICH-MOORE formalism"
        MULTI_BREIT = "MULTILEVEL BREITWIGner is wanted"
        SINGLE_BREIT = "SINGLE LEVEL BREITWigner is wanted"
        RED_WIDTH_AMPS = "REDUCED WIDTH AMPLITudes are used for input"
        NEW_SPIN_FORMAT = "USE NEW SPIN GROUP Format"
        PARTICL_PAIR_DEF = "PARTICLE PAIR DEFINItions are used"
        KEY_WORD_PARTICLE_PAIR= "KEY-WORD PARTICLE-PAir definitions are given"
        QUANTUM_NUMBERS = "QUANTUM NUMBERS ARE in parameter file"
        PUT_QUANTUM_NUMS_IN_PARAM = "PUT QUANTUM NUMBERS into parameter file"    
        INPUT_ENDF = "INPUT IS ENDF/B FILE"
        USE_ENDF_ENERGY = "USE ENERGY RANGE FROm endf/b file"
        FLAG_ALL_RES = "FLAG ALL RESONANCE Parameters"
        SOLVE_BAYES = "SOLVE BAYES EQUATIONs"
        NO_SOLVE_BAYES = "DO NOT SOLVE BAYES EQUATIONS"
        TWENTY = "USE TWENTY SIGNIFICAnt digits"
        BROADENING = "BROADENING IS WANTED"
        CHI_SQUARED = "CHI SQUARED IS WANTEd"
        NO_CHI_SQUARED = "CHI SQUARED IS NOT Wanted"
        
        
        def __init__(self, config_file=None):
            self.commands = []  # A list to hold the command statements
            if config_file:
                self._read_from_config(config_file)

        def add_command(self, command):
            """Add a command statement to the list."""
            self.commands.append(command)

        def _read_from_config(self, config_file):
            """Read the Card3 values from the config file using configparser. """

            config = configparser.ConfigParser()
            config.read(config_file)
            # Assuming the config file has a 'Card3' section with 'commands' that's a comma-separated list of commands
            commands = config.get('Card3', 'commands', fallback='').split(',')
            for command in commands:
                command = command.strip()  # Remove any extra spaces
                if hasattr(self, command):  # If it's one of our predefined commands
                    self.add_command(getattr(self, command))
                else:
                    self.add_command(command)

        def __str__(self):
            return '\n'.join(self.commands) + '\n'
        
    class Card5:
        """Card5 class for the Sammy input file.
        """
        
        def __init__(self, config_file=None):
            # Default values
            self.TEMP = 0.0
            self.DIST = 0.0
            self.DELTAL = 0.0
            self.DELTAE = 0.0
            self.DELTAG = 0.0
            self.DELTTT = 0.0
            self.ELOWBR = 0.0

            if config_file:
                self._read_from_config(config_file)

        def _read_from_config(self, config_file):
            """Read the Card5 values from the config file using configparser.

            Args:
                config_file (string): Path to the configuration file.
            """
            config = configparser.ConfigParser()
            config.read(config_file)
            self.TEMP = config.getfloat('Card5', 'TEMP', fallback=self.TEMP)
            self.DIST = config.getfloat('Card5', 'DIST', fallback=self.DIST)
            self.DELTAL = config.getfloat('Card5', 'DELTAL', fallback=self.DELTAL)
            self.DELTAE = config.getfloat('Card5', 'DELTAE', fallback=self.DELTAE)
            self.DELTAG = config.getfloat('Card5', 'DELTAG', fallback=self.DELTAG)
            self.DELTTT = config.getfloat('Card5', 'DELTTT', fallback=self.DELTTT)
            self.ELOWBR = config.getfloat('Card5', 'ELOWBR', fallback=self.ELOWBR)

        def __str__(self):
            """String representation of Card5 for writing to the input file.

            Returns:
                string: String representation of Card5 for writing to the input file.
            """
            return (
                InputFile.format_type_F(self.TEMP, 10) +
                InputFile.format_type_F(self.DIST, 10) +
                InputFile.format_type_F(self.DELTAL, 10) +
                InputFile.format_type_F(self.DELTAE, 10) +
                InputFile.format_type_F(self.DELTAG, 10) +
                InputFile.format_type_F(self.DELTTT, 10) +
                InputFile.format_type_F(self.ELOWBR, 10)
            )

    class Card6:
        """Card6 class for the Sammy input file.
        """
        def __init__(self, card5_instance=None, config_file=None):
            """Initialize Card6 instance.

            Args:
                card5_instance (card5_instance, optional): Card5 instance. Defaults to None.
                config_file (string, optional): Path to the configuration file. Defaults to None.
            """
            self.DELTAG = card5_instance.DELTAG if card5_instance else 0.0
            self.DELTAB = 0.0
            self.NCF = 0
            self.BCF = []  # List of maximum energies for each crunch factor
            self.CF = []   # List of crunch factors

            if self.DELTAG < 0:
                if config_file:
                    self._read_from_config(config_file)

        def _read_from_config(self, config_file):
            """Read the Card6 values from the config file using configparser.

            Args:
                config_file (string): Path to the configuration file.
            """
            config = configparser.ConfigParser()
            config.read(config_file)
            
            self.DELTAB = config.getfloat('Card6', 'DELTAB', fallback=self.DELTAB)
            self.NCF = config.getint('Card6', 'NCF', fallback=self.NCF)
            
            for i in range(1, self.NCF + 1):
                bcf_key = f"BCF_{i}"
                cf_key = f"CF_{i}"
                
                bcf_value = config.getfloat('Card6', bcf_key, fallback=0.0)
                cf_value = config.getfloat('Card6', cf_key, fallback=0.0)
                
                self.BCF.append(bcf_value)
                self.CF.append(cf_value)

        def __str__(self):
            """String representation of Card6 for writing to the input file.

            Returns:
                string: String representation of Card6 for writing to the input file.
            """
            if self.DELTAG >= 0:
                return ""
            
            line1 = (
                InputFile.format_type_F(self.DELTAB, 10) +
                InputFile.format_type_I(self.NCF, 5)
            )
            
            line2 = ""
            for i in range(self.NCF):
                line2 += (
                    InputFile.format_type_F(self.BCF[i], 10) +
                    InputFile.format_type_F(self.CF[i], 10)
                )
            return line1 + "\n" + line2


    class Card7:
        
        def __init__(self, config_file=None):
            # Default values
            self.CRFN = 0.0
            self.THICK = 0.0
            self.DCOVA = 0.0
            self.DCOVB = 0.0
            self.VMIN = 0.0

            if config_file:
                self._read_from_config(config_file)

        def _read_from_config(self, config_file):
            config = configparser.ConfigParser()
            config.read(config_file)
            self.CRFN = config.getfloat('Card7', 'CRFN', fallback=self.CRFN)
            self.THICK = config.getfloat('Card7', 'THICK', fallback=self.THICK)
            self.DCOVA = config.getfloat('Card7', 'DCOVA', fallback=self.DCOVA)
            self.DCOVB = config.getfloat('Card7', 'DCOVB', fallback=self.DCOVB)
            self.VMIN = config.getfloat('Card7', 'VMIN', fallback=self.VMIN)

        def __str__(self):
            return (
                InputFile.format_type_F(self.CRFN, 10) +
                InputFile.format_type_F(self.THICK, 10) +
                InputFile.format_type_F(self.DCOVA, 10) +
                InputFile.format_type_F(self.DCOVB, 10) +
                InputFile.format_type_F(self.VMIN, 10)
            )
    
    class Card8:
        def __init__(self, config_file=None):
            """Initialize Card8 instance.

            Parameters:
            - config_file (str): Path to the configuration file.
            """
            self.CROSS = ""  # Default value
            
            if config_file:
                self._read_from_config(config_file)

        def _read_from_config(self, config_file):
            """Read the CROSS values from the config file using configparser.

            Args:
                config_file (_type_): Path to the configuration file.
            """

            config = configparser.ConfigParser()
            config.read(config_file)
            
            # Assuming the config file has a 'Card8' section with a single 'CROSS' key
            self.CROSS = config.get('Card8', 'CROSS', fallback=self.CROSS)[:80]

        def __str__(self):
            """String representation of Card8 for writing to the input file.

            Returns:
                String: String representation of Card8 for writing to the input file.
            """
            return "{:<80}".format(self.CROSS)
    
    class Card10:
        """ Card10 class for the Sammy input file.
        """
        def __init__(self, config_file=None):
            """Initialize Card10 instance.

            Args:
                config_file (string, optional): Path to the configuration file. Defaults to None.

            Raises:
                ValueError: If the number of isotopes and spin groups in the configuration file do not match.
            """
            self.isotopes = []
            self.spingroups = []
            
            if config_file:
                config = self.read_config(config_file)
                self.isotopes = config['Card10']['ISOTOPES'].split(',')
                self.spingroups = list(map(int, config['Card10']['SPINGROUPS'].split(',')))

                # Check if the lengths of isotopes and spin groups match
                if len(self.isotopes) != len(self.spingroups):
                    raise ValueError("The number of isotopes and spin groups in the configuration file do not match!")
                
        def read_config(self, config_file):
            """Read the Card10 values from the config file using configparser.

            Args:
                config_file (string): Path to the configuration file.

            Returns:
                configparser.ConfigParser: ConfigParser instance with the config file loaded.
            """
            config = configparser.ConfigParser()
            config.read(config_file)
            return config

        def create_spin_group_string(self):
            """Create the string representation of the spin group data for writing to the input file.

            Returns:
                string: String representation of the spin group data for writing to the input file.
            """
            spin_group_str = ""
            groupNum = 0
            
            for i, isotope in enumerate(self.isotopes):
                for j in range(self.spingroups[i]):
                    groupNum += 1
                    JJ = groupNum 
                    EXCL = " "  # Assuming a space for now, update if there's a default or provided value
                    NENT = 0    # Assuming 0 for now, update if there's a default or provided value
                    NEXT = 0    # Assuming 0 for now, update if there's a default or provided value
                    SPINJ = 0.0 # Assuming 0.0 for now, update if there's a default or provided value
                    ABNDNC = 0.0 # Assuming 0.0 for now, update if there's a default or provided value
                    SPINI = 0.0  # Assuming 0.0 for now, update if there's a default or provided value
                    Comments = isotope
                    
                    line = "{:3d}{}{:>5d}{:>5d}{:>5.2f}{:>10.2f}{:>5.2f}{:<35}\n".format(
                        JJ, EXCL, NENT, NEXT, SPINJ, ABNDNC, SPINI, Comments
                    )
                    spin_group_str += line
            
            return spin_group_str

        def __str__(self):
            return self.create_spin_group_string()

    
    
    
    def write_to_file(self, filename, *cards):
        """Write the input file to a file with the given filename and the given cards.

        Args:
            filename (string): file to write to
            cards (array): array of cards to write to file
        """
        with open(filename, 'w') as f:
            for card in cards:
                f.write(str(card) + "\n")
