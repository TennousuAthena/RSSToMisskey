#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import sqlite3
import requests
import xmltodict
import time
from misskey import Misskey

time_start = time.time()
print(
    '''  __  __ _         _                       __ __ _           _   \n |  \/  (_)       | |                     / //_ | |         | |  \n | \  / |_ ___ ___| | _____ _   _  __  __/ /_ | | |__   ___ | |_ \n | |\/| | / __/ __| |/ / _ \ | | | \ \/ / '_ \| | '_ \ / _ \| __|\n | |  | | \__ \__ \   <  __/ |_| |  >  <| (_) | | |_) | (_) | |_ \n |_|  |_|_|___/___/_|\_\___|\__, | /_/\_\\___/|_|_.__/ \___/ \__|\n                             __/ |                               \n                            |___/                                ''')
conn = sqlite3.connect('DB.sqlite3')
print("Opened database successfully")


def json_read(file):
    config_file = open(file, 'r')
    config = json.loads(config_file.read())
    config_file.close()
    return config

def xml_to_json(xml):
    pars = xmltodict.parse(xml)
    return json.dumps(pars)


def spider(rule_name, rss_url):
    print("Fetch RSS: [" + rule_name + "] ", rss_url)
    start = time.time()
    c = conn.cursor()
    fetch = requests.get(rss_url)
    if fetch.status_code != 200:
        print("Failed to fetch")
        return False
    result = xmltodict.parse(fetch.content)
    c.execute('INSERT INTO "main"."spider_log" ("rule_name", "rss_url", "result_json", "timestamp") '
              'VALUES (?, ?, ?, ?)', (rule_name, rss_url, json.dumps(result), time.time()))
    c.close()
    end = time.time()
    print("Fetch done in", end - start, "s")
    return result


def fetch_detail(url):
    print()


if __name__ == '__main__':
    print("Misskey X61 RSS Bot initialized")
    spider("DuoWei", "https://rsshub.app/dwnews/yaowen/global")

    config = json_read("config.json")
    rules = json_read("rules.json")

    Misskey.config = config['misskey.io']

    req = Misskey.post(baseurl="https://misskey.io", content="Beep.. Beep Beep! Beep:" + str(time.time()), self=Misskey)
    conn.commit()
    conn.close()

    time_end = time.time()
    print("X61 bot: done in", time_end - time_start, "s")
