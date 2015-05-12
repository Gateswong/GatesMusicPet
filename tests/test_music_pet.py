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
        album_detail_expected = [
            u"==== Album : Good Morning 精选集 ====",
            u" == Track : 1 ==",
            u"   album : Good Morning 精选集",
            u"   comment : ExactAudioCopy v1.0b2",
            u"   index_01 : 00:00:00",
            u"   discid : 2011FICDKE",
            u"   title : さよなら",
            u"   date : 2021",
            u"   albumartist : 愛玩魂斗羅的狂人",
            u"   genre : Soundtrack",
            u"   tracknumber : 1",
            u"   original_file : CDImage.flac",
            u" == Track : 2 ==",
            u"   album : Good Morning 精选集",
            u"   comment : ExactAudioCopy v1.0b2",
            u"   index_01 : 03:23:16",
            u"   index_00 : 03:20:54",
            u"   discid : 2011FICDKE",
            u"   title : 歌",
            u"   date : 2021",
            u"   albumartist : 愛玩魂斗羅的狂人",
            u"   genre : Soundtrack",
            u"   tracknumber : 2",
            u"   original_file : CDImage.flac",
            u" == Track : 3 ==",
            u"   album : Good Morning 精选集",
            u"   comment : ExactAudioCopy v1.0b2",
            u"   index_01 : 06:17:31",
            u"   index_00 : 06:16:15",
            u"   discid : 2011FICDKE",
            u"   title : 丧心病狂",
            u"   date : 2021",
            u"   albumartist : 愛玩魂斗羅的狂人",
            u"   genre : Soundtrack",
            u"   tracknumber : 3",
            u"   original_file : CDImage.flac",
            u" == Track : 4 ==",
            u"   album : Good Morning 精选集",
            u"   comment : ExactAudioCopy v1.0b2",
            u"   index_01 : 12:42:24",
            u"   index_00 : 12:38:49",
            u"   discid : 2011FICDKE",
            u"   title : ～看不到看不到看不到！",
            u"   date : 2021",
            u"   albumartist : 愛玩魂斗羅的狂人",
            u"   genre : Soundtrack",
            u"   tracknumber : 4",
            u"   original_file : CDImage.flac",
        ]
        self.assertEqual(album_detail_expected, album_detail)

    def test_multitrack_flac_CUE_utf8(self):
        INPUT_FILE = u"testfiles/CUETestFile2.utf8.cue"

        album_list = meta.parse_cue(INPUT_FILE)

        album_detail = album_list.values()[0].detail()
        album_detail_expected = [
            u"==== Album : No zuo no die why you try. ====",
            u" == Track : 1 ==",
            u"   comment : ExactAudioCopy v1.0b3",
            u"   album : No zuo no die why you try.",
            u"   index_01 : 00:00:00",
            u"   discid : FF30FB07",
            u"   title : Peace War Found",
            u"   index_02 : 03:56:24",
            u"   artist : LOL",
            u"   albumartist : 大萌神赛高233",
            u"   date : 2011",
            u"   tracknumber : 1",
            u"   original_file : TRACK01.wav",
            u" == Track : 2 ==",
            u"   comment : ExactAudioCopy v1.0b3",
            u"   album : No zuo no die why you try.",
            u"   index_01 : 00:00:00",
            u"   discid : FF30FB07",
            u"   title : GOGOGOGO",
            u"   index_02 : 04:57:68",
            u"   albumartist : 大萌神赛高233",
            u"   date : 2011",
            u"   tracknumber : 2",
            u"   original_file : TRACK02.wav",
            u" == Track : 3 ==",
            u"   comment : ExactAudioCopy v1.0b3",
            u"   album : No zuo no die why you try.",
            u"   index_01 : 00:00:00",
            u"   discid : FF30FB07",
            u"   title : 麻麻请再打我一次",
            u"   index_02 : 04:38:13",
            u"   genre : Pop",
            u"   albumartist : 大萌神赛高233",
            u"   date : 2011",
            u"   tracknumber : 3",
            u"   original_file : TRACK03.wav",
            u" == Track : 4 ==",
            u"   comment : ExactAudioCopy v1.0b3",
            u"   album : No zuo no die why you try.",
            u"   index_01 : 00:00:00",
            u"   discid : FF30FB07",
            u"   title : duang~",
            u"   index_02 : 03:38:54",
            u"   albumartist : 大萌神赛高233",
            u"   date : 2011",
            u"   tracknumber : 4",
            u"   original_file : TRACK04.wav",
            u" == Track : 5 ==",
            u"   comment : ExactAudioCopy v1.0b3",
            u"   album : No zuo no die why you try.",
            u"   index_01 : 00:00:00",
            u"   discid : FF30FB07",
            u"   title : Hmmmm...",
            u"   index_02 : 05:00:01",
            u"   albumartist : 大萌神赛高233",
            u"   date : 2011",
            u"   tracknumber : 5",
            u"   original_file : TRACK05.wav",
        ]

        self.assertEqual(album_detail_expected, album_detail)

    def test_INI_utf8(self):
        CUE_FILE = u"testfiles/CUETestFile2.utf8.cue"
        INPUT_FILE = u"testfiles/INITestFile1.ini"

        metas = meta.parse_ini(INPUT_FILE)
        album_list = meta.parse_cue(CUE_FILE)

        for m in metas:
            for album in album_list.values():
                album.update_all_tracks(m)

        album_detail = album_list.values()[0].detail()
        album_detail_expected = [
            u"==== Album : 覆盖起来 ====",
            u" == Track : 1 ==",
            u"   comment : ExactAudioCopy v1.0b3, extra comments ~~~",
            u"   album : No zuo no die why you try.",
            u"   index_01 : 00:00:00",
            u"   discid : FF30FB07",
            u"   title : Peace War Found",
            u"   index_02 : 03:56:24",
            u"   artist : LOL",
            u"   genre : Soundtrack",
            u"   albumartist : 押す！",
            u"   date : 2011",
            u"   tracknumber : 1",
            u"   original_file : TRACK01.wav",
            u" == Track : 2 ==",
            u"   comment : ExactAudioCopy v1.0b3, extra comments ~~~",
            u"   album : No zuo no die why you try.",
            u"   index_01 : 00:00:00",
            u"   discid : FF30FB07",
            u"   title : GOGOGOGO",
            u"   index_02 : 04:57:68",
            u"   artist : No Name",
            u"   genre : Soundtrack",
            u"   albumartist : 押す！",
            u"   date : 2011",
            u"   tracknumber : 2",
            u"   original_file : TRACK02.wav",
            u" == Track : 3 ==",
            u"   comment : ExactAudioCopy v1.0b3, extra comments ~~~",
            u"   album : No zuo no die why you try.",
            u"   index_01 : 00:00:00",
            u"   discid : FF30FB07",
            u"   title : 麻麻请再打我一次",
            u"   index_02 : 04:38:13",
            u"   artist : No Name",
            u"   genre : Pop, Soundtrack",
            u"   albumartist : 押す！",
            u"   date : 2011",
            u"   tracknumber : 3",
            u"   original_file : TRACK03.wav",
            u" == Track : 4 ==",
            u"   comment : ExactAudioCopy v1.0b3, extra comments ~~~",
            u"   album : No zuo no die why you try.",
            u"   index_01 : 00:00:00",
            u"   discid : FF30FB07",
            u"   title : duang~",
            u"   index_02 : 03:38:54",
            u"   artist : No Name",
            u"   genre : Soundtrack",
            u"   albumartist : 押す！",
            u"   date : 2011",
            u"   tracknumber : 4",
            u"   original_file : TRACK04.wav",
            u" == Track : 5 ==",
            u"   comment : ExactAudioCopy v1.0b3, extra comments ~~~",
            u"   album : No zuo no die why you try.",
            u"   index_01 : 00:00:00",
            u"   discid : FF30FB07",
            u"   title : Hmmmm...",
            u"   index_02 : 05:00:01",
            u"   artist : No Name",
            u"   genre : Soundtrack",
            u"   albumartist : 押す！",
            u"   date : 2011",
            u"   tracknumber : 5",
            u"   original_file : TRACK05.wav",            
        ]

        self.assertEqual(album_detail_expected, album_detail)

    def test_AAA(self):
        from music_pet import utils
        from music_pet import meta
        
        cue = u"/Users/Gates_ice/Public/vmware-share/BaiduDownloader/[www.PT80.com]Gregorian/Japan/2001 - Masters Of Chant Chapter II (NXCB-00030)/00. Gregorian - Masters Of Chant Chapter II.cue"
        
        albumList = meta.parse_cue(cue)
        pass


