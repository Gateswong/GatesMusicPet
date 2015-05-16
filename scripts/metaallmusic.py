from music_pet.meta import *
import argparse
import os


def print_dir_meta():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", type=unicode,
                    nargs="?",
                    help="The folder which contains the files.")
    ap.add_argument("-C", type=unicode,
                    nargs="?",
                    help="Encoding for ANSI CUE files")
    args = ap.parse_args()
    if args.folder is None:
        args.folder = u"."

    if args.C is None:
        args.C = u"utf8"

    all_files = os.listdir(args.folder)
    utf8_cue_files = filter(lambda f: f.endswith(".utf8.cue"),
                            all_files)
    ansi_cue_files = filter(lambda f: f.endswith(".cue") and
                            u"%s.utf8.cue" % f[:-4] not in utf8_cue_files and
                            f not in utf8_cue_files,
                            all_files)

    all_prefix = set()
    all_prefix.update(map(lambda f: f[:-9], utf8_cue_files))
    all_prefix.update(map(lambda f: f[:-4], ansi_cue_files))

    for f in all_prefix:
        for album in parse_cue(f, args.C).values():
            for line in album.detail():
                print(line)

    print("DEBUG: args=%s" % args)

