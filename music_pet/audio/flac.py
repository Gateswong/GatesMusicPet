# -*- coding: utf-8 -*-

from . import AudioFile, PictureMixin

from ..utils import *


class FLAC(AudioFile, PictureMixin):

    def __init__(self, trackmeta=None):
        AudioFile.__init__(self, trackmeta)
        self.commandline = u"flac"

    def command(self):
        arguments = [self.commandline]

        # Output File
        arguments.append(u'''-o "%s"''' %
                         self.metadata.get_tag(u"@output_fullpath"))

        # Start Time
        if self.metadata.has_tag(u"@time_from"):
            arguments.append(u'''--skip=%s''' %
                             cue_index_to_flac_time(self.metadata.get_tag(u"@time_from")))

        # End Time
        if self.metadata.has_tag(u"@time_to"):
            arguments.append(u'''--until=%s''' %
                             cue_index_to_flac_time(self.metadata.get_tag(u"@time_to")))

        # Attach Tags
        for tag in self.metadata.list_tag():
            if not tag.startswith(u"@"):
                arguments.append(u'''--tag="%s"="%s"''' %
                                 (tag,
                                  cli.escape(self.metadata.get_tag(tag))))

        # Attach pictures
        if self.cover_picture is not None:
            arguments.append(u'''--picture=3||||"%s"''' %
                             self.cover_picture)

        if self.back_picture is not None:
            arguments.append(u'''--picture=4||||"%s"''' %
                             self.back_picture)

        # Set Quality
        arguments.append(u'''--best''')

        # Input File
        arguments.append(u'''%s''' % self.metadata.get_tag(u"@input_fullpath"))

        # Convert command
        return u" ".join(arguments)





