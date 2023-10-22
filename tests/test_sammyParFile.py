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
        assert par.particle_pair_data[0]["Name"].startswith((PWD / filename).stem)

def test_spingroup_loopback():
    # tests if I can read and write a particle pair card and get the same card back
    par = sammyParFile.ParFile(PWD / "Ta_181.par")
    par.read()

    sg_dict = par._read_spingroup(par.spingroup_cards[0])
    loopback = par._write_spingroup(sg_dict)
    assert loopback.strip()==par.spingroup_cards[0].strip()

    sc_dict = par._read_spinchannel(par.spingroup_cards[1])
    loopback = par._write_spinchannel(sc_dict)
    assert loopback.strip()==par.spingroup_cards[1].strip()

    # another group from another isotope
    par = sammyParFile.ParFile(PWD / "U_235.par")
    par.read()

    sg_dict = par._read_spingroup(par.spingroup_cards[0])
    loopback = par._write_spingroup(sg_dict)
    assert loopback.strip()==par.spingroup_cards[0].strip()

    sc_dict = par._read_spinchannel(par.spingroup_cards[3])
    loopback = par._write_spinchannel(sc_dict)
    assert loopback.strip()==par.spingroup_cards[3].strip()   

