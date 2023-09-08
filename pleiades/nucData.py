import numpy as np

def extract_isotope_info(filename, isotope):
    """This function extracts the spin and abundance of an isotope from the file isotope.info.

    Args:
        filename (_type_): isotope.info file location
        isotope (string): String of the form "element-nucleonNumber" (e.g. "C-13")

    Returns:
        _type_: spin and natural abundance of the isotope
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespaces
            if line and line[0].isdigit():  # Check if the line contains isotope data
                data = line.split()  # Split the line into columns based on spaces
                
                symbol = data[3]  # Extract the element symbol
                numOfNucleons = data[1]  # Extract the number of nucleons
                
                if isotope == f"{symbol}-{numOfNucleons}":  # Check if the isotope matches
                    spin = data[5]
                    abundance = data[7]
                    return spin, abundance
    return None, None

def parse_ame_line(line):
    def safe_float(val, default="nan"):
        return float(val if val.strip() else default)

    def safe_int(val, default=0):
        return int(val if val.strip() else default)

    # Extracting values based on their fixed positions
    cc = line[0]
    NZ = safe_int(line[2:5])
    N = safe_int(line[5:9])
    Z = safe_int(line[9:14])
    A = safe_int(line[14:19])
    el = line[20:23].strip()
    o = line[23:27].strip()
    mass = safe_float(line[28:42].replace("*", "nan").replace("#", ".0"))
    mass_unc = safe_float(line[42:54].replace("*", "nan").replace("#", ".0"))
    binding = safe_float(line[55:68].replace("*", "nan").replace("#", ".0"))
    bind_unc = safe_float(line[69:79].replace("*", "nan").replace("#", ".0"))
    B = line[79:81].strip()
    beta = safe_float(line[82:93].replace("*", "nan").replace("#", ".0"))
    beta_unc = safe_float(line[95:106].replace("*", "nan").replace("#", ".0"))

    atomic_mass_coarse = line[106:109].replace("*", "nan").replace("#", ".0")
    atomic_mass_fine = line[111:124].replace("*", "nan").replace("#", ".0")

    # Check if both coarse and fine are not NaN before converting
    if "nan" not in [atomic_mass_coarse, atomic_mass_fine]:
        atomic_mass = float(atomic_mass_coarse + atomic_mass_fine)
    else:
        atomic_mass = float("nan")

    atomic_mass_unc = safe_float(line[124:136].replace("*", "nan").replace("#", ".0"))

    return {
        "cc": cc,
        "NZ": NZ,
        "N": N,
        "Z": Z,
        "A": A,
        "el": el,
        "o": o,
        "mass": mass,
        "mass_unc": mass_unc,
        "binding": binding,
        "bind_unc": bind_unc,
        "B": B,
        "beta": beta,
        "beta_unc": beta_unc,
        "atomic_mass": atomic_mass,
        "atomic_mass_unc": atomic_mass_unc
    }


def get_info(isotopic_str):
    # Extract the element and its atomic number from the isotopic string
    element = ''.join([c for c in isotopic_str if not c.isdigit()])
    atomic_number = int(''.join([c for c in isotopic_str if c.isdigit()]))

    return element, atomic_number

def get_mass_from_ame(isotopic_str):
    
    possible_isotopes_data_list = []

    element, atomic_number = get_info(isotopic_str)
    # Load the file into a list of lines
    with open("mass.mas20", "r") as f:
        
        # Skip the first 36 lines of header info
        for _ in range(36):
            next(f)

        # start searching through lines.
        for line in f:
            if (element in line[:25]) and (str(atomic_number) in line[:25]):
                possible_isotopes_data = parse_ame_line(line)
                possible_isotopes_data_list.append(possible_isotopes_data)

        for iso in possible_isotopes_data_list:
            if (iso['el'] == element) and (iso['A'] == atomic_number):
                final_atomic_mass = iso['atomic_mass']

    return(final_atomic_mass)