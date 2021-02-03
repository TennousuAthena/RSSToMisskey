#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Misskey API Docs: https://misskey.io/api-doc
import json
import sqlite3
import requests
import xmltodict
import time

time_start = time.time()
print(
    '''  __  __ _         _                       __ __ _           _   \n |  \/  (_)       | |                     / //_ | |         | |  \n | \  / |_ ___ ___| | _____ _   _  __  __/ /_ | | |__   ___ | |_ \n | |\/| | / __/ __| |/ / _ \ | | | \ \/ / '_ \| | '_ \ / _ \| __|\n | |  | | \__ \__ \   <  __/ |_| |  >  <| (_) | | |_) | (_) | |_ \n |_|  |_|_|___/___/_|\_\___|\__, | /_/\_\\___/|_|_.__/ \___/ \__|\n                             __/ |                               \n                            |___/                                ''')
config_file = open('config.json', 'r')
config = json.loads(config_file.read())
config_file.close()
conn = sqlite3.connect('DB.sqlite3')
print("Opened database successfully")


def xml_to_json(xml):
    pars = xmltodict.parse(xml)
    return json.dumps(pars)


def misskey_post(baseurl, content, channel=""):
    print("Creating new post to", baseurl, ":", content)
    req_url = baseurl + "/api/notes/create"
    body = {
        "visibility": "specified",
        "text": content,
        "localOnly": channel != "",
        "i": "0v1t2poJeEh9RI74VqCCzJLHk9N6Wyds"
    }
    if channel != "":
        body["channelId"] = channel
    result = requests.post(req_url, json=body)
    if result.status_code == 200:
        return result
    else:
        print("Failed to post:", result.json()['error']['message'])
        return False


def spider(rule_name, rss_url):
    print("Fetch: [" + rule_name + "] ", rss_url)
    time_start = time.time()
    c = conn.cursor()
    fetch = requests.get(rss_url)
    if fetch.status_code != 200:
        print("Failed to fetch")
        return False
    result = xmltodict.parse(fetch.content)
    c.execute('INSERT INTO "main"."spider_log" ("rule_name", "rss_url", "result_json", "timestamp") '
              'VALUES (?, ?, ?, ?)', (rule_name, rss_url, json.dumps(result), time.time()))
    c.close()
    time_end = time.time()
    print("Fetch done in", time_end - time_start, "s")
    return result


if __name__ == '__main__':
    print("Misskey X61 RSS Bot initialized")
    spider("duowei", "https://rsshub.app/dwnews/yaowen/global")

    req = misskey_post("https://misskey.io", "Beep.. Beep Beep! Beep:"+str(time.time()))
    conn.commit()
    conn.close()

    time_end = time.time()
    print("X61 bot: done in", time_end - time_start, "s")
