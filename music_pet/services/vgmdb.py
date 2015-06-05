# -*-: coding: utf-8 -*-

import requests
import json
import re

from ..audio import AudioTrack


LANGS = {
    u"jp": (u"jp", u"Japanese"),
    u"en": (u"en", u"English"),
}


def _get_json_by_link(link):
    url = u'''http://vgmdb.info/%s''' % link
    return _get_json(url)


def _get_json(url):
    resp = requests.get(url, timeout=5)
    if resp.status_code != 200:
        raise Exception("Failed to search from VGMdb! Error Code = %d" % resp.status_code)

    d = resp.json()

    return d


# Functions with Search API
def search_all(keyword):
    d = _get_json_by_link(u'''search/"%s"?format=json''' % keyword)
    _validate_search_result(d)

    return d[u"results"]


def search_albums(keyword):
    d = _get_json_by_link(u'''search/albums/"%s"?format=json''' % keyword)
    _validate_search_result(d)

    return d[u"results"]


def search_artists(keyword):
    d = _get_json_by_link(u'''search/artists/"%s"?format=json''' % keyword)
    _validate_search_result(d)

    return d[u"results"]


def search_orgs(keyword):
    d = _get_json_by_link(u'''search/orgs/"%s"?format=json''' % keyword)
    _validate_search_result(d)

    return d[u"results"]


def search_products(keyword):
    d = _get_json_by_link(u'''search/products/"%s"?format=json''' % keyword)
    _validate_search_result(d)

    return d[u"results"]


def _validate_search_result(search_result):
    for key in [u"results", u"sections"]:
        if key not in search_result:
            raise ValueError("Invalid search result: field '%s' required!" % key)

    for key in search_result[u"sections"]:
        if key not in search_result[u"results"]:
            raise ValueError("Invalid search result: in field 'results', field '%s' required!"
                             % key)


# Functions with Infomation API
def get_album(id):
    d = _get_json_by_link(u'''album/%s''' % id)
    return d


def get_artist(id):
    d = _get_json_by_link(u'''artist/%s''' % id)
    return d


def get_org(id):
    d = _get_json_by_link(u'''org/%s''' % id)
    return d


def get_product(id):
    d = _get_json_by_link(u'''product/%s''' % id)
    return d


def get_event(id):
    d = _get_json_by_link(u'''event/%s''' % id)
    return d


# Utility
def disc(num):
    return u"Disc %s" % num


# Functions that producing data from JSON (dict)
def album_get_cover_picture(album_info, size="full"):
    if u"covers" not in album_info:
        return None

    for cover_dict in album_info[u"covers"]:
        if cover_dict[u"name"].lower() in [u"front", u"cover", u"folder"]:
            return cover_dict[size]


def album_tracks(album_info, discname, lang=u"en"):
    for disc in album_info[u"discs"]:
        if disc[u"name"] == discname:
            tracks = []
            for track in disc[u"tracks"]:
                tracks.append(track[u"names"].get(
                    LANGS[lang][1],
                    track[u"names"][u"English"]
                ))
            return tracks


def update(album_info, track, lang=u"en"):
    if not isinstance(track, AudioTrack):
        raise TypeError("Instance is not a Meta object")

    update_album_title(album_info, track, lang=lang)
    # update_artist(album_info, track, lang=lang)
    update_album_artist(album_info, track, lang=lang)
    update_catalog(album_info, track, lang=lang)
    update_category(album_info, track, lang=lang)
    update_cover_picture(album_info, track, lang=lang)
    update_title(album_info, track, lang=lang)

    return


def update_album_title(album_info, track, lang=u"en"):
    track.ALBUM = album_info[u"names"].get(
        LANGS[lang][0],
        album_info[u"names"][u"en"]
    )


def update_album_artist(album_info, track, lang=u"en"):
    composers = u""
    for composer in album_info[u"composers"]:
        composers += u", %s" % composer[u"names"].get(
            LANGS[lang][0],
            composer[u"names"][u"en"]
        )
    track.ALBUMARTIST = composers[2:]


def update_catalog(album_info, track, lang=u"en"):
    if u"catalog" in album_info:
        track[u"CATALOG"] = album_info[u"catalog"]


def update_category(album_info, track, lang=u"en"):
    if u"category" in album_info:
        track[u"CATEGORY"] = album_info[u"category"]


def update_cover_picture(album_info, track, lang=u"en"):
    track[u"_picture"] = album_get_cover_picture(album_info)


def update_title(album_info, track, lang=u"en"):
    if track.DISCNUMBER is None:
        discname = u"Disc 1"
    else:
        discname = disc(track.DISCNUMBER)

    track_names = album_tracks(album_info, discname, lang=lang)
    track.TITLE = track_names[int(track.TRACKNUMBER) - 1]


def album_detail(album_info, lang=u"English", lang_short=u"en"):
    detail_string = u""

    if lang_short in album_info[u"names"]:
        detail_string += u"TITLE : %s\n" % album_info[u"names"][lang_short]
    else:
        detail_string += u"TITLE : %s\n" % album_info[u"name"]

    detail_string += u"\nCOMPOSER :\n"

    for composer in album_info[u"composers"]:
        if lang_short in composer[u"names"]:
            detail_string += u"%s\n" % composer[u"names"][lang_short]
        else:
            detail_string += u"%s\n" % composer[u"names"][u"en"]

    for disc in album_info[u"discs"]:
        detail_string += u"\nIn : %s\n" % disc[u"name"]
        for track_id, track in enumerate(disc[u"tracks"]):
            detail_string += u"  %s : %s\n" % (
                str(track_id + 1).zfill(2),
                track[u"names"][lang] if lang in track[u"names"] else track[u"names"]["English"])

    return detail_string


# Functions for details
def print_album_detail(album_info, lang=u"English", lang_short=u"en"):
    print(album_detail(album_info, lang, lang_short))

