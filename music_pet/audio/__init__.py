# -*- coding: utf-8 -*-

from ..meta import Meta


class AudioTrack(Meta):

    def __init__(self, **kwargs):
        Meta.__init__(self, **kwargs)

    @property
    def TRACKNUMBER(self):
        if u"TRACKNUMBER" in self:
            return self[u"TRACKNUMBER"]
        return None

    @TRACKNUMBER.setter
    def TRACKNUMBER(self, value):
        self[u"TRACKNUMBER"] = value

    @TRACKNUMBER.deleter
    def TRACKNUMBER(self):
        del self[u"TRACKNUMBER"]

    @property
    def TRACKTOTAL(self):
        if u"TRACKTOTAL" in self:
            return self[u"TRACKTOTAL"]
        if u"TOTALTRACKS" in self:
            return self[u"TOTALTRACKS"]
        return None

    @TRACKTOTAL.setter
    def TRACKTOTAL(self, value):
        if u"TOTALTRACKS" in self:
            self[u"TOTALTRACKS"] = value
        else:
            self[u"TRACKTOTAL"] = value

    @TRACKTOTAL.deleter
    def TRACKTOTAL(self):
        if u"TRACKTOTAL" in self:
            del self[u"TRACKTOTAL"]
        if u"TOTALTRACKS" in self:
            del self[u"TOTALTRACKS"]

    @property
    def DISCNUMBER(self):
        if u"DISCNUMBER" in self:
            return self[u"DISCNUMBER"]
        return None

    @DISCNUMBER.setter
    def DISCNUMBER(self, value):
        if u"DISCNUMBER" in self:
            return self[u"DISCNUMBER"]
        return None

    @DISCNUMBER.deleter
    def DISCNUMBER(self):
        if u"DISCNUMBER" in self:
            del self[u"DISCNUMBER"]

    @property
    def DISCTOTAL(self):
        if u"DISCTOTAL" in self:
            return self[u"DISCTOTAL"]
        if u"TOTALDISCS" in self:
            return self[u"TOTALDISCS"]
        return None

    @DISCTOTAL.setter
    def DISCTOTAL(self, value):
        if u"TOTALDISCS" in self:
            self[u"TOTALDISCS"] = value
        else:
            self[u"DISCTOTAL"] = value

    @DISCTOTAL.deleter
    def DISCTOTAL(self):
        if u"DISCTOTAL" in self:
            del self[u"DISCTOTAL"]
        if u"TOTALDISCS" in self:
            del self[u"TOTALDISCS"]

    @property
    def ALBUM(self):
        if u"ALBUM" in self:
            return self[u"ALBUM"]
        return None

    @ALBUM.setter
    def ALBUM(self, value):
        self[u"ALBUM"] = value

    @ALBUM.deleter
    def ALBUM(self):
        if u"ALBUM" in self:
            del self[u"ALBUM"]

    @property
    def ALBUMARTIST(self):
        if u"ALBUMARTIST" in self:
            return self[u"ALBUMARTIST"]
        if u"ALBUM ARTIST" in self:
            return self[u"ALBUM ARTIST"]
        return None

    @ALBUMARTIST.setter
    def ALBUMARTIST(self, value):
        if u"ALBUM ARTIST" in self:
            self[u"ALBUM ARTIST"] = value
        else:
            self[u"ALBUMARTIST"] = value

    @ALBUMARTIST.deleter
    def ALBUMARTIST(self):
        if u"ALBUMARTIST" in self:
            del self[u"ALBUMARTIST"]
        if u"ALBUM ARTIST" in self:
            del self[u"ALBUM ARTIST"]

    @property
    def ARTIST(self):
        if u"ARTIST" in self:
            return self[u"ARTIST"]
        return None

    @ARTIST.setter
    def ARTIST(self, value):
        self[u"ARTIST"] = value

    @ARTIST.deleter
    def ARTIST(self):
        if u"ARTIST" in self:
            del self[u"ARTIST"]

    @property
    def TITLE(self):
        if u"TITLE" in self:
            return self[u"TITLE"]
        return None

    @TITLE.setter
    def TITLE(self, value):
        self[u"TITLE"] = value

    @TITLE.deleter
    def TITLE(self):
        if u"TITLE" in self:
            del self[u"TITLE"]


class ConvertHelper(object):
    pass


