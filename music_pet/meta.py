# -*- coding: utf-8 -*-
import re
import os
from collections import defaultdict
from ConfigParser import ConfigParser

from .utils import trim_quote, to_unicode, remove_bom, iconv_file
from .exc import InvalidTag

__all__ = [
    "Meta",
    "Track",
    "Album",
    "AlbumList",
    "parse_cue",
    "parse_ini",
]

u = to_unicode


class Meta(object):
    """
    Stores metadata.
    """

    TAG_UPDATE_MODE = u"@music_pet:update_mode"

    UPDATE_DEFAULT = 0
    UPDATE_OVERWRITE = 1
    UPDATE_APPEND = 2

    def __init__(self, **kwargs):
        self._metadata = {}
        for k, v in kwargs.iteritems():
            self.set_tag(k, v)

    def __contains__(self, key):
        return self.has_tag(key)

    def __getitem__(self, key):
        return self.get_tag(key)

    def __setitem__(self, key, value):
        return self.set_tag(key, value)

    def __delitem__(self, key):
        return self.remove_tag(key)

    def has_tag(self, tag):
        if u(tag) not in self._metadata:
            return False
        return True

    def get_tag(self, tag):
        if not self.has_tag(tag):
            raise InvalidTag(u"Tag '%s' doesn't exists" % tag)
        return self._metadata[u(tag)]

    def set_tag(self, tag, value):
        if not value and self.has_tag(tag):
            self.remove_tag(tag)
            return
        self._metadata[u(tag)] = u(value)

    def remove_tag(self, tag):
        if self.has_tag(tag):
            del self._metadata[u(tag)]

    def list_tags(self):
        return self._metadata.keys()

    def update(self, metadata, mode=UPDATE_DEFAULT):
        """
        mode is one of DEFAULT, OVERWRITE and APPEND
        """
        if not isinstance(metadata, (Meta)):
            raise TypeError("An instance of Meta is needed for update()")

        if metadata.has_tag(self.TAG_UPDATE_MODE):
            mode = int(metadata.get_tag(self.TAG_UPDATE_MODE))

        for tag in metadata.list_tags():
            if tag == self.TAG_UPDATE_MODE: continue

            elif mode in [self.UPDATE_DEFAULT, self.UPDATE_APPEND] and not self.has_tag(tag):
                self.set_tag(tag, metadata.get_tag(tag))

            elif mode == self.UPDATE_OVERWRITE:
                self.set_tag(tag, metadata.get_tag(tag))

            elif mode == self.UPDATE_APPEND:
                self.set_tag(tag,
                             u"%s, %s" % (
                                 self.get_tag(tag),
                                 metadata.get_tag(tag)
                             ))
        return

    def to_string(self):
        string = u""
        for tag, value in self._metadata.items():
            string += u"%s : %s" % (tag, value)
        return string


