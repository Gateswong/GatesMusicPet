# -*- coding: utf-8 -*-

import re
from uuid import uuid4
from subprocess import check_output, CalledProcessError

from . import AudioTrack, ConvertHelper

from ..utils import (
    to_unicode as u,
    cli_escape,
    filename_safe,
    ensure_parent_folder,
    path_from_pattern,
)
from ..actions import (
    Action,
    SystemCallActionMixin,
    FileActionMixin,
)


class FLAC(AudioTrack):

    def __init__(self):
        AudioTrack.__init__(self)

    def validate(self):
        if u"_file" not in self:
            raise ValueError("The FLAC instance doesn't have an input file.")


def read_flac_file_tags(filename):
    cmdline = u'''metaflac --no-utf8-convert --export-tags-to=- "%s"''' % cli_escape(filename)
    try:
        p = check_output(cmdline, shell=True)
    except CalledProcessError as ex:
        raise ex  # for now, let's just raise this error.

    return p


class FLACConvertHelper(ConvertHelper, Action, SystemCallActionMixin, FileActionMixin):

    def __init__(self):
        ConvertHelper.__init__(self)
        Action.__init__(self)
        SystemCallActionMixin.__init__(self)
        FileActionMixin.__init__(self)

        self.flacs = []
        self.tmp_wav = {}
        self.files_to_copy = {}
        self.output_pattern = None
        return

    def add_flac(self, flac):
        self.validate_flac(flac)
        self.assign_tmp_wav(flac)  # Assign a temp wav file.
        self.flacs.append(flac)

    def assign_tmp_wav(self, flac):
        if flac[u"_file"] in self.tmp_wav:
            return
        if flac[u"_file"].endswith(u".wav"):
            self.tmp_wav[flac[u"_file"]] = flac[u"_file"]
        else:
            self.tmp_wav[flac[u"_file"]] = u"_tmp_%s.wav" % uuid4()

    def build_commands(self, **kwargs):
        self.build_temp_wav_commands(**kwargs)
        self.build_conv_commands(**kwargs)
        self.build_copy_commands(**kwargs)
        self.build_cleanup_commands(**kwargs)

    def build_temp_wav_commands(self, **kwargs):
        for source_file, wav_file in self.tmp_wav.items():
            if source_file != wav_file:
                self.add_system_call(1, command_ffmpeg(infile=source_file, outfile=wav_file, **kwargs))

    def build_conv_commands(self, **kwargs):
        pattern = kwargs.pop(u"pattern")

        for flac in self.flacs:
            outfile = path_from_pattern(pattern, flac)
            infile = self.tmp_wav[flac[u"_file"]]
            self.add_system_call(2, command_flac_conv(flac, infile=infile, outfile=outfile, **kwargs))

    def build_copy_commands(self, **kwargs):
        return

    def build_cleanup_commands(self, **kwargs):
        for tmpwav in self.tmp_wav.values():
            if tmpwav.startswith(u"_tmp_"):
                self.add_delete(3, tmpwav)


def command_ffmpeg(**kwargs):
    infile = kwargs.get(u"infile")
    outfile = kwargs.get(u"outfile")

    arguments = [u"ffmpeg", u"-i", infile, outfile]

    return u" ".join(arguments)


def command_flac_conv(flac, **kwargs):
    infile = kwargs.get(u"infile")
    outfile = kwargs.get(u"outfile")

    arguments = [u"flac", u"-V", u'''-o "%s"''' % outfile, u'''--best''']

    time_begin = kwargs.get(u"_time_begin", None)
    if time_begin: arguments.append(u'''--skip=%s''' % cue_index_to_flac_time(time_begin))

    time_end = kwargs.get(u"_time_end", None)
    if time_end: arguments.append(u'''--until=%s''' % cue_index_to_flac_time(time_end))

    pic_cover = kwargs.get(u"_pic_cover", None)
    if pic_cover: arguments.append(u'''--picture="%s"''' % pic_cover)

    for tag in flac.list_tags():
        if not tag.startswith(u"_"):
            arguments.append(u'''--tag="%s"="%s"''' % (tag, flac.get_tag(tag)))

    arguments.append(u'''"%s"''' % infile)

    return u" ".join(arguments)


def cue_index_to_flac_time(timestr):
    """
    This function converts the time string in CUE file to the format that FLAC accepts.

    Time string in CUE file:  00:00:00

    Time string in FLAC file: 00:00.00
    """
    r = re.match(u'''(\d+:\d{2}):(\d{2})''', timestr)
    if r is None:
        raise ValueError("Invalid time string: %s" % timestr)

    g = r.groups()
    return u'''%s.%s''' % (g[0], g[1])

