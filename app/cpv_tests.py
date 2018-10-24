from cpv import CPV
import unittest

class CPVTest(unittest.TestCase):
    """A simple test of the  CPV system using pregenerated test files."""

    def setUp(self):

        self.test_rotations = 'test_files/test_rotations.csv'
        self.test_spots = 'test_files/test_spots.csv'
        self.cpv = CPV(self.test_spots, self.test_rotations)

    def test_cpv_by_creative(self):

        cpv_by_creative = self.cpv.cpv_by_creative()
        expected_result = {'SPOT1': 1}
        self.assertEqual(cpv_by_creative, expected_result)

    def test_cpv_by_rotation_by_day(self):

        cpv_by_rotation_by_day = self.cpv.cpv_by_rotation_by_day()
        expected_result = { 'Afternoon': {'10/23/2018': 1.5 },
                            'Morning': {'10/23/2018': 0.8333333333333334 },
                            'Prime': {'10/23/2018': 0}
                            }
        self.assertEqual(cpv_by_rotation_by_day, expected_result)


if __name__ == '__main__':
    unittest.main()
