# -*- coding: utf-8 -*-
import unittest
import os

from music_pet.cue import CUE


class TestOnParseCUEFile(unittest.TestCase):

    def setUp(self):
        return

    def test_CUE_utf8(self):
        INPUT_FILE = u"testfiles/CUETestFile1.utf8.cue"

        cue = CUE(INPUT_FILE)

        print(cue.details())

