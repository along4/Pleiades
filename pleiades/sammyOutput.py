import pathlib
from typing import List, Str, Int, Union, Dict

class LptFile:
    # utilities to read and parse an LPT output file

    def __init__(self,filename: str) -> None:
        """Reads a .lpt file

        Args:
            filename (str): SAMMY output file with .lpt extension
        """
        self._filename = filename
        
        LPT_SEARCH_PATTERNS = {
            "input_file":dict(
                start_text=" Name of input file",
                skipped_rows=1,
                line_format="line.split()[1]"),
            "par_file":dict(
                start_text=" Name of parameter file",
                skipped_rows=1,
                line_format="line.split()[1]"),
            "Emin":dict(
                start_text=" Emin and Emax",
                skipped_rows=0,
                line_format="float(line.split()[4])"),
            "Emax":dict(
                start_text=" Emin and Emax",
                skipped_rows=0,
                line_format="float(line.split()[5])"),
            "thickness":dict(
                start_text=" Target Thickness=",
                skipped_rows=0,
                line_format="float(line.split()[2])"),
            "varied_params":dict(
                start_text=" Number of varied parameters",
                skipped_rows=0,
                line_format="int(line.split()[5])"),
            "reduced_chi2":dict(
                start_text=" CUSTOMARY CHI SQUARED DIVIDED",
                skipped_rows=0,
                line_format="float(line.split()[7])"),
            "time_elapsed":dict(
                start_text="                              Total time",
                skipped_rows=0,
                line_format="float(line.split()[3])"),
            }
    
        self.LPT_SEARCH_PATTERNS = LPT_SEARCH_PATTERNS
            

    def stats(self) -> dict:
        """parse and collect statistical data from a SAMMY.LPT file
        
        Returns (dict): formatted statistical data from the run
        """        
        stats = {}

        with open(self._filename,"r") as fid:
            for line in fid:
                for pattern_key in self.LPT_SEARCH_PATTERNS:
                    pattern = self.LPT_SEARCH_PATTERNS[pattern_key]    
                    if line.startswith(pattern["start_text"]):
                        [line:=next(fid) for row in range(pattern["skipped_rows"])]
                        stats[pattern_key] = eval(pattern["line_format"])

        return stats
    

    def register_new_stats(self,keyname: str, first_line: str, skipped_rows: str, line_format: str ) -> None:
        """
        Registers a search pattern for parsing statistical values from the .lpt file.

        Args:
            - keyname (str): The name of the requested parameter.
            - first_line (str): A string used for line.startswith search to identify relevant lines.
            - skipped_rows (int): The number of rows to skip from the 'first_line' during parsing.
            - line_format (str): Python code snippet used to parse the line for the requested value.
                                Typically, this would be a split method on the input `line` variable.

        Example:
        Register a search pattern for temperature values in the .lpt file:
        >>> from pleiades import sammyOutput
        >>> sammyOutput.register_search_pattern(keyname="temperature", first_line="  TEMPERATURE",
                                                skipped_rows=1, line_format="float(line.split()[0])")
        """
        self.LPT_SEARCH_PATTERNS[keyname] = dict(first_line=first_line,
                                                 skipped_rows=skipped_rows,
                                                 line_format=line_format)

    def commands(self) -> list:
        """parse and collect the alphanumeric command cards from a SAMMY.LPT file
        
            Returns (list): of alphanumeric commands used in SAMMY run
        """        
        with open(self._filename,"r") as fid:
            for line in fid:
                if line.startswith(" *********** Alphanumeric Control Information"):
                    line = next(fid)
                    cards = []
                    while not line.startswith(" **** end"):
                        if line.strip():
                            cards.append(line.replace("\n","").strip())
                        line = next(fid)
                        
        return cards

