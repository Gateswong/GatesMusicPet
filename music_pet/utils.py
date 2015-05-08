# -*- coding: utf-8 -*-
import os
from codecs import encode, decode


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


def iconv_file(input_filename, output_filename, encoding, overwrite=False):
    fp = open(input_filename, "rb")
    ansi_content = fp.read()
    fp.close()
    if not overwrite:
        if os.path.exists(output_filename):
            return
    with open(output_filename, "w") as fp:
        if encoding.lower() in ["utf8", "utf-8", "u8", "utf", "utf_8"]:
            fp.write(ansi_content)
        else:
            fp.write(encode(
                decode(ansi_content, encoding),
                "utf8"))


def filename_safe(filename):
    for ch in u'''<>'"?*\\/:''':
        filename = filename.replace(ch, u"_")
    return filename.strip()


def cli_escape(text):
    for ch in u'''"''':
        text.replace(ch, u'''\\%s''' % ch)
    return text