class Track(Meta):

    def __init__(self, **kwargs):
        Meta.__init__(self, **kwargs)
        self.fix_tags()

    def fix_tags(self):
        self._fix_discnumber()
        self._fix_albumartist()

    @property
    def tracknumber(self):
        if u"tracknumber" in self._metadata:
            return self._metadata[u"tracknumber"]
        return None

    @tracknumber.setter
    def tracknumber(self, value):
        self._metadata[u"tracknumber"] = unicode(int(value))
        zf = 2
        if self.totaltracks is not None:
            zf = len(self.totaltracks)
            if zf < 2: zf = 2
        self._metadata[u"tracknumber"] = self._metadata[u"tracknumber"].zfill(zf)

    @tracknumber.deleter
    def tracknumber(self):
        del self._metadata[u"tracknumber"]

    @property
    def totaltracks(self):
        if u"totaltracks" in self._metadata:
            return self._metadata[u"totaltracks"]
        return None

    @totaltracks.setter
    def totaltracks(self, value):
        self._metadata[u"totaltracks"] = unicode(int(value))

    @totaltracks.deleter
    def totaltracks(self):
        del self._metadata[u"totaltracks"]

    @property
    def discnumber(self):
        if u"discnumber" in self._metadata:
            return self._metadata[u"discnumber"]
        return None

    @discnumber.setter
    def discnumber(self, value):
        self._metadata[u"discnumber"] = unicode(int(value))
        if self.totaldiscs is not None:
            self._metadata[u"discnumber"] = self._metadata[u"discnumber"].zfill(len(self.totaldiscs))
        self._fix_discnumber()

    @discnumber.deleter
    def discnumber(self):
        del self._metadata[u"discnumber"]

    @property
    def totaldiscs(self):
        if u"totaldiscs" in self._metadata:
            return self._metadata[u"totaldiscs"]
        return None

    @totaldiscs.setter
    def totaldiscs(self, value):
        self._metadata[u"totaldiscs"] = unicode(int(value))

    @totaldiscs.deleter
    def totaldiscs(self):
        del self._metadata[u"totaldiscs"]

    @property
    def album(self):
        if u"album" in self._metadata:
            return self._metadata[u"album"]
        return None

    @album.setter
    def album(self, value):
        self._metadata[u"album"] = unicode(value)

    @album.deleter
    def album(self):
        del self._metadata[u"album"]

    @property
    def albumartist(self):
        if u"albumartist" in self._metadata:
            return self._metadata[u"albumartist"]
        return None

    @albumartist.setter
    def albumartist(self, value):
        self._metadata[u"albumartist"] = unicode(value)

    @albumartist.deleter
    def albumartist(self):
        del self._metadata[u"albumartist"]

    @property
    def artist(self):
        if u"artist" in self._metadata:
            return self._metadata[u"artist"]
        return None

    @artist.setter
    def artist(self, value):
        self._metadata[u"artist"] = unicode(value)

    @artist.deleter
    def artist(self):
        del self._metadata[u"artist"]

    @property
    def title(self):
        if u"title" in self._metadata:
            return self._metadata[u"title"]
        return None

    @title.setter
    def title(self, value):
        self._metadata[u"title"] = unicode(value)

    @title.deleter
    def title(self):
        del self._metadata[u"title"]

    def refresh_tracknumber(self):
        if self.tracknumber is not None:
            self.tracknumber = self.tracknumber

    def refresh_discnumber(self):
        if self.discnumber is not None:
            self.discnumber = self.discnumber

    def _fix_discnumber(self):
        if self.discnumber is None:
            return

        try:
            int(self.discnumber)
        except ValueError:
            r = re.match(u'''(\d+)/(\d+)''', self.discnumber)
            if r is not None:
                gps = r.groups()
                self.discnumber = gps[0]
                self.totaldiscs = gps[1]

    def _fix_albumartist(self):
        if not self.has_tag(u"albumartist"):
            if self.has_tag(u"album artist"):
                self.set_tag(u"albumartist", self.get_tag(u"album artist"))


class Album(list):

    def __init__(self, name=None, tracks=None):
        self.name = None

        if tracks:
            self.extend(tracks)

    def extend(self, tracks):
        for track in tracks:
            self.check_name(track.album)
            list.append(self, track)
        sortedList = sorted(self, key=lambda t: int(t.tracknumber))
        for i in xrange(len(sortedList)):
            self[i] = sortedList[i]
        self._fix_discnumber()
        self._fix_tracknumber()

    def append(self, track):
        self.check_name(track.album)
        list.append(self, track)
        sortedList = sorted(self, key=lambda t: int(t.tracknumber))
        for i in xrange(len(sortedList)):
            self[i] = sortedList[i]
        self._fix_discnumber()
        self._fix_tracknumber()

    def check_name(self, name):
        if self.name is not None:
            if name != self.name:
                raise ValueError("Track not belong the album %s" % self.name)
        else:
            self.name = name

    def update_tag(self, tag, value):
        for track in self:
            track.set_tag(tag, value)

    def get_track(self, track_num):
        for track in self:
            if not track.has_tag(u"tracknumber"):
                continue
            if int(track.tracknumber) == int(track_num):
                return track
        return None

    def update_all_tracks(self, meta, mode=DEFAULT):
        for track in self:
            track.update(meta, mode)
        if meta.has_tag(u"album"):
            self.name = meta.get_tag(u"album")

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
            track.refresh_discnumber()

    def _fix_tracknumber(self):
        max_tracknumber = 1
        for track in self:
            if int(track.tracknumber) > max_tracknumber:
                max_tracknumber = int(track.tracknumber)
        for track in self:
            track.totaltracks = max_tracknumber
            track.refresh_tracknumber()


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

    def fix_album_names(self):
        changed_keys = set()

        for key in self.keys():
            if self[key].name != key:
                changed_keys.add(key)

        for key in changed_keys:
            self[self[key].name] = self[key]
            del self[key]


