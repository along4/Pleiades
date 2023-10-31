import pathlib
import inspect
import glob
import time

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
    shutil.move(archivepath /'SAMMY.PAR', archivepath / f'results/{archivename}.par')
    shutil.move(archivepath /'SAMMY.LST', archivepath / f'results/{archivename}.lst')
    shutil.move(archivepath /'SAMMY.LPT', archivepath / f'results/{archivename}.lpt')
    shutil.move(archivepath /'SAMMY.IO', archivepath / f'results/{archivename}.io')

    # remove SAM*.*
    filelist = glob.glob(f"{archivepath}/SAM*")
    for f in filelist:
        os.remove(f)

    return


def run_endf(inpfile: str = "") -> None:
    """
    run sammy input with endf isotopes tables file to create a par file
    - This can only be done for a single isotope at a time
    - we don't need a data file, we create a fake dat file with only Emin and Emax data points
    - archive path name will be deducd from input name

    Args:
        inpfile (str): input file name
    """    
    import os
    import shutil

    archivename = inpfile.split(".")[0]

    archivepath = pathlib.Path(f"archive/{archivename}") 

    # create an archive directory
    os.makedirs(archivepath,exist_ok=True)
    os.makedirs(archivepath / "results",exist_ok=True)


    # copy files into archive
    shutil.copy(inpfile, archivepath / f'{archivename}.inp')
    inpfile = f'{archivename}.inp'

    # read the input file to get the Emin and Emax:
    with open(inpfile) as fid:
        next(fid)
        Emin, Emax = next(fid).split()[2:4]

    # write a fake datafile with two entries of Emin and Emax
    with open(archivepath / f'{archivename}.dat',"w") as fid:
        fid.write(f"{Emax} 0 0\n")
        fid.write(f"{Emin} 0 0\n")
    
    datafile = f'{archivename}.dat'

    endffile = pathlib.Path(__file__).parent.parent / "nucDataLibs/resonanceTables/res_endf8.endf"
    try:
        os.symlink(endffile,archivepath / 'res_endf8.endf')
    except FileExistsError:
        pass
    endffile = 'res_endf8.endf'

    outputfile = f'{archivename}.out'

    run_command = f"""sammy > {outputfile} 2>/dev/null << EOF
                      {inpfile}
                      {endffile}
                      {datafile}

                      EOF 
                      """
    run_command = inspect.cleandoc(run_command) # remove indentation
    
    pwd = pathlib.Path.cwd()

    os.chdir(archivepath)
    os.system(run_command) # run sammy
    os.chdir(pwd)

    # move files
    shutil.move(archivepath /'SAMNDF.PAR', archivepath / f'results/{archivename}.par')
    shutil.move(archivepath /'SAMNDF.INP', archivepath / f'results/{archivename}.inp')
    shutil.move(archivepath /'SAMMY.LPT', archivepath / f'results/{archivename}.lpt')


    # remove SAM*.*
    filelist = glob.glob(f"{archivepath}/SAM*")
    for f in filelist:
        os.remove(f)

    return


