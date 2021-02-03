#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Misskey API Docs: https://misskey.io/api-doc
import requests
import json


class Misskey:
    config = {}
    debug = True

    def post(self, baseurl, content, channel=""):
        print("Creating new post to", baseurl, ":", content)
        req_url = baseurl + "/api/notes/create"
        if self.debug:
            visb = "specified"
        else:
            visb = "public"
        body = {
            "visibility": visb,
            "text": content,
            "localOnly": channel != "",
            "i": self.config['token']
        }
        if channel != "":
            body["channelId"] = channel
        result = requests.post(req_url, json=body)
        if result.status_code == 200:
            return result
        else:
            print("Failed to post:", result.json()['error']['message'])
            return False
