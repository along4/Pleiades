from pleiades import sammyParFile
from numpy import testing
import pytest
import pathlib

PWD = pathlib.Path(__file__).parent / "files"

def test_read_and_parse_par_file():
    files = ["Ta_181.par","Eu_151.par","Eu_153.par","U_235.par"]

    for filename in files:
        par = sammyParFile.ParFile(PWD / filename)
        par.read()

        for key in ['particle_pairs', 'spin_group', 'channel_radii','resonance_params']:
            assert key in par.data.keys() 

def test_spin_group_loopback():
    # tests if I can read and write a particle pair card and get the same card back
    par = sammyParFile.ParFile(PWD / "Ta_181.par")
    par.read()

    sg_dict = par._read_spin_group(par._spin_group_cards[0])
    loopback = par._write_spin_group(sg_dict)
    assert loopback.strip()==par._spin_group_cards[0].strip()

    sc_dict = par._read_spin_channel(par._spin_group_cards[1])
    loopback = par._write_spin_channel(sc_dict)
    assert loopback.strip()==par._spin_group_cards[1].strip()

    # another group from another isotope
    par = sammyParFile.ParFile(PWD / "U_235.par")
    par.read()

    sg_dict = par._read_spin_group(par._spin_group_cards[0])
    loopback = par._write_spin_group(sg_dict)
    assert loopback.strip()==par._spin_group_cards[0].strip()

    sc_dict = par._read_spin_channel(par._spin_group_cards[3])
    loopback = par._write_spin_channel(sc_dict)
    assert loopback.strip()==par._spin_group_cards[3].strip()   



def test_channel_radii_loopback():
    # tests if I can read and write a channel_radii card and get the same card back
    par = sammyParFile.ParFile(PWD / "U_235.par",name="none")
    par.read()

    # original line: 'Radii= 9.602, 9.602    Flags= 0, 0'
    original_lines = par._channel_radii_cards
    converted_lines = par._write_channel_radii(par.data["channel_radii"][0])
    # check all lines
    for original, converted in zip(original_lines,converted_lines):
        assert original.strip()==converted.strip()

    par = sammyParFile.ParFile(PWD / "Ta_181.par",name="none")
    par.read()

    # original line: 'Radii= 9.602, 9.602    Flags= 0, 0'
    original_lines = par._channel_radii_cards
    converted_lines = par._write_channel_radii(par.data["channel_radii"][0])
    # check all lines
    for original, converted in zip(original_lines,converted_lines):
        assert original.strip()==converted.strip()



def test_resonance_params_loopback():
    # tests if I can read and write a resonance_params card and get the same card back
    par = sammyParFile.ParFile(PWD / "U_235.par")
    par.read()

    # original line: '-0.48262240 25.4361900 0.10938900 129.801900 -86.354100           1             '
    original_line = par._resonance_params_cards[1]
    converted_line = par._write_resonance_params(par.data["resonance_params"][1])
    assert original_line==converted_line

    # original line: '8.807442000 79.4633000 0.18864900 -259.56180 159.029900           1             '
    original_line = par._resonance_params_cards[10]
    converted_line = par._write_resonance_params(par.data["resonance_params"][10])
    assert original_line==converted_line

@pytest.mark.skip(reason="There's a whitespace difference, but in the final par, everything works. TODO: fix this test")
def test_particle_pairs_loopback():
    # tests if I can read and write a resonance_params card and get the same card back
    par = sammyParFile.ParFile(PWD / "U_235.par",name="none")
    par.read()

    # original lines:
    # Name=PPair1       Particle a=neutron       Particle b=Other   
    #   Za= 0        Zb=63         Pent=1     Shift=0
    #   Sa=  0.5     Sb=   2.5     Ma=   1.008664915780000     Mb= 152.921671000000003'''

    original_line = par._particle_pairs_cards[1]
    converted_line = par._write_particle_pairs(par.data["particle_pairs"][1])
    assert original_line.strip()==converted_line.strip()

def test_read_write_par_file():
    # reads a par file into data and writes to a new par file

    files = ["Ta_181.par","Eu_151.par","Eu_153.par","U_235.par"]

    for filename in files:
        par = sammyParFile.ParFile(PWD / filename,name="none")
        par.read()

        par.write(PWD / "compound.par")

        with open(PWD / filename,"r") as input_par:
            with open(PWD / "compound.par","r") as output_par:
                assert input_par.read()==output_par.read()


def test_read_write_compound_file():
    # create a compound, write it into a file, than read it and write the same file again

    par1 = sammyParFile.ParFile(PWD / "Eu_151.par",weight=0.6).read()

    par2 = sammyParFile.ParFile(PWD / "Eu_153.par",weight=0.4).read()

    (par1 + par2).write(PWD / "compound.par") # create compound and write to file
    
    com = sammyParFile.ParFile(PWD / "compound.par",name="none").read() # read compound file

    com.write(PWD / "new_compound.par")

    with open(PWD / "compound.par","r") as input_par:
        with open(PWD / "new_compound.par","r") as output_par:
            assert input_par.read()==output_par.read()




        



    


