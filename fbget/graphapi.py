#!/usr/bin/env python2

# https://developers.facebook.com/docs/graph-api/reference/user/

from .misc import Http
from datetime import datetime
from multiprocessing.pool import ThreadPool
import os, errno
import logging
import json


class GraphAPI(object):
    url = "https://graph.facebook.com"

    def __init__(self, credentials):
        """
        credentials: object obtained from the auth api
        """
        self.credentials = credentials

    def user_info(self, who="me"):
        "Get user basic info"
        h = self.credentials.authorize(Http())
        resp, body = h.request("{}/{}".format(self.url, who))
        assert resp.status == 200
        return json.loads(body)

    def photos(self, who="me"):
        """
        Get photo info where user is tagged
        https://developers.facebook.com/docs/graph-api/reference/photo
        """
        h = self.credentials.authorize(Http())
        next_url = "{}/{}/photos".format(self.url, who)
        data = []
        while next_url:
            resp_h, resp_b = h.request(next_url)
            assert resp_h.status == 200
            resp = json.loads(resp_b)
            data.extend(resp["data"])
            next_url = resp.get("paging", {}).get("next")
        return data



class PhotoSync(object):
    TIME_FMT = '%Y-%m-%dT%H:%M:%S'

    def __init__(self, credentials, outdir, photo_data):
        self.credentials = credentials
        self.outdir = outdir
        self.data = photo_data
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        elif not os.path.isdir(outdir):
            raise ValueError("outdir cannot be an existing file")

    def sync_one(self, photo, force=False):
        photoinfo = os.path.join(self.outdir, photo.get("id") + ".info")
        extension = photo.get("source").rsplit(".", 1)[1]
        photodata = os.path.join(self.outdir, photo.get("id") + "." + extension)
        try:
            with open(photoinfo) as pi:
                info = json.load(pi)
        except IOError as error:
            if error.errno != errno.ENOENT:
                raise
            info = {}
        fb_dt = datetime.strptime(photo.get("updated_time")[:19], self.TIME_FMT)
        if "updated_time" in info:
            fs_dt = datetime.strptime(info.get("updated_time")[:19], self.TIME_FMT)
        else:
            fs_dt = datetime.min
        # photo was changed from last sync (possibly only caption but can't tell)
        if force or fs_dt < fb_dt:
            logging.info("Getting %s from: %s", photo.get("id"))
            h = self.credentials.authorize(Http())
            resp_h, resp_b = h.request(photo.get("source"))
            assert resp_h.status == 200
            with open(photodata, "w") as pd:
                pd.write(resp_b)
        else:
            logging.info("Skipping %s from: %s", photo.get("id"))
        with open(photoinfo, "w") as pi:
            json.dump(photo, pi, indent=2)

    def sync(self):
        tp = ThreadPool()
        tp.map(self.sync_one, self.data)
        tp.close()
