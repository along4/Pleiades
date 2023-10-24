from pleiades import sammyParFile
from numpy import testing
import pytest
import pathlib

PWD = pathlib.Path(__file__).parent

def test_read_and_parse_par_file():
    files = ["Ta_181.par","Eu_151.par","Eu_153.par","U_235.par"]

    for filename in files:
        par = sammyParFile.ParFile(PWD / filename)
        par.read()

        # tests if the naming of the particle pair is correct in "auto" rename mode
        assert par._particle_pair_data[0]["Name"].startswith((PWD / filename).stem)

        for key in ['particle_pair', 'spin_group', 'channel_group', 'channel_radii']:
            assert key in par.par_file_data.keys() 

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


def test_channel_group_loopback():
    # tests if I can read and write a channel_group card and get the same card back
    par = sammyParFile.ParFile(PWD / "U_235.par")
    par.read()

    # original line: 'Group=2 Chan=1, 2, 3,'
    original_line = par._channel_group_cards[1]
    converted_line = par._write_channel_group(par.par_file_data["channel_group"][1])
    assert original_line==converted_line

    # original line: 'Group=11 Chan=1,'
    original_line = par._channel_group_cards[10]
    converted_line = par._write_channel_group(par.par_file_data["channel_group"][10])
    assert original_line==converted_line


def test_channel_radii_loopback():
    # tests if I can read and write a channel_radii card and get the same card back
    par = sammyParFile.ParFile(PWD / "U_235.par")
    par.read()

    # original line: 'Radii= 9.602, 9.602    Flags= 0, 0'
    original_line = par._channel_radii_cards
    converted_line = par._write_channel_radii(par.par_file_data["channel_radii"])
    assert original_line==converted_line
    

