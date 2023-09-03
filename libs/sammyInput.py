import configparser

class InputFile:

    MAX_COLUMNS = 80
    
    @staticmethod
    def format_type_A(data, width):
        return f"{data:<{width}}"

    @staticmethod
    def format_type_F(data, width):
        # The ".4f" here denotes 4 decimal places. You can adjust if needed.
        return f"{data:>{width}.4f}"

    @staticmethod
    def format_type_I(data, width):
        return f"{data:>{width}d}"

    class Card1:
        def __init__(self, config_file=None):
            self.TITLE = "Blank Sammy Input File Title"
            if config_file:
                self._read_from_config(config_file)
        
        def set(self, TITLE):
            self.TITLE = TITLE
        
        def _read_from_config(self, config_file):
            config = configparser.ConfigParser()
            config.read(config_file)
            self.TITLE = config.get('Card1', 'TITLE', fallback=self.TITLE)
            
        def __str__(self):
            return InputFile.format_type_A(self.TITLE, InputFile.MAX_COLUMNS)

    class Card2:
        def __init__(self, config_file=None):
            # Default values
            self.ELMNT = "none"     # Element name
            self.AW = 0         # Atomic weight
            self.EMIN = 0       # Minimum energy
            self.EMAX = 0       # Maximum energy
            self.NEPNTS = 0     # Number of points to be used in generating artificial energy grid
            self.ITMAX = 0      # Number of iterations (default = 2)
            self.ICORR = 0      # Correlation option (default = 50)
            self.NXTRA = 0      # Number of extra points to be added between each pair of data points for auxiliary energy grid
            self.IPTDOP = 0     # Number of points to be added to auxiliary energy grid across small resonances
            self.IPTWID = 0     # Determines the number of points to be added to auxiliary grid in tails of small resonances
            self.IXXCHN = 0     # Number of energy channels in ODF-type data file to be ignored
            self.NDIGIT = 0     # Number of digits for compact format for covariance matrix
            self.IDROPP = 0     # The input resonanceparameter covariance matrix will be modified before being used in the fitting procedure.
            self.MATNUM = 0     # ENDF Material number

            if config_file:
                self._read_from_config(config_file)
            
        def set(self, ELMNT=None, AW=None, EMIN=None, EMAX=None, NEPNTS=None, ITMAX=None, ICORR=None, NXTRA=None, IPTDOP=None, IPTWID=None, IXXCHN=None, NDIGIT=None, IDROPP=None, MATNUM=None):
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
            return (
                InputFile.format_type_F(self.TEMP, 10) +
                InputFile.format_type_F(self.DIST, 10) +
                InputFile.format_type_F(self.DELTAL, 10) +
                InputFile.format_type_F(self.DELTAE, 10) +
                InputFile.format_type_F(self.DELTAG, 10) +
                InputFile.format_type_F(self.DELTTT, 10) +
                InputFile.format_type_F(self.ELOWBR, 10)
            )


    def write_to_file(self, filename, *cards):
        """_summary_

        Args:
            filename (_type_): _description_
        """
        with open(filename, 'w') as f:
            for card in cards:
                f.write(str(card) + "\n")
