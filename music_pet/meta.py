# -*- coding: utf-8 -*-
import re
import os
from ConfigParser import ConfigParser

from .utils import trim_quote, to_unicode as u, remove_bom, iconv_file
from .exc import InvalidTag

__all__ = [
    "Meta",
    "MetaUpdateHandle",
    "print_metas",
    "parse_ini",
]


class Meta(object):
    """
    Stores metadata.
    """

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

    @property
    def is_empty(self):
        return self._metadata == {}

    def to_string(self):
        string = u""
        for tag, value in self._metadata.items():
            string += u"%s : %s\n" % (tag, value)
        return string


def print_metas(metas):
    """
    Print the array of Meta instances.
    """
    for meta in metas:
        print(meta.to_string())


class MetaUpdateHandle(object):

    DEFAULT = "DEFAULT"
    OVERWRITE = "OVERWRITE"
    APPEND = "APPEND"

    def __init__(self, update_mode=DEFAULT):
        self._data = Meta()
        self._filter = Meta()
        self.update_mode = update_mode

    def apply(self, meta):
        if not isinstance(meta, Meta):
            raise TypeError("Only instance of Meta can be updated.")
        if self._filter.is_empty:
            self._update_meta(meta)
        elif self._match_filter(meta):
            self._update_meta(meta)

    def _match_filter(self, meta):
        for tag in self._filter.list_tags():
            if self._data.get_tag(tag) != self._filter.get_tag(tag):
                return False
        return True

    def _update_meta(self, meta):
        for tag in self._data.list_tags():
            if self.update_mode == self.OVERWRITE:
                meta.set_tag(tag, self._data.get_tag(tag))

            elif self.update_mode == self.APPEND and meta.has_tag(tag):
                meta.set_tag(tag, u"%s, %s" % (meta.get_tag(tag), self._data.get_tag(tag)))

            elif not meta.has_tag(tag):
                meta.set_tag(tag, self._data.get_tag(tag))

    def add_filter(self, tag, value):
        self._filter.set_tag(tag, value)

    def add_data(self, tag, value):
        self._data.set_tag(tag, value)


def parse_ini(filename):
    cp = ConfigParser()
    cp.read(filename)

    meta_handles = []

    sections = cp.sections()
    for section in sections:
        meta_handle = _parse_ini_section(section, cp.items(section))
        if meta_handle is not None:
            meta_handles.append(meta_handle)

    return meta_handles


def _parse_ini_section(section, items):
    r = re.match(u'''(\w+)(?:#(?:(\d+)-)?(\d+))?''',
                 section)
    if r is None:
        return None
    update_mode, discnumber, tracknumber = r.groups()
    meta_handle = MetaUpdateHandle(update_mode=update_mode.upper())
    if discnumber:
        meta_handle.add_filter(u"DISCNUMBER", discnumber)
    if tracknumber:
        meta_handle.add_filter(u"TRACKNUMBER", tracknumber)

    for tag, value in items:
        if tag[0] == u"?":
            meta_handle.add_filter(tag[1:], value)
        else:
            meta_handle.add_data(tag, value)

    return meta_handle

