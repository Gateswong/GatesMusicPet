# -*- coding: utf-8 -*-
import unittest
import os


class UnitTest_music_pet__playlist__CUE(unittest.TestCase):

    def setUp(self):
        return

    def test_single_flac_CUE_utf8(self):
        from music_pet.playlist import cue

        INPUT_FILE = u"testfiles/CUETestFile1.utf8.cue"

        metas = cue.parse_cue(INPUT_FILE)

        from music_pet import meta
        meta.print_metas(metas)

        expected_metas = [
            {
                u'ALBUM': u'Good Morning \u7cbe\u9009\u96c6',
                u'ALBUMARTIST': u'\u611b\u73a9\u9b42\u6597\u7f85\u7684\u72c2\u4eba',
                u'COMMENT': u'ExactAudioCopy v1.0b2',
                u'DATE': u'2021',
                u'DISCID': u'2011FICDKE',
                u'GENRE': u'Soundtrack',
                u'INDEX 01': u'00:00:00',
                u'TITLE': u'\u3055\u3088\u306a\u3089',
                u'TRACKNUMBER': u'1',
                u'_file': u'CDImage.flac',
                u'_source': u'CUE',
                u'_time_begin':u'00:00:00',
                u'_time_end':u'03:20:54'
            }, {
                u'ALBUM': u'Good Morning \u7cbe\u9009\u96c6',
                u'ALBUMARTIST': u'\u611b\u73a9\u9b42\u6597\u7f85\u7684\u72c2\u4eba',
                u'COMMENT': u'ExactAudioCopy v1.0b2',
                u'DATE': u'2021',
                u'DISCID': u'2011FICDKE',
                u'GENRE': u'Soundtrack',
                u'INDEX 00': u'03:20:54',
                u'INDEX 01': u'03:23:16',
                u'TITLE': u'\u6b4c',
                u'TRACKNUMBER': u'2',
                u'_file': u'CDImage.flac',
                u'_source': u'CUE',
                u'_time_begin':u'03:20:54',
                u'_time_end':u'06:16:15'
            }, {
                u'ALBUM': u'Good Morning \u7cbe\u9009\u96c6',
                u'ALBUMARTIST': u'\u611b\u73a9\u9b42\u6597\u7f85\u7684\u72c2\u4eba',
                u'COMMENT': u'ExactAudioCopy v1.0b2',
                u'DATE': u'2021',
                u'DISCID': u'2011FICDKE',
                u'GENRE': u'Soundtrack',
                u'INDEX 00': u'06:16:15',
                u'INDEX 01': u'06:17:31',
                u'TITLE': u'\u4e27\u5fc3\u75c5\u72c2',
                u'TRACKNUMBER': u'3',
                u'_file': u'CDImage.flac',
                u'_source': u'CUE',
                u'_time_begin':u'06:16:15',
                u'_time_end':u'12:38:49'
            }, {
                u'ALBUM': u'Good Morning \u7cbe\u9009\u96c6',
                u'ALBUMARTIST': u'\u611b\u73a9\u9b42\u6597\u7f85\u7684\u72c2\u4eba',
                u'COMMENT': u'ExactAudioCopy v1.0b2',
                u'DATE': u'2021',
                u'DISCID': u'2011FICDKE',
                u'GENRE': u'Soundtrack',
                u'INDEX 00': u'12:38:49',
                u'INDEX 01': u'12:42:24',
                u'TITLE': u'\uff5e\u770b\u4e0d\u5230\u770b\u4e0d\u5230\u770b\u4e0d\u5230\uff01',
                u'TRACKNUMBER': u'4',
                u'_file': u'CDImage.flac',
                u'_source': u'CUE',
                u'_time_begin':u'12:38:49'
            }
        ]

        for i in xrange(len(metas)):
            self.assertEqual(metas[i]._metadata, expected_metas[i])

    def test_multitrack_flac_CUE_utf8(self):
        from music_pet.playlist import cue

        INPUT_FILE = u"testfiles/CUETestFile2.utf8.cue"

        metas = cue.parse_cue(INPUT_FILE)

        expected_metas = [
            {
                u'COMMENT': u'ExactAudioCopy v1.0b3',
                u'ALBUM': u'No zuo no die why you try.',
                u'INDEX 01': u'00:00:00',
                u'DISCID': u'FF30FB07',
                u'TITLE': u'Peace War Found',
                u'INDEX 02': u'03:56:24',
                u'ARTIST': u'LOL',
                u'ALBUMARTIST': u'大萌神赛高233',
                u'DATE': u'2011',
                u'TRACKNUMBER': u'1',
                u'_file': u'TRACK01.wav',
                u'_source': u'CUE',
                u'_time_begin':u'00:00:00'
            }, {
                u'COMMENT': u'ExactAudioCopy v1.0b3',
                u'ALBUM': u'No zuo no die why you try.',
                u'INDEX 01': u'00:00:00',
                u'DISCID': u'FF30FB07',
                u'TITLE': u'GOGOGOGO',
                u'INDEX 02': u'04:57:68',
                u'ALBUMARTIST': u'大萌神赛高233',
                u'DATE': u'2011',
                u'TRACKNUMBER': u'2',
                u'_file': u'TRACK02.wav',
                u'_source': u'CUE',
                u'_time_begin':u'00:00:00'
            }, {
                u'COMMENT': u'ExactAudioCopy v1.0b3',
                u'ALBUM': u'No zuo no die why you try.',
                u'INDEX 01': u'00:00:00',
                u'DISCID': u'FF30FB07',
                u'TITLE': u'麻麻请再打我一次',
                u'INDEX 02': u'04:38:13',
                u'GENRE': u'Pop',
                u'ALBUMARTIST': u'大萌神赛高233',
                u'DATE': u'2011',
                u'TRACKNUMBER': u'3',
                u'_file': u'TRACK03.wav',
                u'_source': u'CUE',
                u'_time_begin':u'00:00:00'
            }, {
                u'COMMENT': u'ExactAudioCopy v1.0b3',
                u'ALBUM': u'No zuo no die why you try.',
                u'INDEX 01': u'00:00:00',
                u'DISCID': u'FF30FB07',
                u'TITLE': u'duang~',
                u'INDEX 02': u'03:38:54',
                u'ALBUMARTIST': u'大萌神赛高233',
                u'DATE': u'2011',
                u'TRACKNUMBER': u'4',
                u'_file': u'TRACK04.wav',
                u'_source': u'CUE',
                u'_time_begin':u'00:00:00'
            }, {
                u'COMMENT': u'ExactAudioCopy v1.0b3',
                u'ALBUM': u'No zuo no die why you try.',
                u'INDEX 01': u'00:00:00',
                u'DISCID': u'FF30FB07',
                u'TITLE': u'Hmmmm...',
                u'INDEX 02': u'05:00:01',
                u'ALBUMARTIST': u'大萌神赛高233',
                u'DATE': u'2011',
                u'TRACKNUMBER': u'5',
                u'_file': u'TRACK05.wav',
                u'_source': u'CUE',
                u'_time_begin':u'00:00:00'
            }
        ]

        for i in xrange(len(metas)):
            self.assertEqual(metas[i]._metadata, expected_metas[i])


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

    def test_7(self):
        from music_pet.utils import path_from_pattern

        PATTERN = u"/Users/normaluser/music_output/<%(prefix)s >%(album)s< (%(suffix)s)>/<<%(discnumber)s->%(tracknumber)s >>%(title)s.flac"
        D = {
            u"album": u"看不懂到底有什么想法",
            u"title": u"有没有搞错",
            u"tracknumber": u"14",
            u"discnumber": u"3",
            u"prefix": u"精选集",
            u"suffix": u"限量版",
        }

        with self.assertRaises(ValueError):
            path_from_pattern(PATTERN, D)

    def test_8(self):
        from music_pet.utils import path_from_pattern

        PATTERN = u"/Users/normaluser/music_output/<%(prefix)s >%(album)s< (%(suffix)s)>/<<%(discnumber)s-%(tracknumber)s >%(title)s.flac"
        D = {
            u"album": u"看不懂到底有什么想法",
            u"title": u"有没有搞错",
            u"tracknumber": u"14",
            u"discnumber": u"3",
            u"prefix": u"精选集",
            u"suffix": u"限量版",
        }

        with self.assertRaises(ValueError):
            path_from_pattern(PATTERN, D)


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
        os.remove(u"tmp/outfile.txt")
        return

    def test_1(self):
        from music_pet.utils import iconv_file

        iconv_file(u"testfiles/CUETestFile1.gbk.cue",
                   u"tmp/outfile.txt",
                   "gbk")

        self.assertEquals(open(u"testfiles/CUETestFile1.utf8.cue").read(),
                          open(u"tmp/outfile.txt").read())

    def test_2(self):
        from music_pet.utils import iconv_file

        with open(u"tmp/outfile.txt", "w") as fp:
            fp.write(u"123")

        iconv_file(u"testfiles/CUETestFile1.gbk.cue",
                   u"tmp/outfile.txt",
                   "gbk")

        self.assertEqual(open(u"tmp/outfile.txt").read(),
                         u"123")

    def test_3(self):
        from music_pet.utils import iconv_file

        iconv_file(u"testfiles/CUETestFile1.utf8.cue",
                   u"tmp/outfile.txt",
                   "utf8")

        self.assertEqual(open(u"testfiles/CUETestFile1.utf8.cue").read(),
                         open(u"tmp/outfile.txt").read())


