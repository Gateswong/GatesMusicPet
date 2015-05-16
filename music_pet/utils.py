# -*- coding: utf-8 -*-
import os
from codecs import encode, decode
import re


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
    parts = filename.split(u"/")
    for i in xrange(len(parts)):
        for ch in u'''<>'"?*\\/:''':
            parts[i] = parts[i].replace(ch, u"_").strip()
    return u"/".join(parts).strip()


def path_from_pattern(pattern, d):
    all_keys = {}
    group_stack = []
    buffer = ""

    # parse all the keys in the pattern string
    iter_formats = re.finditer(u'''%\(([^)]+)\)s''', pattern)
    for f in iter_formats:
        all_keys[f.span()[0]] = (
            f.groups()[0],
            f.span()[1] - f.span()[0]
        )

    # parse the pattern
    i = 0  # current position in pattern string
    while i < len(pattern):
        # Case 1: we meet %(xxx)s
        if i in all_keys:  # if we find a key %(xxx)s
            if not group_stack:  # not in option fields:
                if all_keys[i][0] in d:  # the key exists in `d`
                    buffer += d[all_keys[i][0]]
                i += all_keys[i][1]
            else:
                if all_keys[i][0] in d:
                    group_stack[-1] += d[all_keys[i][0]]
                    i += all_keys[i][1]
                else:  # doesn't exists, skip all for this optional field
                    while i < len(pattern):
                        if pattern[i] == u">": break
                        i += 1
                    i += 1
                    group_stack.pop()
            continue

        # Case 2: we meet a `<`
        if pattern[i] == u"<":
            group_stack.append("")
            i += 1
            continue

        # Case 3: we meet a `>`
        if pattern[i] == u">":
            if not group_stack:
                raise ValueError("Invalid pattern! (unmatched `>`)")

            opt_str = group_stack.pop()
            if not group_stack:
                buffer += opt_str
            else:
                group_stack[-1] += opt_str

            i += 1
            continue

        # Otherwise
        if not group_stack:
            buffer += pattern[i]
        else:
            group_stack[-1] += pattern[i]
        i += 1

    if len(group_stack):
        raise ValueError("Invalid pattern! (lack of `>`)")
    return buffer


def cli_escape(text):
    for ch in u'''"''':
        text = text.replace(ch, u'''\\%s''' % ch)
    return text


def parent_folder(path):
    parts = path.split(u"/")
    if parts[-1] == u"":
        del parts[-1]
    parts[-1] = u""
    return u"/".join(parts)


def ensure_parent_folder(path):
    try:
        os.makedirs(parent_folder(path), mode=0755)
    except OSError, e:
        if e.errno != os.errno.EEXIST:
            raise


def command_copy_to(files, folder, base_command=u"cp"):
    arguments = [base_command]

    arguments.append(u"-n")

    for f in files:
        arguments.append(u'''"%s"''' % f)

    if not folder.endswith(u"/"):
        folder += u"/"
    arguments.append(u'''"%s"''' % folder)

    return u" ".join(arguments)

