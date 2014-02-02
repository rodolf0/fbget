#!/usr/bin/env python2

# https://developers.facebook.com/docs/graph-api/reference/user/

from .misc import Http


class GraphAPI(object):
    url = "https://graph.facebook.com"

    def __init__(self, credentials):
        """
        credentials: object obtained from the auth api
        """
        self.credentials = credentials

    def user_info(self, who="me"):
        h = self.credentials.authorize(Http())
        head, body = h.request("{}/{}".format(self.url, who))
        return head, body
