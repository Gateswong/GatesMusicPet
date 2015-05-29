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
]

u = to_unicode


class Meta(object):
    """
    Stores metadata.
    """

    TAG_UPDATE_MODE = u"_update_mode"

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
            string += u"%s : %s\n" % (tag, value)
        return string


class Track(Meta):

    def __init__(self, **kwargs):
        Meta.__init__(self, **kwargs)

    @property
    def tracknumber(self):
        if u"TRACKNUMBER" in self:
            return self[u"TRACKNUMBER"]
        elif u"TRACK NUMBER" in self:
            return self[u"TRACK NUMBER"]
        return None

    @tracknumber.setter
    def tracknumber(self, value):
        if u"TRACK NUMBER" in self:
            self[u"TRACK NUMBER"] = value
        else:
            self[u"TRACKNUMBER"] = value

    @tracknumber.deleter
    def tracknumber(self):
        if u"TRACK NUMBER" in self:
            del self[u"TRACK NUMBER"]
        else:
            del self[u"TRACKNUMBER"]

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


def print_metas(metas):
    for meta in metas:
        print(meta.to_string())


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

