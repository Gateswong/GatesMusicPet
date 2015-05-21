# -*-: coding:utf-8 -*-

import requests
import json


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
        discs[disc_dict[u"name"]] = []

        for track in disc_dict[u"tracks"]:
            if lang not in track[u"names"]:
                raise ValueError("Can't find track info with language: %s" % lang)
            discs[disc_dict[u"name"]].append(track[u"names"][lang])

    return discs




