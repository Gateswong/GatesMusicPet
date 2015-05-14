# -*- coding: utf-8 -*-
import unittest
import os


class UnitTest_music_pet__meta__Track(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_tracknumber_1(self):
        from music_pet.meta import Track

        t = Track()
        t.tracknumber = 1
        self.assertEqual(t.tracknumber, u"01")

    def test_tracknumber_2(self):
        from music_pet.meta import Track

        t = Track()
        t.tracknumber = 14
        self.assertEqual(t.tracknumber, u"14")

    def test_tracknumber_4(self):
        from music_pet.meta import Track

        t = Track()
        t.tracknumber = 143
        self.assertEqual(t.tracknumber, u"143")

    def test_tracknumber_3(self):
        from music_pet.meta import Track

        t = Track()
        t.totaltracks = 1024
        t.tracknumber = 14
        self.assertEqual(t.tracknumber, u"0014")

    def test_tracknumber_2(self):
        from music_pet.meta import Track

        t = Track()
        t.tracknumber = 14
        t.totaltracks = 1024
        t.refresh_tracknumber()
        self.assertEqual(t.tracknumber, u"0014")


class UnitTest_music_pet__audio__flac__FLAC(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_set_next_start_time_from_album(self):
        from music_pet.meta import Track, Album
        from music_pet.audio.flac import FLAC

        t1 = Track()
        t1.tracknumber = 1
        t1.set_tag(u"index_00", u"00:00:00")
        t2 = Track()
        t2.tracknumber = 2
        t2.set_tag(u"index_00", u"00:03:01")
        a = Album(tracks=[t1, t2])

        f = FLAC(t1.data)
        f.set_next_start_time_from_album(a)

        self.assertTrue(f.has_tag(u"@time_to"))
        print(f.metadata.detail())


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

