# -*- coding: utf-8 -*-

__all__ = [
    "FLAC",
    "init_flacs",
]

import re
from uuid import uuid4

from .base import AudioFile, PictureMixin

from ..meta import (
    Album,
)
from ..utils import (
    to_unicode as u,
    cli_escape,
    filename_safe,
    ensure_parent_folder,
    path_from_pattern,
)


class FLAC(AudioFile, PictureMixin):

    def __init__(self, trackmeta=None):
        AudioFile.__init__(self, trackmeta)
        self.commandline = u"flac"
        self.commandline_decoder = u"ffmpeg"

    def command(self):
        arguments = [self.commandline]

        # Output File
        arguments.append(u'''-o "%s"''' %
                         self.metadata.get_tag(u"@output_fullpath"))

        # Start Time
        if self.metadata.has_tag(u"@time_from"):
            arguments.append(u'''--skip=%s''' %
                             cue_index_to_flac_time(self.metadata.get_tag(u"@time_from")))
        elif self.metadata.has_tag(u"index_00"):
            arguments.append(u'''--skip=%s''' %
                             cue_index_to_flac_time(self.metadata.get_tag(u"index_00")))

        # End Time
        if self.metadata.has_tag(u"@time_to"):
            arguments.append(u'''--until=%s''' %
                             cue_index_to_flac_time(self.metadata.get_tag(u"@time_to")))

        # Attach Tags
        for tag in self.metadata.list_tag():
            if not tag.startswith(u"@"):
                arguments.append(u'''--tag="%s"="%s"''' %
                                 (tag,
                                  cli_escape(self.metadata.get_tag(tag))))

        # Attach pictures
        if self.cover_picture is not None:
            arguments.append(u'''--picture="3||||%s"''' %
                             self.cover_picture)

        if self.back_picture is not None:
            arguments.append(u'''--picture="4||||%s"''' %
                             self.back_picture)

        # Set Quality
        arguments.append(u'''--best''')

        # Verify the result
        arguments.append(u'''-V''')

        # Input File
        arguments.append(u'''"%s"''' % self.metadata.get_tag(u"@input_fullpath"))

        # Convert command
        return u" ".join(arguments).replace(u"`", u"\\`")

    def command_build_tempwav(self, memoize={}):
        arguments = [self.commandline_decoder]

        if self.get_tag(u"@input_fullpath") in memoize:
            self.set_tag(u"@input_fullpath_original", self.get_tag(u"@input_fullpath"))
            self.set_tag(u"@input_fullpath", memoize[self.get_tag(u"@input_fullpath")])
            return u"pwd"

        # Input file
        if self.has_tag(u"@input_fullpath_original"):
            arguments.append(u'''-i "%s"''' % self.get_tag(u"@input_fullpath_original"))
        else:
            self.set_tag(u"@input_fullpath_original", self.get_tag(u"@input_fullpath"))
            arguments.append(u'''-i "%s"''' %
                             self.get_tag(u"@input_fullpath"))

        # Output file
        ofile = u'''__tmp_%s.wav''' % (uuid4())
        arguments.append(u'''"%s"''' % ofile)
        self.set_tag(u"@input_fullpath", ofile)
        memoize[self.get_tag(u"@input_fullpath_original")] = ofile

        return u" ".join(arguments).replace(u"`", u"\\`")

    def command_clear_tempwav(self, base_command=u"rm"):
        arguments = [base_command]

        if self.has_tag(u"@input_fullpath_original"):
            arguments.append(self.get_tag(u"@input_fullpath"))

            return " ".join(arguments).replace(u"`", u"\\`")
        return "pwd"

    def set_input_file(self, wavfile):
        if not wavfile.endswith(u".wav"):
            raise ValueError("Only accepts wav file as input files")

        self.set_tag(u"@input_fullpath_original", self.get_tag(u"@input_fullpath"))
        self.set_tag(u"@input_fullpath", wavfile)

    def set_next_start_time_from_album(self, album):
        if self.metadata.tracknumber is None:
            return None

        if type(album) != Album:
            raise ValueError("not an instance of Album")

        nexttrack = album.get_track(int(self.metadata.tracknumber) + 1)
        if nexttrack is None:
            return None

        if nexttrack.has_tag(u"@input_fullpath") and self.has_tag(u"@input_fullpath"):
            if nexttrack.get_tag(u"@input_fullpath") != self.get_tag(u"@input_fullpath"):
                return

        if nexttrack.has_tag(u"original_file") and self.has_tag(u"original_file"):
            if nexttrack.get_tag(u"original_file") != self.get_tag(u"original_file"):
                return
        else:
            return

        if nexttrack.has_tag(u"index_00"):
            self.set_tag(u"@time_to", nexttrack.get_tag(u"index_00"))
        elif nexttrack.has_tag(u"index_01"):
            self.set_tag(u"@time_to", nexttrack.get_tag(u"index_01"))

    def set_next_start_time(self, tstr):
        self.set_tag(u"@time_to", cue_index_to_flac_time(tstr))

    def set_output_file(self, pattern):
        self.set_tag(u"@output_fullpath",
                     filename_safe(path_from_pattern(pattern, self.metadata.data)))

    def set_input_file(self, filename):
        self.set_tag(u"@input_fullpath",
                     filename_safe(filename))

    def create_target_dir(self):
        ensure_parent_folder(self.get_tag(u"@output_fullpath"))


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


def init_flacs(album, output_pattern):
    if not album:
        return []

    flacs = []

    for track in album:
        flac = FLAC(track.data)
        if not flac.has_tag(u"index_00") and flac.has_tag(u"index_01"):
            flac.set_tag(u"index_00", flac.get_tag(u"index_01"))
        flac.set_next_start_time_from_album(album)
        flac.set_output_file(output_pattern)
        flacs.append(flac)

    return flacs

