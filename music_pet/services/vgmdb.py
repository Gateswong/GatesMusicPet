# -*-: coding: utf-8 -*-

import requests
import json
import re

from ..meta import Album


def _get_json_by_link(link):
    url = u'''http://vgmdb.info/%s''' % link
    return _get_json(url)


def _get_json(url):
    resp = requests.get(url)
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


# Functions that producing data from JSON (dict)
def url_for_album_cover_picture(album_info, size="full"):
    if u"covers" not in album_info:
        return None

    for cover_dict in album_info[u"covers"]:
        if cover_dict[u"name"].lower() in [u"front", u"cover", u"folder"]:
            return cover_dict[u"full"]


def album_tracks(album_info, lang=u"English"):
    if u"discs" not in album_info:
        return {}

    discs = {}

    for disc_dict in album_info[u"discs"]:
        r = re.match(u'''Disc (\d+)''', disc_dict[u"name"])
        if not r:
            disc_num = disc_dict[u"name"]
        else:
            disc_num = r.groups()[0]
        discs[disc_num] = []

        for track in disc_dict[u"tracks"]:
            if lang not in track[u"names"]:
                raise ValueError("Can't find track info with language: %s" % lang)
            discs[disc_num].append(track[u"names"][lang])

    return discs


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


# Functions that working with other modules
def update_album(album_info, album, lang=u"English"):
    if not isinstance(album, Album):
        raise TypeError("update_album only accepts instance of Album")

    discs = album_tracks(album_info, lang=lang)

    # First pass: Assume all tracks info exists in the result from vgmdb.
    for track in album:
        if int(track.discnumber) not in discs:
            raise ValueError("Can't find the track info from the result of vgmdb.")

        if int(track.tracknumber) > len(discs[int(track.discnumber)]):
            raise ValueError("Can't find the track info from the result of vgmdb.")

    # Second pass: Update all tracks' info.
    for track in album:
        track.title = discs[int(track.discnumber)][int(track.tracknumber)-1]

    return


# Functions for details
def print_album_detail(album_info, lang=u"English", lang_short=u"en"):
    print(album_detail(album_info, lang, lang_short))

