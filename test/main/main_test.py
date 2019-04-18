from os import path

import sys
import unittest

FILE_PATH = path.dirname(path.realpath(__file__))
sys.path.append(FILE_PATH + "/../../src")

from follower import Follower
from leader import Leader
from main import decide_role
from tagrec import TagRecognition

class MainTest(unittest.TestCase):
    def setUp(self):
        self._pictures_dir = FILE_PATH + "/../res/tag_pictures/"


    def test_artag_not_detected(self):
        img_src = self._pictures_dir + "no_tag.jpg"
        tag = TagRecognition()
        self.assertTrue(isinstance(decide_role(tag.detect(img_src)), Leader))


    def test_artag_detected(self):
        img_src = self._pictures_dir + "straight_no_turn_5in.jpg"
        tag = TagRecognition()
        self.assertTrue(isinstance(decide_role(tag.detect(img_src)), Follower))


if __name__ == '__main__':
    unittest.main()
