from os import path

import sys
import unittest

FILE_PATH = path.dirname(path.realpath(__file__))
sys.path.append(FILE_PATH + "/../../src")

from follower import Follower
from leader import Leader
from main import decide_role

class MainTest(unittest.TestCase):
    def test_artag_not_detected(self):
        self.assertTrue(isinstance(decide_role(False), Leader))


    def test_artag_detected(self):
        self.assertTrue(isinstance(decide_role(True), Follower))


if __name__ == '__main__':
    unittest.main()
