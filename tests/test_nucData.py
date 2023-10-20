from pleiades import nucData
from numpy import testing
import pytest



def test_get_mass_from_ame():
    isotopes = {'H-1':      1.0078,
                'B-10':    10.0129,
                'Be-9':     9.0122,
                'N-14':    14.0031,
                'Na-23':   22.9898,
                'P-31':    30.9738,
                'Ru-100':  99.9042,
                'Bi-210': 209.9841,
                'U-238':  238.0508,
                'Fm-255': 255.09}
    for iso in isotopes:
        testing.assert_equal(nucData.get_mass_from_ame(iso),isotopes[iso])

    # test wrong isotope names
    with pytest.raises(ValueError):
        nucData.get_mass_from_ame("C-19")
        nucData.get_mass_from_ame("UU-238")
        nucData.get_mass_from_ame("12C")
        nucData.get_mass_from_ame("C - 12")
        nucData.get_mass_from_ame("6-C-12")
        nucData.get_mass_from_ame("We-200")


def test_get_mat_number():
    isotopes = {'H-1':     125,
                'B-10':    525,
                'Be-9':    425,
                'N-14':    725,
                'Na-23':  1125,
                'P-31':   1525,
                'Ru-100': 4437,
                'Bi-210': 8329,
                'U-238':  9237,
                'Fm-255': 9936}
    
    for iso in isotopes:
        testing.assert_equal(nucData.get_mat_number(iso),isotopes[iso])

    # test wrong isotope names
    with pytest.raises(ValueError):
        nucData.get_mat_number("C-19")
        nucData.get_mat_number("UU-238")
        nucData.get_mat_number("12C")
        nucData.get_mat_number("C - 12")
        nucData.get_mat_number("6-C-12")
        nucData.get_mat_number("We-200")


