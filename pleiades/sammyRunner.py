import pathlib
import inspect
import glob
import time

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
    }


def run(archivename: str="example",
            inpfile: str = "",
            parfile: str = "",
            datafile: str = "") -> None:
    """run the sammy program inside an archive directory

    Args:
        archivename (str): archive directory name. If only archivename is provided
                           the other file names will be assumed to have the same name 
                           at the archive has with the associate extension, e.g. {archivename}.inp
        inpfile (str, optional): input file name
        parfile (str, optional): parameter file name
        datafile (str, optional): data file name
    """
    
    import os
    import shutil

    if not inpfile:
        inpfile = f"{archivename}.inp"
    if not parfile:
        parfile = f"{archivename}.par"
    if not datafile:
        datafile = f"{archivename}.dat"

    archivepath = pathlib.Path(f"archive/{archivename}") 

    # create an archive directory
    os.makedirs(archivepath,exist_ok=True)
    os.makedirs(archivepath / "results",exist_ok=True)


    # copy files into archive
    shutil.copy(inpfile, archivepath / f'{archivename}.inp')
    inpfile = f'{archivename}.inp'
    shutil.copy(parfile, archivepath / f'{archivename}.par')
    parfile = f'{archivename}.par'
    shutil.copy(datafile, archivepath / f'{archivename}.dat')
    datafile = f'{archivename}.dat'

    outputfile = f'{archivename}.out'

    run_command = f"""sammy > {outputfile} 2>/dev/null << EOF
                      {inpfile}
                      {parfile}
                      {datafile}

                      EOF 
                      """
    run_command = inspect.cleandoc(run_command) # remove indentation
    
    pwd = pathlib.Path.cwd()

    os.chdir(archivepath)
    os.system(run_command) # run sammy
    os.chdir(pwd)

    # move files
    shutil.move(archivepath /'SAMQUA.PAR', archivepath / f'results/{archivename}.par')
    shutil.move(archivepath /'SAMMY.LST', archivepath / f'results/{archivename}.lst')
    shutil.move(archivepath /'SAMMY.LPT', archivepath / f'results/{archivename}.lpt')
    shutil.move(archivepath /'SAMMY.IO', archivepath / f'results/{archivename}.io')

    # remove SAM*.*
    filelist = glob.glob(f"{archivepath}/SAM*")
    for f in filelist:
        os.remove(f)

    return


def lpt_stats(lptfile: str) -> dict:
    """parse and collect statistical data from a SAMMY.LPT file

        Args: 
            - lptfile (str): file name of the lpt file produced in a succesful SAMMY run
    
        Returns (dict): formatted statistical data from the run
    """        
    stats = {}

    with open(lptfile,"r") as fid:
        for line in fid:
            for pattern_key in LPT_SEARCH_PATTERNS:
                pattern = LPT_SEARCH_PATTERNS[pattern_key]    
                if line.startswith(pattern["start_text"]):
                    [line:=next(fid) for row in range(pattern["skipped_rows"])]
                    stats[pattern_key] = eval(pattern["line_format"])

    return stats




def lpt_command_cards(lptfile: str) -> list:
    """parse and collect the alphanumeric command cards from a SAMMY.LPT file

        Args: 
            - lptfile (str): file name of the lpt file produced in a succesful SAMMY run
    
        Returns (list): of alphanumeric commands used in SAMMY run
    """        
    with open(lptfile,"r") as fid:
        for line in fid:
            if line.startswith(" *********** Alphanumeric Control Information"):
                line = next(fid)
                cards = []
                while not line.startswith(" **** end"):
                    if line.strip():
                        cards.append(line.replace("\n","").strip())
                    line = next(fid)
                    
    return cards

