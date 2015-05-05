# -*- coding: utf-8 -*-
import unittest
import os

from music_pet import meta


class TestOnParseCUEFile(unittest.TestCase):

    def setUp(self):
        return

    def test_CUE_utf8(self):
        INPUT_FILE = u"testfiles/CUETestFile1.utf8.cue"
        
        album_list = meta.parse_cue(INPUT_FILE)
        
        for album in album_list.values():
            print("\n".join(album.detail()) + "\n")
            