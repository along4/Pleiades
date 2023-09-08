import configparser

def parse_xs_file(file_location, isotope_name):
    xs_data = []
    isotope_xs_found = False
    capture_data = False
    with open(file_location, 'r') as f:
        for line in f:
            # If we find the name of the isotope
            if isotope_name in line:
                isotope_xs_found = True
            # If we have found the isotope, then look for the "#data..." marker
            if isotope_xs_found:
                if "#data..." in line:
                    capture_data = True
                # If we find the "//" line, stop capturing data
                elif '//' in line:
                    capture_data = False
                    break
                # If capture_data is True and the line doesn't start with a '#', then it's the data
                elif capture_data and not line.startswith("#"):
                    energy, xs = line.split()
                    xs_data.append((float(energy), float(xs)))
                
                
    # If the loop completes and the isotope was not found
    if not isotope_xs_found:
        raise ValueError(f"Cross-section data for {isotope_name} not found in {file_location}")

    return xs_data



class Isotope:
    def __init__(self, name="Unknown", thickness=0.0, thickness_unit="atoms/cm2", abundance=0.0, xs_file_location="Unknown", density=0.0, density_unit="g/cm3"):
        self.name = name
        self.thickness = thickness
        self.thickness_unit = thickness_unit
        self.abundance = abundance
        self.xs_file_location = xs_file_location
        self.density = density
        self.density_unit = density_unit
        self.xs_data = []  # Array to hold xs data
        
    def load_xs_data(self):
        """Load cross-section data from file."""
        self.xs_data = parse_xs_file(self.xs_file_location, self.name)
        if not self.xs_data:
            raise ValueError(f"No data loaded for {self.name} from {self.xs_file_location}")
    
    def __repr__(self):
        xs_status = "XS data loaded successfully" if len(self.xs_data) != 0 else "XS data not loaded"
        return f"Isotope({self.name}, {self.thickness} {self.thickness_unit}, {self.abundance}, {self.xs_file_location}, {self.density} {self.density_unit}, {xs_status})"

class Isotopes:
    def __init__(self, config_file):
        self.isotopes = []
        config = configparser.ConfigParser()
        config.read(config_file)

        # Create a dummy Isotope instance to get the default values
        default_isotope = Isotope()

        for section in config.sections():
            # Check if the ignore flag is set for this isotope
            ignore = config.getboolean(section, 'ignore', fallback=False)
            if ignore:
                continue
            
            # Fetch each attribute with the default value from the dummy Isotope instance
            name = config.get(section, 'name', fallback=default_isotope.name)
            thickness = config.getfloat(section, 'thickness', fallback=default_isotope.thickness)
            thickness_unit = config.get(section, 'thickness_unit', fallback=default_isotope.thickness_unit)
            abundance = config.getfloat(section, 'abundance', fallback=default_isotope.abundance)
            xs_file_location = config.get(section, 'xs_file_location', fallback=default_isotope.xs_file_location)
            density = config.getfloat(section, 'density', fallback=default_isotope.density)
            density_unit = config.get(section, 'density_unit', fallback=default_isotope.density_unit)

            isotope = Isotope(name, thickness, thickness_unit, abundance, xs_file_location, density, density_unit)
            isotope.load_xs_data()  # Load xs data for the isotope
            self.isotopes.append(isotope)

    def __repr__(self):
        return "\n".join([str(isotope) for isotope in self.isotopes])

