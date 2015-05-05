# -*- coding: utf-8 -*-
import unittest
import os

from music_pet import meta


class TestOnParseCUEFile(unittest.TestCase):

    def setUp(self):
        return

    def test_single_flac_CUE_utf8(self):
        INPUT_FILE = u"testfiles/CUETestFile1.utf8.cue"
        
        album_list = meta.parse_cue(INPUT_FILE)
        
        album_detail = album_list.values()[0].detail()
        album_detail_preset = [
            u"==== Album : Good Morning 精选集 ====",
            u" == Track : 01 ==",
            u"   album : Good Morning 精选集",
            u"   comment : ExactAudioCopy v1.0b2",
            u"   index_01 : 00:00:00",
            u"   discid : 2011FICDKE",
            u"   title : さよなら",
            u"   genre : Soundtrack",
            u"   albumartist : 愛玩魂斗羅的狂人",
            u"   date : 2021",
            u"   tracknumber : 01",
            u"   original_file : CDImage.flac",
            u" == Track : 02 ==",
            u"   album : Good Morning 精选集",
            u"   comment : ExactAudioCopy v1.0b2",
            u"   index_01 : 03:23:16",
            u"   index_00 : 03:20:54",
            u"   discid : 2011FICDKE",
            u"   title : 歌",
            u"   genre : Soundtrack",
            u"   albumartist : 愛玩魂斗羅的狂人",
            u"   date : 2021",
            u"   tracknumber : 02",
            u"   original_file : CDImage.flac",
            u" == Track : 03 ==",
            u"   album : Good Morning 精选集",
            u"   comment : ExactAudioCopy v1.0b2",
            u"   index_01 : 06:17:31",
            u"   index_00 : 06:16:15",
            u"   discid : 2011FICDKE",
            u"   title : 丧心病狂",
            u"   genre : Soundtrack",
            u"   albumartist : 愛玩魂斗羅的狂人",
            u"   date : 2021",
            u"   tracknumber : 03",
            u"   original_file : CDImage.flac",
            u" == Track : 04 ==",
            u"   album : Good Morning 精选集",
            u"   comment : ExactAudioCopy v1.0b2",
            u"   index_01 : 12:42:24",
            u"   index_00 : 12:38:49",
            u"   discid : 2011FICDKE",
            u"   title : ～看不到看不到看不到！",
            u"   genre : Soundtrack",
            u"   albumartist : 愛玩魂斗羅的狂人",
            u"   date : 2021",
            u"   tracknumber : 04",
            u"   original_file : CDImage.flac"
        ]
        self.assertEqual(album_detail_preset, album_detail)
            