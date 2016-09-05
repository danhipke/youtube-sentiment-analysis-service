# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Python Youtube Data API
# ---------------------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Author:
# Daniel Hipke
# danhipke@yahoo.com
# ---------------------------------------------------------------------------
import urllib, urllib2


class YouTubeDataAPI(object):
    prefix_path = "https://www.googleapis.com/youtube/v3/"
    api_key = ""

    def _get_request(self, path, params={}):
        params["key"] = self.api_key
        url = "%s%s?%s" % (self.prefix_path, path, urllib.urlencode(params))
        try:
            return urllib2.urlopen(url).read()
        except urllib2.HTTPError, err:
            raise YouTubeException(err.read())

    def get_comment_threads(self, part="id,snippet", videoId="", order="relevance"):
        return self._get_request("commentThreads", {"part": part, "videoId": videoId, "order": order})


class YouTubeException(Exception):
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description



