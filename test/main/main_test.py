from os import path

import sys
import unittest

FILE_PATH = path.dirname(path.realpath(__file__))
sys.path.append(FILE_PATH + "/../../src")

from leader import Leader
from follower import Follower
from tagrec import TagRecognition

class MainTest(unittest.TestCase):
    def setUp(self):
        self.tag = TagRecognition()
        self.follower = None
        self.leader = None
        if self.tag.detect():
            self.follower = Follower()
        else:
            self.leader = Leader()


    def test_artag_not_detected(self):
        self.assertTrue(self.leader is not None)


    def test_artag_detected(self):
        self.assertTrue(self.follower is not None)


if __name__ == '__main__':
    unittest.main()
