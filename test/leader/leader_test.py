from os import path

import sys
import unittest

FILE_PATH = path.dirname(path.realpath(__file__))
sys.path.append(FILE_PATH + "/../../src")

from leader import Leader
from leader import MAX_SPEED

class LeaderTest(unittest.TestCase):

    def test_set_speed_at_lower_bound(self):
        leader = Leader(test_mode=True)
        self.assertEqual(0, leader.set_speed(-1.0))


    def test_set_speed_below_lower_bound(self):
        leader = Leader(test_mode=True)
        self.assertEqual(0, leader.set_speed(-1.1))


    def test_set_speed_at_upper_bound(self):
        leader = Leader(test_mode=True)
        self.assertEqual(MAX_SPEED, leader.set_speed(1.0))


    def test_set_speed_above_upper_bound(self):
        leader = Leader(test_mode=True)
        self.assertEqual(MAX_SPEED, leader.set_speed(1.1))


    def test_set_speed_zero_position(self):
        leader = Leader(test_mode=True)
        self.assertEqual(MAX_SPEED / 2, leader.set_speed(0.0))


    def test_set_speed_none_position(self):
        leader = Leader(test_mode=True)
        self.assertEqual(0, leader.set_speed(None))


    def test_set_speed_string_position(self):
        leader = Leader(test_mode=True)
        self.assertEqual(0, leader.set_speed("position"))


    def test_turn_position_at_lower_bound(self):
        leader = Leader(test_mode=True)
        self.assertEqual(45, leader.turn(-1.0))


    def test_turn_position_below_lower_bound(self):
        leader = Leader(test_mode=True)
        self.assertEqual(45, leader.turn(-1.1))


    def test_turn_position_at_upper_bound(self):
        leader = Leader(test_mode=True)
        self.assertEqual(135, leader.turn(1.0))


    def test_turn_position_above_upper_bound(self):
        leader = Leader(test_mode=True)
        self.assertEqual(135, leader.turn(1.1))


    def test_turn_position_zero(self):
        leader = Leader(test_mode=True)
        self.assertEqual(90, leader.turn(0.0))


    def test_turn_position_type_errro(self):
        leader = Leader(test_mode=True)
        self.assertEqual(None, leader.turn(None))


    def test_turn_position_value_error(self):
        leader = Leader(test_mode=True)
        self.assertEqual(None, leader.turn("position"))


if __name__ == '__main__':
    unittest.main()
