# -*- coding: utf-8 -*-
import unittest
import os

from music_pet import meta


class UnitTest_music_pet__utils__path_from_pattern(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_1(self):
        from music_pet.utils import path_from_pattern

        PATTERN = u"/Users/normaluser/music_output/<%(prefix)s >%(album)s< (%(suffix)s)>/<<%(discnumber)s->%(tracknumber)s >%(title)s.flac"
        D = {
            u"album": u"看不懂到底有什么想法",
            u"title": u"有没有搞错",
        }

        path = path_from_pattern(PATTERN, D)
        path_expected = u"/Users/normaluser/music_output/看不懂到底有什么想法/有没有搞错.flac"

        print(path)
        self.assertEqual(path, path_expected, "The result is not correct!")

    def test_2(self):
        from music_pet.utils import path_from_pattern

        PATTERN = u"/Users/normaluser/music_output/<%(prefix)s >%(album)s< (%(suffix)s)>/<<%(discnumber)s->%(tracknumber)s >%(title)s.flac"
        D = {
            u"album": u"看不懂到底有什么想法",
            u"title": u"有没有搞错",
            u"tracknumber": u"14",
        }

        path = path_from_pattern(PATTERN, D)
        path_expected = u"/Users/normaluser/music_output/看不懂到底有什么想法/14 有没有搞错.flac"

        print(path)
        self.assertEqual(path, path_expected, "The result is not correct")

    def test_3(self):
        from music_pet.utils import path_from_pattern

        PATTERN = u"/Users/normaluser/music_output/<%(prefix)s >%(album)s< (%(suffix)s)>/<<%(discnumber)s->%(tracknumber)s >%(title)s.flac"
        D = {
            u"album": u"看不懂到底有什么想法",
            u"title": u"有没有搞错",
            u"tracknumber": u"14",
            u"discnumber": u"3",
        }

        path = path_from_pattern(PATTERN, D)
        path_expected = u"/Users/normaluser/music_output/看不懂到底有什么想法/3-14 有没有搞错.flac"

        print(path)
        self.assertEqual(path, path_expected, "The result is not correct")

    def test_4(self):
        from music_pet.utils import path_from_pattern

        PATTERN = u"/Users/normaluser/music_output/<%(prefix)s >%(album)s< (%(suffix)s)>/<<%(discnumber)s->%(tracknumber)s >%(title)s.flac"
        D = {
            u"album": u"看不懂到底有什么想法",
            u"title": u"有没有搞错",
            u"discnumber": u"3",
        }

        path = path_from_pattern(PATTERN, D)
        path_expected = u"/Users/normaluser/music_output/看不懂到底有什么想法/有没有搞错.flac"

        print(path)
        self.assertEqual(path, path_expected, "The result is not correct")

    def test_5(self):
        from music_pet.utils import path_from_pattern

        PATTERN = u"/Users/normaluser/music_output/<%(prefix)s >%(album)s< (%(suffix)s)>/<<%(discnumber)s->%(tracknumber)s >%(title)s.flac"
        D = {
            u"album": u"看不懂到底有什么想法",
            u"title": u"有没有搞错",
            u"tracknumber": u"14",
            u"discnumber": u"3",
            u"prefix": u"精选集",
        }

        path = path_from_pattern(PATTERN, D)
        path_expected = u"/Users/normaluser/music_output/精选集 看不懂到底有什么想法/3-14 有没有搞错.flac"

        print(path)
        self.assertEqual(path, path_expected, "The result is not correct")

    def test_6(self):
        from music_pet.utils import path_from_pattern

        PATTERN = u"/Users/normaluser/music_output/<%(prefix)s >%(album)s< (%(suffix)s)>/<<%(discnumber)s->%(tracknumber)s >%(title)s.flac"
        D = {
            u"album": u"看不懂到底有什么想法",
            u"title": u"有没有搞错",
            u"tracknumber": u"14",
            u"discnumber": u"3",
            u"prefix": u"精选集",
            u"suffix": u"限量版",
        }

        path = path_from_pattern(PATTERN, D)
        path_expected = u"/Users/normaluser/music_output/精选集 看不懂到底有什么想法 (限量版)/3-14 有没有搞错.flac"

        print(path)
        self.assertEqual(path, path_expected, "The result is not correct")

