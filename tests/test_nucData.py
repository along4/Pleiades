from pleiades import nucData
from numpy import testing

def test_get_mass_from_ame():
    testing.assert_approx_equal(nucData.get_mass_from_ame("C-12"),12)
    testing.assert_approx_equal(nucData.get_mass_from_ame("U-238"),238.0508)

def test_get_mat_number():
    testing.assert_equal(nucData.get_mat_number("Li-6"),325)
    testing.assert_equal(nucData.get_mat_number("F-19"),925)

