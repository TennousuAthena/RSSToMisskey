#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Misskey API Docs: https://misskey.io/api-doc
import requests
import json


class Misskey:
    config = {}
    debug = True

    def post(self, baseurl, content, channel="", visibility="public"):
        print("Creating new post to", baseurl, ":", content)
        req_url = baseurl + "/api/notes/create"
        body = {
            "visibility": visibility,
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
