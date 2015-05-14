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

        albums = [[x.data for x in y] for y in album_list.values()]
        albums_expected = [
            [
                {
                    u'album': u'Good Morning 精选集',
                    u'comment': u'ExactAudioCopy v1.0b2',
                    u'index_01': u'00:00:00',
                    u'totaltracks': u'4',
                    u'discid': u'2011FICDKE',
                    u'title': u'さよなら',
                    u'date': u'2021',
                    u'albumartist': u'愛玩魂斗羅的狂人',
                    u'genre': u'Soundtrack',
                    u'tracknumber': u'01',
                    u'original_file': u'CDImage.flac'
                }, {
                    u'album': u'Good Morning 精选集',
                    u'comment': u'ExactAudioCopy v1.0b2',
                    u'index_01': u'03:23:16',
                    u'index_00': u'03:20:54',
                    u'discid': u'2011FICDKE',
                    u'title': u'歌',
                    u'totaltracks': u'4',
                    u'date': u'2021',
                    u'albumartist': u'愛玩魂斗羅的狂人',
                    u'genre': u'Soundtrack',
                    u'tracknumber': u'02',
                    u'original_file': u'CDImage.flac'
                }, {
                    u'album': u'Good Morning 精选集',
                    u'comment': u'ExactAudioCopy v1.0b2',
                    u'index_01': u'06:17:31',
                    u'index_00': u'06:16:15',
                    u'discid': u'2011FICDKE',
                    u'title': u'丧心病狂',
                    u'totaltracks': u'4',
                    u'date': u'2021',
                    u'albumartist': u'愛玩魂斗羅的狂人',
                    u'genre': u'Soundtrack',
                    u'tracknumber': u'03',
                    u'original_file': u'CDImage.flac'
                }, {
                    u'album': u'Good Morning 精选集',
                    u'comment': u'ExactAudioCopy v1.0b2',
                    u'index_01': u'12:42:24',
                    u'index_00': u'12:38:49',
                    u'discid': u'2011FICDKE',
                    u'title': u'～看不到看不到看不到！',
                    u'totaltracks': u'4',
                    u'date': u'2021',
                    u'albumartist': u'愛玩魂斗羅的狂人',
                    u'genre': u'Soundtrack',
                    u'tracknumber': u'04',
                    u'original_file': u'CDImage.flac'
                }
            ]
        ]

        self.assertEqual(album_list.keys(), [u'Good Morning 精选集'])
        self.assertEqual(albums, albums_expected)

    def test_multitrack_flac_CUE_utf8(self):
        INPUT_FILE = u"testfiles/CUETestFile2.utf8.cue"

        album_list = meta.parse_cue(INPUT_FILE)

        albums = [[x.data for x in y] for y in album_list.values()]

        albums_names_expected = [u'No zuo no die why you try.']
        albums_expected = [
            [
                {
                    u'comment': u'ExactAudioCopy v1.0b3',
                    u'album': u'No zuo no die why you try.',
                    u'index_01': u'00:00:00',
                    u'discid': u'FF30FB07',
                    u'title': u'Peace War Found',
                    u'index_02': u'03:56:24',
                    u'artist': u'LOL',
                    u'totaltracks': u'5',
                    u'albumartist': u'大萌神赛高233',
                    u'date': u'2011',
                    u'tracknumber': u'01',
                    u'original_file': u'TRACK01.wav'
                }, {
                    u'comment': u'ExactAudioCopy v1.0b3',
                    u'album': u'No zuo no die why you try.',
                    u'index_01': u'00:00:00',
                    u'discid': u'FF30FB07',
                    u'title': u'GOGOGOGO',
                    u'index_02': u'04:57:68',
                    u'totaltracks': u'5',
                    u'albumartist': u'大萌神赛高233',
                    u'date': u'2011',
                    u'tracknumber': u'02',
                    u'original_file': u'TRACK02.wav'
                }, {
                    u'comment': u'ExactAudioCopy v1.0b3',
                    u'album': u'No zuo no die why you try.',
                    u'index_01': u'00:00:00',
                    u'totaltracks': u'5',
                    u'discid': u'FF30FB07',
                    u'title': u'麻麻请再打我一次',
                    u'index_02': u'04:38:13',
                    u'genre': u'Pop',
                    u'albumartist': u'大萌神赛高233',
                    u'date': u'2011',
                    u'tracknumber': u'03',
                    u'original_file': u'TRACK03.wav'
                }, {
                    u'comment': u'ExactAudioCopy v1.0b3',
                    u'album': u'No zuo no die why you try.',
                    u'index_01': u'00:00:00',
                    u'discid': u'FF30FB07',
                    u'title': u'duang~',
                    u'index_02': u'03:38:54',
                    u'totaltracks': u'5',
                    u'albumartist': u'大萌神赛高233',
                    u'date': u'2011',
                    u'tracknumber': u'04',
                    u'original_file': u'TRACK04.wav'
                }, {
                    u'comment': u'ExactAudioCopy v1.0b3',
                    u'album': u'No zuo no die why you try.',
                    u'index_01': u'00:00:00',
                    u'discid': u'FF30FB07',
                    u'title': u'Hmmmm...',
                    u'index_02': u'05:00:01',
                    u'totaltracks': u'5',
                    u'albumartist': u'大萌神赛高233',
                    u'date': u'2011',
                    u'tracknumber': u'05',
                    u'original_file': u'TRACK05.wav'
                }
            ]
        ]

        self.assertEqual(album_list.keys(), albums_names_expected)
        self.assertEqual(albums, albums_expected)


    def test_INI_utf8(self):
        CUE_FILE = u"testfiles/CUETestFile2.utf8.cue"
        INPUT_FILE = u"testfiles/INITestFile1.ini"

        metas = meta.parse_ini(INPUT_FILE)
        album_list = meta.parse_cue(CUE_FILE)

        for m in metas:
            for album in album_list.values():
                album.update_all_tracks(m)

        albums = [[x.data for x in y] for y in album_list.values()]

        albums_names_expected = [u'No zuo no die why you try.']
        albums_expected = [
            [
                {
                    u'comment': u'ExactAudioCopy v1.0b3, extra comments ~~~',
                    u'album': u'No zuo no die why you try.',
                    u'index_01': u'00:00:00',
                    u'discid': u'FF30FB07',
                    u'title': u'Peace War Found',
                    u'index_02': u'03:56:24',
                    u'artist': u'LOL',
                    u'totaltracks': u'5',
                    u'albumartist': u'押す！',
                    u'date': u'2011',
                    u'tracknumber': u'01',
                    u'genre': u'Soundtrack',
                    u'original_file': u'TRACK01.wav'
                }, {
                    u'comment': u'ExactAudioCopy v1.0b3, extra comments ~~~',
                    u'album': u'No zuo no die why you try.',
                    u'index_01': u'00:00:00',
                    u'discid': u'FF30FB07',
                    u'title': u'GOGOGOGO',
                    u'index_02': u'04:57:68',
                    u'artist': u'No Name',
                    u'totaltracks': u'5',
                    u'albumartist': u'押す！',
                    u'date': u'2011',
                    u'tracknumber': u'02',
                    u'genre': u'Soundtrack',
                    u'original_file': u'TRACK02.wav'
                }, {
                    u'comment': u'ExactAudioCopy v1.0b3, extra comments ~~~',
                    u'album': u'No zuo no die why you try.',
                    u'index_01': u'00:00:00',
                    u'totaltracks': u'5',
                    u'discid': u'FF30FB07',
                    u'title': u'麻麻请再打我一次',
                    u'index_02': u'04:38:13',
                    u'artist': u'No Name',
                    u'genre': u'Pop, Soundtrack',
                    u'albumartist': u'押す！',
                    u'date': u'2011',
                    u'tracknumber': u'03',
                    u'original_file': u'TRACK03.wav'
                }, {
                    u'comment': u'ExactAudioCopy v1.0b3, extra comments ~~~',
                    u'album': u'No zuo no die why you try.',
                    u'index_01': u'00:00:00',
                    u'discid': u'FF30FB07',
                    u'title': u'duang~',
                    u'index_02': u'03:38:54',
                    u'artist': u'No Name',
                    u'totaltracks': u'5',
                    u'albumartist': u'押す！',
                    u'date': u'2011',
                    u'tracknumber': u'04',
                    u'genre': u'Soundtrack',
                    u'original_file': u'TRACK04.wav'
                }, {
                    u'comment': u'ExactAudioCopy v1.0b3, extra comments ~~~',
                    u'album': u'No zuo no die why you try.',
                    u'index_01': u'00:00:00',
                    u'discid': u'FF30FB07',
                    u'title': u'Hmmmm...',
                    u'index_02': u'05:00:01',
                    u'artist': u'No Name',
                    u'totaltracks': u'5',
                    u'albumartist': u'押す！',
                    u'date': u'2011',
                    u'tracknumber': u'05',
                    u'genre': u'Soundtrack',
                    u'original_file': u'TRACK05.wav'
                }
            ]
        ]

        self.assertEqual(album_list.keys(), albums_names_expected)
        self.assertEqual(albums, albums_expected)


