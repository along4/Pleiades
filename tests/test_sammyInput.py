from pleiades import sammyInput
from numpy import testing
import pytest
import configparser
import pathlib

# current directory location
PWD = pathlib.Path(__file__).parent

def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

@pytest.fixture
def config_file():
    return PWD / 'config.ini'

@pytest.fixture
def config(config_file):
    return load_config(config_file)

@pytest.fixture
def inputFile():
    return sammyInput.InputFile()

def test_card_sections_exist(config):
    for card_number in [1, 2, 3, 5, 7, 8, 10]:
        card_name = f'Card{card_number}'
        assert card_name in config

def test_class_card1(inputFile,config_file):
    card1 = inputFile.Card1(config_file)
    assert hasattr(card1,"TITLE")
    assert type(card1.TITLE)==str

def test_class_card2(inputFile,config_file):
    card2 = inputFile.Card2(config_file)
    attrs_and_types = {'AW': float,
                       'ELMNT': str,
                       'EMAX': float,
                       'EMIN': float,
                       'ICORR': int,
                       'IDROPP': int,
                       'IPTDOP': int,
                       'IPTWID': int,
                       'ITMAX': int,
                       'IXXCHN': int,
                       'MATNUM': int,
                       'NDIGIT': int,
                       'NEPNTS': int,
                       'NXTRA': int}
    for attr in attrs_and_types:
        assert hasattr(card2,attr)
        assert type(card2.__getattribute__(attr))==attrs_and_types[attr]

def test_class_card3(inputFile,config_file):
    card3 = inputFile.Card3(config_file)
    assert hasattr(card3,"commands")
    assert type(card3.commands)==list
    for command in card3.commands:
        assert type(command)==str

def test_class_card5(inputFile,config_file):
    card5 = inputFile.Card5(config_file)
    attrs_and_types = {'DELTAE': float,
                       'DELTAG': float,
                       'DELTAL': float,
                       'DELTTT': float,
                       'DIST': float,
                       'ELOWBR': float,
                       'TEMP': float}
    for attr in attrs_and_types:
        assert hasattr(card5,attr)
        assert type(card5.__getattribute__(attr))==attrs_and_types[attr]

def test_class_card6(inputFile,config_file):
    card5 = inputFile.Card5(config_file)
    card6 = inputFile.Card6(card5,config_file)
    attrs_and_types = {'BCF': list,
                       'CF': list,
                       'DELTAB': float,
                       'DELTAG': float,
                       'NCF': int}
    for attr in attrs_and_types:
        assert hasattr(card6,attr)
        assert type(card6.__getattribute__(attr))==attrs_and_types[attr]

def test_class_card8(inputFile,config_file):
    card8 = inputFile.Card8(config_file)
    assert hasattr(card8,"CROSS")
    assert type(card8.CROSS)==str
    assert card8.CROSS.upper() in ["TRANSMISSION","CAPTURE","TOTAL"] # TODO: update the other options 

def test_class_card10(inputFile,config_file):
    card10 = inputFile.Card10(config_file)
    assert hasattr(card10,"isotopes")
    assert type(card10.isotopes)==list
    assert hasattr(card10,"spingroups")
    assert type(card10.isotopes)==list

def test_run_sammy():
    pass # TODO: add a real run of sammy to test the input
