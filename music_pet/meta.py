# -*- coding: utf-8 -*-
import re
from collections import defaultdict
from ConfigParser import ConfigParser

from .utils import trim_quote, to_unicode, remove_bom, iconv_file
from .exc import InvalidTag

__all__ = ["Meta", "Track", "Album", "AlbumList",
           "parse_cue"]


u = to_unicode


class Meta:

    def __init__(self, data=None):
        if data is None:
            self.data = {}
        else:
            assert type(data) == dict
            self.data = data

    def has_tag(self, tag):
        if tag not in self.data:
            return False
        if self.data[u(tag)] is None:
            return False
        return True

    def get_tag(self, tag):
        if not self.has_tag(tag):
            raise InvalidTag(u"Tag '%s' doesn't exists" % tag)
        return self.data[u(tag)]

    def set_tag(self, tag, value):
        self.data[u(tag)] = u(value)

    def remove_tag(self, tag):
        if self.has_tag(tag):
            del self.data[tag]

    def list_tag(self):
        return filter(lambda t: self.data[u(t)] is not None, self.data.keys())

    def detail(self):
        lines = []
        for tag in self.list_tag():
            lines.append(u"%s : %s" % (tag, self.get_tag(tag)))
        return lines


class Track(Meta):

    def __init__(self, data=None):
        Meta.__init__(self, data)

    @property
    def tracknumber(self):
        if u"tracknumber" in self.data:
            return self.data[u"tracknumber"]
        return None

    @tracknumber.setter
    def tracknumber(self, value):
        self.data[u"tracknumber"] = unicode(int(value))

    @tracknumber.deleter
    def tracknumber(self):
        del self.data[u"tracknumber"]

    @property
    def discnumber(self):
        if u"discnumber" in self.data:
            return self.data[u"discnumber"]
        return None

    @discnumber.setter
    def discnumber(self, value):
        self.data[u"discnumber"] = unicode(int(value))

    @discnumber.deleter
    def discnumber(self):
        del self.data[u"discnumber"]

    @property
    def totaldiscs(self):
        if u"totaldiscs" in self.data:
            return self.data[u"totaldiscs"]
        return None

    @totaldiscs.setter
    def totaldiscs(self, value):
        self.data[u"totaldiscs"] = unicode(int(value))

    @totaldiscs.deleter
    def totaldiscs(self):
        del self.data[u"totaldiscs"]

    @property
    def album(self):
        if u"album" in self.data:
            return self.data[u"album"]
        return None

    @album.setter
    def album(self, value):
        self.data[u"album"] = unicode(value)

    @album.deleter
    def album(self):
        del self.data[u"album"]

    @property
    def albumartist(self):
        if u"albumartist" in self.data:
            return self.data[u"albumartist"]
        return None

    @albumartist.setter
    def albumartist(self, value):
        self.data[u"albumartist"] = unicode(value)

    @albumartist.deleter
    def albumartist(self):
        del self.data[u"albumartist"]

    @property
    def artist(self):
        if u"artist" in self.data:
            return self.data[u"artist"]
        return None

    @artist.setter
    def artist(self, value):
        self.data[u"artist"] = unicode(value)

    @artist.deleter
    def artist(self):
        del self.data[u"artist"]

    @property
    def title(self):
        if u"title" in self.data:
            return self.data[u"title"]
        return None

    @title.setter
    def title(self, value):
        self.data[u"title"] = unicode(value)

    @title.deleter
    def title(self):
        del self.data[u"title"]


class Album(list):

    def __init__(self, name=None, tracks=None):
        self.name = None

        if tracks:
            self.extend(tracks)

    def extend(self, tracks):
        for track in tracks:
            self.check_name(track.album)
            list.append(self, track)
        self = sorted(self, key=lambda t: int(t.tracknumber))

    def append(self, track):
        self.check_name(track.album)
        list.append(self, track)
        self = sorted(self, key=lambda t: int(t.tracknumber))

    def check_name(self, name):
        if self.name is not None:
            if name != self.name:
                raise ValueError("Track not belong the album %s" % self.name)
        else:
            self.name = name

    def update_tag(self, tag, value):
        for track in self:
            track.set_tag(tag, value)

    def update_track_tag(self, track_num, tag, value):
        for track in self:
            if not track.has_tag(u"tracknum"):
                continue
            if track.tracknum == u(track_num):
                track.set_tag(tag, value)

    def get_track(self, track_num):
        for track in self:
            if not track.has_tag(u"tracknum"):
                continue
            if track.tracknum == u(track_num):
                return track

    def detail(self):
        lines = [u"==== Album : %s ====" % self.name]
        for track in self:
            lines.append(u" == Track : %s ==" % track.tracknumber)
            for line in track.detail():
                lines.append(u"   %s" % line)
        return lines

    def _fix_discnumber(self):
        max_discnumber = 1
        for track in self:
            if track.has_tag(u"discnumber"):
                if int(track.discnumber) > max_discnumber:
                    max_discnumber = int(track.discnumber)
        if max_discnumber > 1:
            if not track.has_tag(u"discnumber"):
                raise ValueError("Some track don't have discnumber in multi-disc album")
            track.totaldiscs = unicode(max_discnumber)
        else:
            track.remove_tag(u"discnumber")
            track.remove_tag(u"totaldiscs")


