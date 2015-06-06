# -*- coding: utf-8 -*-

import re
import codecs
from collections import defaultdict

from ..utils import trim_quote, read_file, to_unicode as u
from ..meta import Meta


class _CUEParseHandle(object):

    def __init__(self):
        self.stag = []
        self.svalue = []
        self.slen = 0
        self.metas = []

    def push(self, tag, value):
        self.stag.append(tag)
        self.svalue.append(value)
        self.slen += 1

    def pop(self):
        if self.slen > 0:
            self.slen -= 1
            tag = self.stag.pop()
            value = self.svalue.pop()
            return tag, value
        return None, None

    def pop_until(self, tag):
        try:
            i = self.stag.index(tag)
            self.stag = self.stag[:i]
            self.svalue = self.svalue[:i]
            self.slen = i
        except ValueError:
            return

    def extract(self):
        meta = Meta(_source=u"CUE")
        for i in xrange(self.slen):
            meta.set_tag(self.stag[i], self.svalue[i])
        self.metas.append(meta)

    def has_tag(self, tag):
        return tag in self.stag

    def next_token(self, tag, value):
        if self.has_tag(tag):
            self.extract()
            self.pop_until(tag)
        self.push(tag, value)

    def finish(self):
        self.extract()
        self.set_begin_time()
        self.analyse_time()

    def build_time_table(self):
        """
        Build a time table which each item has time and its tracknumber.
        """
        time_table = defaultdict(set)
        for meta in self.metas:
            if u"_time_begin" in meta:
                time_table[meta[u"_file"]].add(meta[u"_time_begin"])

        for _f, _l in time_table.items():
            time_table[_f] = sorted(_l, key=_cue_time_to_int)

        return time_table

    def analyse_time(self):
        """
        Analyse the time in all metas.
        """
        time_table = self.build_time_table()

        for meta in self.metas:
            if meta[u"_file"] not in time_table:
                continue

            if u"_time_begin" in meta:
                index = time_table[meta[u"_file"]].index(meta[u"_time_begin"])
                if index == len(time_table[meta[u"_file"]]) - 1:
                    continue
                meta[u"_time_end"] = time_table[meta[u"_file"]][index + 1]

    def set_begin_time(self):
        for meta in self.metas:
            _set_meta_begin_time(meta)


def _set_meta_begin_time(meta):
    if not isinstance(meta, Meta):
        raise TypeError("Only Meta instance is allowed")

    if u"INDEX 00" in meta:
        meta[u"_time_begin"] = meta[u"INDEX 00"]
    elif u"INDEX 01" in meta:
        meta[u"_time_begin"] = meta[u"INDEX 01"]
    else:
        meta[u"_time_begin"] = u"00:00:00"


def _cue_time_to_int(cue_time):
    """
    Convert an item from time table, take the CUE time and convert it to integer.
    """
    r = re.match(u'''(\d+):(\d{2}):(\d{2})''', cue_time)
    if r is None:
        raise ValueError("Invalid CUE Time: %s" % cue_time)

    return int(u"%s%s%s" % r.groups())


def _matched_line_rem(textline, cue_handle):
    r = re.search(u'''REM\s+(?P<rem_tag>[^\s]+)\s+(?P<rem_value>.+)''',
                  textline)

    if not r: return False

    _tag = u(trim_quote(r.groupdict()["rem_tag"].strip())).upper()
    _value = u(trim_quote(r.groupdict()["rem_value"].strip()))

    cue_handle.next_token(_tag, _value)
    return True


def _matched_line_performer(textline, cue_handle):
    r = re.search(u'''PERFORMER\s+(?P<performer>.+)$''',
                  textline)

    if not r: return False

    _performer = u(trim_quote(r.groupdict()["performer"].strip()))

    if cue_handle.has_tag(u"ALBUMARTIST"):
        cue_handle.next_token(u"ARTIST", _performer)
    else:
        cue_handle.next_token(u"ALBUMARTIST", _performer)
    return True


def _matched_line_title(textline, cue_handle):
    r = re.search(u'''TITLE\s+(?P<title>.+)''',
                  textline)

    if not r: return False

    _title = u(trim_quote(r.groupdict()["title"].strip()))

    if cue_handle.has_tag(u"ALBUM"):
        cue_handle.next_token(u"TITLE", _title)
    else:
        cue_handle.next_token(u"ALBUM", _title)
    return True


def _matched_line_file(textline, cue_handle):
    r = re.search(u'''FILE\s+(?P<file>.+)\s\w+''',
                  textline)

    if not r: return False

    _file = u(trim_quote(r.groupdict()["file"].strip()))

    cue_handle.next_token(u"_file", _file)
    return True


def _matched_line_track(textline, cue_handle):
    r = re.search(u'''TRACK\s+(?P<track_num>\d+)\s+AUDIO''',
                  textline)

    if not r: return False

    _tracknum = u(int(trim_quote(r.groupdict()["track_num"].strip())))

    cue_handle.next_token(u"TRACKNUMBER", _tracknum)
    return True


def _matched_line_index(textline, cue_handle):
    r = re.search(u'''INDEX\s+(?P<index_num>\d+)\s+(?P<timing>.+)''',
                  textline)

    if not r: return False

    _indexnum = u(trim_quote(r.groupdict()["index_num"].strip()))
    _timing = u(trim_quote(r.groupdict()["timing"].strip()))

    cue_handle.next_token(u"INDEX %s" % _indexnum, _timing)


def parse_cue(filename, encoding="utf_8"):
    '''
    Parse a CUE file
    '''
    cue_handle = _CUEParseHandle()
    cue_content = read_file(filename, encoding=encoding)

    for textline in cue_content.split(u"\n"):
        if _matched_line_rem(textline, cue_handle): continue
        if _matched_line_title(textline, cue_handle): continue
        if _matched_line_file(textline, cue_handle): continue
        if _matched_line_performer(textline, cue_handle): continue
        if _matched_line_track(textline, cue_handle): continue
        if _matched_line_index(textline, cue_handle): continue

    cue_handle.finish()
    cue_handle.analyse_time()

    return cue_handle.metas



