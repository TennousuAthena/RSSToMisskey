#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import re
import sqlite3
import requests
import xmltodict
import time
from misskey import Misskey
from bs4 import BeautifulSoup

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
              'VALUES (?, ?, ?, ?)', (rule_name, rss_url, "{}", time.time()))
    item_list = result['rss']['channel']['item']
    for i in item_list:
        unique = c.execute('SELECT * FROM "main"."result" WHERE "title" = ? LIMIT 0,1', (i['title'],)).fetchone()
        re_cdata = re.compile('//<![CDATA[[^>]*//]]>', re.I)
        title = re_cdata.sub('', i['title'])
        if not (unique is None):
            print("Skip: ", title)
            continue
        print("Got: ", title)
        desc = i['description'].replace("<blockquote>", "<i>“").replace("</blockquote>", "”</i>")
        c.execute('INSERT INTO "main"."result" ("rule_name", "url", "title", "description", "timestamp")'
                  ' VALUES (?, ?, ?, ?, ?)', (rule_name, i['link'], title, desc, time.time()))

    c.close()
    end = time.time()
    print("Fetch done in", end - start, "s")
    return result


def fetch_img(url):
    print()


if __name__ == '__main__':
    print("Misskey X61 RSS Bot initialized")

    config = json_read("config.json")
    rules = json_read("rules.json")

    for key in rules:
        spider(key, rules[key]['rss_source'])
        name = rules[key]['identity']
        Misskey.baseurl = config[name]['url']

        c = conn.cursor()
        r = c.execute('''SELECT * FROM "main"."result" 
        WHERE "rule_name" = ? AND
         "post_time" = '0' ORDER BY "rid" DESC''', (key,)).fetchone()
        if not(r is None):
            res = c.execute('UPDATE "main"."result" SET "post_time" = ? WHERE rowid = ?', (time.time(), r[0]))
            if not (res is None):
                reg = re.compile('<[^>]*>')
                desc = reg.sub('', r[4]).replace(' ', '').replace('\n\n\n', '\n')
                content = "**"+r[3]+"**\n\n"+desc+"\n<"+r[2]+">\n"+rules[key]['extra_content']
                if Misskey.debug:
                    config[name]['visibility'] = "specified"
                Misskey.post(self=Misskey,
                             content=content,
                             i=config[name]['token'], visibility=config[name]['visibility'])
    conn.commit()
    conn.close()

    time_end = time.time()
    print("X61 bot: done in", time_end - time_start, "s")
