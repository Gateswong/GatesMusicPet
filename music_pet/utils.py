# -*- coding: utf-8 -*-
from codecs import decode


def trim_quote(text):
    if len(text) > 2 and text[0] == '"' and text[-1] == '"':
        text = text[1:-1]
    return text


def to_unicode(text, encoding="utf8"):
    if type(text) == unicode:
        return text

    elif type(text) == str:
        return decode(text, encoding)

    else:
        return unicode(text)


def remove_bom(input_filename, output_filename):
    fp = open(input_filename, "rb")
    bom = fp.read(3)
    if bom != b'\xef\xbb\xbf':
        raise ValueError("File doesn't have UTF-8 BOM")
    fo = open(output_filename, "wb")
    fo.write(fp.read())
    fo.close()
    fp.close()


