# -*- coding: utf-8 -*-
import unittest
import os


class TestOnParseCUEFile(unittest.TestCase):

    def setUp(self):
        return

    def test_single_flac_CUE_utf8(self):
        from music_pet import meta

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
        from music_pet import meta

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
        from music_pet import meta

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
        t1.set_tag(u"original_file", u"CDImage.flac")
        t2 = Track()
        t2.tracknumber = 2
        t2.set_tag(u"index_00", u"00:03:01")
        t2.set_tag(u"original_file", u"CDImage.flac")
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


class UnitTest_music_pet__utils__trim_quote(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_have_quote(self):
        from music_pet.utils import trim_quote

        input_string = u'''"Hello!"'''

        output_string = trim_quote(input_string)
        output_expected = u'''Hello!'''

        self.assertEqual(output_string, output_expected)

    def test_no_quote(self):
        from music_pet.utils import trim_quote

        input_string = u'''Hello!'''

        output_string = trim_quote(input_string)
        output_expected = u'''Hello!'''

        self.assertEqual(output_string, output_expected)

    def test_have_one_quote(self):
        from music_pet.utils import trim_quote

        input_string = u'''"Hello!'''

        output_string = trim_quote(input_string)
        output_expected = u'''"Hello!'''

        self.assertEqual(output_string, output_expected)


class UnitTest_music_pet__utils__remove_bom(unittest.TestCase):

    def setUp(self):
        import os

        self.str_with_bom = "\xef\xbb\xbf1234567"
        self.str_without_bom = "1234567"

        try:
            os.makedirs(u"tmp")
        except:
            pass

        self.testfiles = [
            u"tmp/file_with_bom.txt",
            u"tmp/file_without_bom.txt",
        ]

        with open(u"tmp/file_with_bom.txt", "w") as fp:
            fp.write(self.str_with_bom)
        with open(u"tmp/file_without_bom.txt", "w") as fp:
            fp.write(self.str_without_bom)

        return

    def tearDown(self):
        import os

        for f in self.testfiles:
            os.remove(f)
        return

    def test_remove_bom(self):
        from music_pet.utils import remove_bom

        self.testfiles.append(u"tmp/file_with_bom_removed.txt")
        remove_bom(u"tmp/file_with_bom.txt", u"tmp/file_with_bom_removed.txt")

        with open(u"tmp/file_with_bom_removed.txt") as fp:
            content = fp.read()

        self.assertEqual(content, self.str_without_bom)

    def test_remove_bom_not_exists(self):
        from music_pet.utils import remove_bom

        with self.assertRaises(ValueError):
            remove_bom(u"tmp/file_without_bom.txt", u"tmp/file_with_bom_removed.txt")


class UnitTest_music_pet__utils__iconv_file(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return


class UnitTest_music_pet__utils__filename_safe(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return


class UnitTest_music_pet__utils__ensure_parent_folder(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return


class UnitTest_music_pet__utils__cli_escape(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return


class UnitTest_music_pet__utils__parent_folder(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return


class UnitTest_music_pet__utils__copy_to(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return
