#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Misskey API Docs: https://misskey.io/api-doc
import json
import sqlite3
import requests
import xmltodict
import time

config_file = open('config.json', 'r')
config = json.loads(config_file.read())
config_file.close()
conn = sqlite3.connect('DB.sqlite3')
print("Opened database successfully")


def xml_to_json(xml):
    pars = xmltodict.parse(xml)
    return json.dumps(pars)


def spider(rule_name, rss_url):
    print("Fetch: ", rss_url)
    c = conn.cursor()
    result = xmltodict.parse(requests.get(rss_url).content)
    c.execute('INSERT INTO "main"."spider_log" ("rule_name", "rss_url", "result_json", "timestamp") '
              'VALUES (?, ?, ?, ?)', (rule_name, rss_url, json.dumps(result), time.time()))
    c.close()
    return result


if __name__ == '__main__':
    print("Misskey X61 RSS Bot")
    spider("duowei", "https://rsshub.app/dwnews/yaowen/global")
    conn.commit()
    conn.close()
