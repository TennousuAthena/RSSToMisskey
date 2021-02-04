#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Misskey API Docs: https://misskey.io/api-doc
import requests
import re


class Misskey:
    debug = True
    baseurl = ""

    def post(self, content, i, channel="", visibility="public",):
        print("Creating new post to", self.baseurl, ":", content)
        req_url = self.baseurl + "/api/notes/create"
        body = {
            "visibility": visibility,
            "text": content,
            "localOnly": channel != "",
            "i": i
        }
        if channel != "":
            body["channelId"] = channel
        result = requests.post(req_url, json=body)
        if result.status_code == 200:
            return True
        else:
            print("Failed to post:", result.json()['error']['message'])
            return False

    def upload_from_url(self, i, url):
        print("Uploading img to misskey")
        req_url = self.baseurl + "/api/drive/files/upload-from-url"
        body = {
            "url": url,
            "i": i
        }
        r = requests.post(req_url, json=body)
        if r.status_code == 204:
            print("Done!")
            return True
        else:
            print("Failed to upload:", r.json()['error']['message'])
            return False
