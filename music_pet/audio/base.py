from ..utils import to_unicode as u
from ..meta import *

__all__ = [
    "AudioFile",
    "PictureMixin",
]


class AudioFile(object):

    def __init__(self, trackmeta=None):
        if trackmeta is not None:
            self.metadata = Track(trackmeta)
        else:
            self.metadata = Track()

    def has_tag(self, tag):
        return self.metadata.has_tag(tag)

    def get_tag(self, tag):
        return self.metadata.get_tag(tag)

    def set_tag(self, tag, value):
        self.metadata.set_tag(tag, value)

    def list_tag(self):
        return self.metadata.list_tag()


class PictureMixin(object):

    def set_picture(self, pic_index, pic_file):
        self.metadata.set_tag(u"@picture_%s" % pic_index, pic_file)

    @property
    def cover_picture(self):
        if self.metadata.has_tag(u"@cover_picture"):
            return self.metadata.get_tag(u"@cover_picture")
        return None

    @cover_picture.setter
    def cover_picture(self, value):
        self.metadata.set_tag(u"@cover_picture", u(value))

    @cover_picture.deleter
    def cover_picture(self):
        if self.metadata.has_tag(u"@cover_picture"):
            del self.metadata.data[u"@cover_picture"]

    @property
    def back_picture(self):
        if self.metadata.has_tag(u"@back_picture"):
            return self.metadata.get_tag(u"@back_picture")
        return None

    @back_picture.setter
    def back_picture(self, value):
        self.metadata.set_tag(u"@back_picture", u(value))

    @back_picture.deleter
    def back_picture(self):
        if self.metadata.has_tag(u"@back_picture"):
            del self.metadata.data[u"@back_picture"]

    @property
    def disc_picture(self):
        if self.metadata.has_tag(u"@disc_picture"):
            return self.metadata.get_tag(u"@disc_picture")
        return None

    @disc_picture.setter
    def disc_picture(self, value):
        self.metadata.set_tag(u"@disc_picture", u(value))

    @disc_picture.deleter
    def disc_picture(self):
        if self.metadata.has_tag(u"@disc_picture"):
            del self.metadata.data[u"@disc_picture"]


