def generate_sammy_input_file(filename, title, element, atomic_weight):
    """
    Generate an input file for a Fortran program.
    
    Parameters:
    - filename: the name of the file to save to.
    - title: a string (up to 80 characters) for the title.
    - element: a string (up to 10 characters) for the element name.
    - atomic_weight: a float for the atomic weight of the element.
    """
    with open(filename, 'w') as f:
        # Write the title (padded or truncated to 80 characters)
        f.write(f"{title:80}\n")
        
        # Write the element (padded or truncated to 10 characters) 
        # and atomic weight (formatted to occupy 10 columns)
        f.write(f"{element:10}{atomic_weight:10.4f}\n")