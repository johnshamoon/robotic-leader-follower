from os import path

import sys
import unittest

FILE_PATH = path.dirname(path.realpath(__file__))
sys.path.append(FILE_PATH + "/../../src")

from leader import Leader

class LeaderTest(unittest.TestCase):
    def test_set_speed_lower_bound(self):
        leader = Leader()
        self.assertEqual(leader.set_speed(-1), 0)


    def test_set_speed_upper_bound(self):
        leader = Leader()
        self.assertEqual(leader.set_speed(1) , 50)


    def test_set_speed_zero(self):
        leader = Leader()
        self.assertEqual(leader.set_speed(0) , 50/2)


    def test_set_speed_above_upper_bound(self):
        leader = Leader()
        self.assertEqual(leader.set_speed(2) , 50)


    def test_set_speed_below_lower_bound(self):
        leader = Leader()
        self.assertEqual(leader.set_speed(-2) , 0)


    def test_set_speed_none(self):
        leader = Leader()
        self.assertEqual(leader.set_speed(None) , 0)


    def test_drive_max_speed(self):
        leader = Leader()
        self.assertEqual(leader.set_speed(1) , 50)


    def test_drive_zero_speed(self):
        leader = Leader()
        self.assertEqual(leader.set_speed(-1) , 0)


    def test_reverse_max_speed(self):
        leader = Leader()
        self.assertEqual(leader.set_speed(1) , 50)


    def test_reverse_zero_speed(self):
        leader = Leader()
        self.assertEqual(leader.set_speed(-1) , 0)


if __name__ == '__main__':
    unittest.main()
    