

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
        def __init__(self, TITLE):
            self.TITLE = TITLE

        def __str__(self):
            return InputFile.format_type_A(self.TITLE, InputFile.MAX_COLUMNS)

    class Card2:
        def __init__(self, ELMNT, AW, EMIN, EMAX, NEPNTS, ITMAX, ICORR, NXTRA, IPTDOP, IPTWID, IXXCHN, NDIGIT, IDROPP, MATNUM):
            self.ELMNT = ELMNT      # Element name
            self.AW = AW            # Atomic weight
            self.EMIN = EMIN        # Minimum energy
            self.EMAX = EMAX        # Maximum energy
            self.NEPNTS = NEPNTS    # Number of points to be used in generating artificial energy grid
            self.ITMAX = ITMAX      # Number of iterations (default = 2)
            self.ICORR = ICORR      # Correlation option (default = 50)
            self.NXTRA = NXTRA      # Number of extra points to be added between each pair of data points for auxiliary energy grid
            self.IPTDOP = IPTDOP    # Number of points to be added to auxiliary energy grid across small resonances
            self.IPTWID = IPTWID    # Determines the number of points to be added to auxiliary grid in tails of small resonances
            self.IXXCHN = IXXCHN    # Number of energy channels in ODF-type data file to be ignored
            self.NDIGIT = NDIGIT    # Number of digits for compact format for covariance matrix
            self.IDROPP = IDROPP    # The input resonanceparameter covariance matrix will be modified before being used in the fitting procedure.
            self.MATNUM = MATNUM    # ENDF Material number

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

    def write_to_file(self, filename, *cards):
        """_summary_

        Args:
            filename (_type_): _description_
        """
        with open(filename, 'w') as f:
            for card in cards:
                f.write(str(card) + "\n")
