#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
import psycopg2
from konlpy.tag import Kkma

# process for collecting only words
def process( soup_selction_list ):
    global DATA_dic
    for content in soup_selction_list:
        title = content.get_text()
        sentence = re.findall(r"(?i)\b[a-zA-Z\u3131-\u3163\uac00-\ud7a3]+\b", title)
        #r"(?i)\b[a-z]+\b", content.get_text()
        # hangul = [^ \u3131-\u3163\uac00-\ud7a3]+
        # a-zA-Z^ \u3131-\u3163\uac00-\ud7a3
        # sentence = list(content.get_text().split())
        for word in sentence:
            if DATA_dic.get(word)==None:
                DATA_dic[word] = 
            else :
                DATA_dic[word] += 1


url_list = []
url_list.append(u'https://search.naver.com/search.naver?where=news&query=K&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Aall&is_sug_officeid=0')
for i in range(1,1000):
    url_list.append(u"https://search.naver.com/search.naver?where=news&sm=tab_pge&query=K&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=18&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={}1".format(i))
for url in url_list:
    res = requests.get(url)

    # implement BeautifulSoup
    soup = BeautifulSoup(res.content,"html.parser")

    # DATA_dic as dictionary of { "word" : "url" }
    global DATA_dic
    DATA_dic = {}

    # check for each types
    title = soup.select('a.news_tit')

    process(title)
    words = list(DATA_dic.keys())
    frequencies = list(DATA_dic.values())

    # use psycopg2 to save data in PostgreSQL
    host = "localhost"
    dbname = "test"
    user = "t_usr"
    password = "passwd"
    sslmode = "require"

    # make into string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    # connect to PostgreSQL
    conn = psycopg2.connect(conn_string) 
    # set cursor
    cursor = conn.cursor()
    # drop previous table of same name if one exists
    cursor.execute("DROP TABLE IF EXISTS inventory;")
    # create a table
    cursor.execute("CREATE TABLE inventory (id serial PRIMARY KEY, url VARCHAR(255), word VARCHAR(50), frequency INTEGER);")
    # insert (url, word, frequency)
    for i in range(len(words)):
        cursor.execute("INSERT INTO inventory (url, word, frequency) VALUES (%s, %s, %s);",(url,words[i],frequencies[i]))
    # check if it is stored
    cursor.execute("SELECT * FROM inventory;")
    rows = cursor.fetchall()
    # # print all rows
    # for row in rows:
    #     print("DATA stored = (%s, %s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2]), str(row[3])))
    # cleanup
    conn.commit()
    cursor.close()
    conn.close()
