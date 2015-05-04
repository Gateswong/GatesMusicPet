# -*- coding: utf-8 -*-
import re
from collections import defaultdict
from ConfigParser import ConfigParser

from .utils import trim_quote, to_unicode


def mdget(match, key):
    return trim_quote(match.groupdict()[key].strip())


class CUE:
    """
    This class takes UTF8 cue file, parse them to the metadata.
    """

    def __init__(self, filename, meta=None):
        self.inputfile = filename
        if not self.inputfile.endswith(u".utf8.cue"):
            self.inputfile += u".utf8.cue"

        if meta is None:
            self.meta = defaultdict(dict)
        else:
            self.meta = meta

        self.current_track = 0
        self.errors = []
        self._parse()

    def has_album_tag(self, field):
        field = to_unicode(field)
        return field in self.meta[u"0"]

    def get_album_tag(self, field):
        field = to_unicode(field)
        return self.meta[u"0"][field]

    def has_track_tag(self, field, track_num):
        field = to_unicode(field)
        track = to_unicode(track_num)
        return track in self.meta and field in self.meta[track]

    def get_track_tag(self, field, track_num):
        field = to_unicode(field)
        track = to_unicode(track_num)
        return self.meta[track][field]

    def has_tag(self, field, track_num):
        return self.has_album_tag(field) or self.has_track_tag(field, track_num)

    def get_tag(self, field, track_num):
        if self.has_track_tag(field, track_num):
            return self.get_track_tag(field, track_num)
        return self.get_album_tag(field)

    def list_album_tags(self):
        return self.meta[u"0"].keys()

    def list_track_tags(self, track_num):
        track = to_unicode(track_num)
        if track in self.meta:
            return self.meta[track].keys()
        return []

    def list_tags(self, track_num):
        return list(set(self.list_album_tags() + self.list_track_tags(track_num)))

    def details(self):
        """
        Return a string that contains all the info in this meta
        """
        s = u""
        for track, track_meta in sorted(self.meta.items(), key=lambda x: int(x[0])):
            if track == u"0":
                s += u"\n=== Album Info ===\n"
            else:
                s += u"\n=== Track %s ===\n" % track

            for tag, value in track_meta.items():
                s += u"  %s : %s\n" % (tag, value)
        return s

    def _new_track(self):
        self.current_track += 1
        self.meta[unicode(self.current_track)][u"tracknumber"] = unicode(self.current_track)

    def _match_performer(self, textline):
        r = re.search('''PERFORMER\s+(?P<performer>.+)$''', textline)

        if r:
            performer = to_unicode(mdget(r, "performer"))
            if self.current_track == 0:
                self.meta[u"0"][u"albumartist"] = performer
            else:
                self.meta[unicode(self.current_track)][u"artist"] = performer

            return True
        return False

    def _match_title(self, textline):
        r = re.search('''TITLE\s+(?P<title>.+)''', textline)

        if r:
            title = to_unicode(mdget(r, "title"))
            if self.current_track == 0:
                self.meta[u"0"][u"album"] = title
            else:
                self.meta[unicode(self.current_track)][u"title"] = title

            return True
        return False

    def _match_file(self, textline):
        r = re.search('''FILE\s+(?P<file>.+)\s+\w+''', textline)

        if r:
            audiofile = to_unicode(mdget(r, "file"))
            self.meta[unicode(self.current_track)][u"original_file"] = audiofile

            return True
        return False

    def _match_track(self, textline):
        r = re.search('''TRACK\s+(?P<track_num>\d+)\s+AUDIO''', textline)

        if r:
            return True
        return False

    def _match_index(self, textline):
        r = re.search('''INDEX\s+(?P<index_num>\d+)\s+(?P<timing>.+)''', textline)

        if r:
            index_num = to_unicode(mdget(r, "index_num"))
            timing = to_unicode(mdget(r, "timing"))

            if self.current_track == 0:
                self.errors.append((2,
                                    "Index appears before track!",
                                    textline))
            else:
                self.meta[unicode(self.current_track)][u"index_%s" % index_num] = timing

            return True
        return False

    def _match_rem(self, textline):
        r = re.search('''REM\s+(?P<rem_tag>[^\s]+)\s+(?P<rem_value>.+)''', textline)

        if r:
            rem_tag = to_unicode(mdget(r, "rem_tag")).lower()
            rem_value = to_unicode(mdget(r, "rem_value"))

            self.meta[unicode(self.current_track)][rem_tag] = rem_value

            return True
        return False

    def _parse(self):
        with open(self.inputfile, "r") as fp:
            for textline in fp:
                if self._match_performer(textline): continue
                if self._match_title(textline): continue
                if self._match_file(textline): continue
                if self._match_index(textline): continue
                if self._match_rem(textline): continue
                if self._match_track(textline):
                    self._new_track()
                    continue

                self.errors.append((1,
                                    "Line not recognized",
                                    textline))
        self.meta[u"0"][u"tracktotal"] = unicode(self.current_track)


class ExtraInfo:

    def __init__(self, filename):
        self.infofile = unicode(filename)
        self.extrainfo = defaultdict(dict)

        self._parse()

    def update_meta(self, meta):
        if meta is None:
            return

        if type(meta) != defaultdict:
            raise ValueError("The meta shall be the instance of defaultdict")

        for track in meta:
            for sec in [u"default", u"overwrite", u"append"]:
                if track != u"0":
                    section = u"%s:%s" % (sec, track)
                else:
                    section = sec

                if section not in self.extrainfo:
                    continue

                for option, value in self.extrainfo[section].items():
                    if (sec == u"default" and option not in meta[track]) or sec == u"overwrite":
                        meta[track][option] = value
                    elif sec == u"append":
                        if option not in meta[track]:
                            meta[track][option] = value
                        else:
                            meta[track][option] += ", %s" % value

        return

    def _parse(self):
        config = ConfigParser()
        config.read(self.infofile)

        for section in config.sections():
            for option in config.options(section):
                self.extrainfo[to_unicode(section.lower())][to_unicode(option.lower())] = to_unicode(config.get(section, option))