class UnitTest_music_pet__utils__filename_safe(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_1(self):
        from music_pet.utils import filename_safe

        IN = u"CDImage.flac"
        OUT_EXPECTED = u"CDImage.flac"

        self.assertEqual(filename_safe(IN), OUT_EXPECTED)

    def test_2(self):
        from music_pet.utils import filename_safe

        IN = u"music/CDImage.flac"
        OUT_EXPECTED = u"music/CDImage.flac"

        self.assertEqual(filename_safe(IN), OUT_EXPECTED)

    def test_3(self):
        from music_pet.utils import filename_safe

        IN = u"music/is that good?.flac"
        OUT_EXPECTED = u"music/is that good_.flac"

        self.assertEqual(filename_safe(IN), OUT_EXPECTED)


class UnitTest_music_pet__utils__ensure_parent_folder(unittest.TestCase):

    def setUp(self):
        self.deltmp = True
        self.deltmp2 = True
        return

    def tearDown(self):
        if self.deltmp:
            os.rmdir(u"tmp/a/b/c")
            os.rmdir(u"tmp/a/b")
        if self.deltmp2:
            os.rmdir(u"tmp/a")
        return

    def test_1(self):
        from music_pet.utils import ensure_parent_folder

        ensure_parent_folder(u"tmp/a/b/c/d")
        self.assertTrue(os.path.exists(u"tmp/a/b/c"))
        self.assertTrue(os.path.isdir(u"tmp/a/b/c"))

    def test_2(self):
        from music_pet.utils import ensure_parent_folder

        self.deltmp = False
        os.makedirs(u"tmp/a", 0440)

        with self.assertRaises(OSError):
            ensure_parent_folder(u"tmp/a/b/c/d")


class UnitTest_music_pet__utils__cli_escape(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_1(self):
        from music_pet.utils import cli_escape

        IN = u"flac a.wav"
        OUT_EXPECTED = u"flac a.wav"

        self.assertEqual(cli_escape(IN), OUT_EXPECTED)

    def test_2(self):
        from music_pet.utils import cli_escape

        IN = u'''flac `you`.wav'''
        OUT_EXPECTED = u'''flac \\`you\\`.wav'''

        self.assertEqual(cli_escape(IN), OUT_EXPECTED)


class UnitTest_music_pet__utils__parent_folder(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_1(self):
        from music_pet.utils import parent_folder

        IN = u'''a/b/c'''
        OUT_EXPECTED = u'''a/b/'''

        self.assertEqual(parent_folder(IN), OUT_EXPECTED)

    def test_2(self):
        from music_pet.utils import parent_folder

        IN = u'''/a/b/c'''
        OUT_EXPECTED = u'''/a/b/'''

        self.assertEqual(parent_folder(IN), OUT_EXPECTED)

    def test_3(self):
        from music_pet.utils import parent_folder

        IN = u'''a/b/c/'''
        OUT_EXPECTED = u'''a/b/'''

        self.assertEqual(parent_folder(IN), OUT_EXPECTED)

    def test_4(self):
        from music_pet.utils import parent_folder

        IN = u'''a'''
        OUT_EXPECTED = u'''./'''

        self.assertEqual(parent_folder(IN), OUT_EXPECTED)

    def test_5(self):
        from music_pet.utils import parent_folder

        IN = u'''.'''
        OUT_EXPECTED = u'''../'''

        self.assertEqual(parent_folder(IN), OUT_EXPECTED)

    def test_6(self):
        from music_pet.utils import parent_folder

        IN = u'''..'''
        OUT_EXPECTED = u'''../../'''

        self.assertEqual(parent_folder(IN), OUT_EXPECTED)

    def test_7(self):
        from music_pet.utils import parent_folder

        IN = u'''../'''
        OUT_EXPECTED = u'../../'''

        self.assertEqual(parent_folder(IN), OUT_EXPECTED)

    def test_8(self):
        from music_pet.utils import parent_folder

        IN = u'''/'''

        with self.assertRaises(ValueError):
            parent_folder(IN)


class UnitTest_music_pet__utils__copy_to(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_1(self):
        from music_pet.utils import command_copy_to

        FILES = [u"1.txt", u"2.dat"]
        FOLDER = u"/a"

        OUT_EXPECTED = u'''cp -n "1.txt" "2.dat" "/a/"'''

        self.assertEqual(command_copy_to(FILES, FOLDER), OUT_EXPECTED)

    def test_2(self):
        from music_pet.utils import command_copy_to

        FILES = [u"1.txt", u"2.dat"]
        FOLDER = u"/a/"

        OUT_EXPECTED = u'''cp -n "1.txt" "2.dat" "/a/"'''

        self.assertEqual(command_copy_to(FILES, FOLDER), OUT_EXPECTED)

    def test_3(self):
        from music_pet.utils import command_copy_to

        FILES = []
        FOLDER = u"/a"

        OUT_EXPECTED = u"echo"

        self.assertEqual(command_copy_to(FILES, FOLDER), OUT_EXPECTED)

    def test_4(self):
        from music_pet.utils import command_copy_to

        FILES = [u"ABC.txt", u'''good`work`.dat''']
        FOLDER = u"/a"

        OUT_EXPECTED = u'''cp -n "ABC.txt" "good\\`work\\`.dat" "/a/"'''

        self.assertEqual(command_copy_to(FILES, FOLDER), OUT_EXPECTED)

    def test_5(self):
        from music_pet.utils import command_copy_to

        FILES = [u"ABC.txt", u'''good`work`.dat''']
        FOLDER = u""

        OUT_EXPECTED = u'''cp -n "ABC.txt" "good\\`work\\`.dat" "./"'''

        self.assertEqual(command_copy_to(FILES, FOLDER), OUT_EXPECTED)