class AlbumList(dict):

    def __init__(self, albums=[], tracks=[]):
        self.extend_albums(albums)
        self.extend_tracks(tracks)

    def extend_albums(self, albums):
        for album in albums:
            if album.name in self:
                self[album.name].append(album)
            else:
                self[album.name] = album

    def add_album(self, album):
        if album.name in self:
            self[album.name].append(album)
        else:
            self[album.name] = album

    def extend_tracks(self, tracks):
        for track in tracks:
            self.add_track(track)

    def add_track(self, track):
        if track.album in self:
            self[track.album].append(track)
        else:
            self[track.album] = Album(track.album, [track])


def parse_cue(filename, encoding=None):
    """
    The CUE file shall be UTF-8 without BOM"
    """
    filename = _cue_format_convert(filename, encoding=encoding)
    state = {}
    textline = ""
    al = AlbumList()

    def _m(match, key):
        return trim_quote(match.groupdict()[key].strip())

    def _match_rem():
        r = re.search('''REM\s+(?P<rem_tag>[^\s]+)\s+(?P<rem_value>.+)''',
                      textline)

        if not r: return False

        _tag = u(_m(r, "rem_tag")).lower()
        _value = u(_m(r, "rem_value"))

        state[_tag] = _value
        return True

    def _match_performer():
        r = re.search('''PERFORMER\s+(?P<performer>.+)$''',
                      textline)

        if not r: return False

        _perf = u(_m(r, "performer"))

        if u"tracknumber" not in state:
            state[u"albumartist"] = _perf
        else:
            state[u"artist"] = _perf
        return True

    def _match_title():
        r = re.search('''TITLE\s+(?P<title>.+)''',
                      textline)

        if not r: return False

        _title = u(_m(r, "title"))

        if u"tracknumber" not in state:
            state[u"album"] = _title
        else:
            state[u"title"] = _title
        return True

    def _match_file():
        r = re.search('''FILE\s+(?P<file>.+)\s+\w+''',
                      textline)

        if not r: return False

        # File changed, create track if necessary
        if _ready(): _gen_track()

        _file = u(_m(r, "file"))

        state[u"original_file"] = _file
        return True

    def _match_track():
        r = re.search('''TRACK\s+(?P<track_num>\d+)\s+AUDIO''',
                      textline)

        if not r: return False

        # Track changed, create track if necessary
        if _ready(): _gen_track()

        _track = u(_m(r, "track_num"))

        state[u"tracknumber"] = _track
        return True

    def _match_index():
        r = re.search('''INDEX\s+(?P<index_num>\d+)\s+(?P<timing>.+)''',
                      textline)

        if not r: return False

        _index_num = u(_m(r, "index_num"))
        _timing = u(_m(r, "timing"))

        state[u"index_%s" % _index_num] = _timing
        return True

    def _ready():
        return u"index_01" in state

    def _gen_track():
        track = Track()
        for k, v in state.items():
            track.set_tag(k, v)
        al.add_track(track)
        for k in [u"tracknumber", u"title", u"artist",
                  u"index_00", u"index_01"]:
            try:
                del state[k]
            except KeyError:
                pass

    fp = open(filename, "r")
    for textline in fp:
        if _match_file(): continue
        if _match_index(): continue
        if _match_performer(): continue
        if _match_rem(): continue
        if _match_title(): continue
        if _match_track(): continue

    if _ready(): _gen_track()

    fp.close()
    return al


def _cue_format_convert(filename, encoding=None):
    if not filename.endswith(u".utf8.cue"):
        if filename.endswith(u".cue"):
            filename = filename[:-4]

        # Try to remove UTF-8 BOM, if failed, do encoding convertion
        try:
            remove_bom(u"%s.cue" % filename,
                       u"%s.utf8.cue" % filename)
        except ValueError:
            iconv_file(u"%s.cue" % filename,
                       u"%s.utf8.cue" % filename,
                       encoding)
        filename = u"%s.utf8.cue" % filename

    return filename