def parse_cue(filename, encoding=None):
    """
    The CUE file shall be UTF-8 without BOM"
    """
    filename = _cue_format_convert(filename, encoding=encoding)
    states = []
    textline = ""
    al = AlbumList()

    def _m(match, key):
        return trim_quote(match.groupdict()[key].strip())

    def _extract_meta(tag):
        newmeta = Track()
        for s in states:
            newmeta.set_tag(s[0], s[1])
        while len(states) > 0:
            if states[-1][0] == tag:
                break
            states.pop()
        if len(states) > 1:
            states.pop()
        al.add_track(newmeta)

    def _push(tag, value):
        for s in states:
            if tag == s[0] and tag in [u"original_file", u"tracknumber"]:
                _extract_meta(tag)
                break
        states.append((tag, value))

    def _has_tag(tag):
        for x in states:
            if x[0] == tag:
                return True
        return False

    def _match_rem():
        r = re.search('''REM\s+(?P<rem_tag>[^\s]+)\s+(?P<rem_value>.+)''',
                      textline)

        if not r: return False

        _tag = u(_m(r, "rem_tag")).lower()
        _value = u(_m(r, "rem_value"))

        _push(_tag, _value)
        return True

    def _match_performer():
        r = re.search('''PERFORMER\s+(?P<performer>.+)$''',
                      textline)

        if not r: return False

        _perf = u(_m(r, "performer"))

        if not _has_tag(u"tracknumber"):
            _push(u"albumartist", _perf)
        else:
            _push(u"artist", _perf)
        return True

    def _match_title():
        r = re.search('''TITLE\s+(?P<title>.+)''',
                      textline)

        if not r: return False

        _title = u(_m(r, "title"))

        if not _has_tag(u"tracknumber"):
            _push(u"album", _title)
        else:
            _push(u"title", _title)
        return True

    def _match_file():
        r = re.search('''FILE\s+(?P<file>.+)\s+\w+''',
                      textline)

        if not r: return False

        _file = u(_m(r, "file"))

        _push(u"original_file", _file)
        return True

    def _match_track():
        r = re.search('''TRACK\s+(?P<track_num>\d+)\s+AUDIO''',
                      textline)

        if not r: return False

        _track = u(int(_m(r, "track_num")))

        _push(u"tracknumber", _track)
        return True

    def _match_index():
        r = re.search('''INDEX\s+(?P<index_num>\d+)\s+(?P<timing>.+)''',
                      textline)

        if not r: return False

        _index_num = u(_m(r, "index_num"))
        _timing = u(_m(r, "timing"))

        _push(u"index_%s" % _index_num, _timing)
        return True

    fp = open(filename, "r")
    for textline in fp:
        if _match_file(): continue
        if _match_index(): continue
        if _match_performer(): continue
        if _match_rem(): continue
        if _match_title(): continue
        if _match_track(): continue

    _extract_meta(0)

    fp.close()
    return al


def parse_ini(filename):
    cp = ConfigParser()
    cp.read(filename)

    metas = []

    sections = cp.sections()
    for section in sections:
        if section.startswith(u"default"): mode = DEFAULT
        elif section.startswith(u"overwrite"): mode = OVERWRITE
        elif section.startswith(u"append"): mode = APPEND

        meta = Meta()
        meta.set_tag(TAG_UPDATE_MODE, u(mode))

        for option in cp.options(section):
            meta.set_tag(u(option), u(cp.get(section, option)))

        metas.append(meta)

    return metas


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

