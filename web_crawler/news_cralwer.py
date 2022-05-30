#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
import psycopg2

# process for collecting only words
def process( soup_selction_list ):
    global DATA_dic
    for content in soup_selction_list:
        sentence = re.findall(r"(?i)\b[a-z]+\b", content.get_text())
        # sentence = list(content.get_text().split())
        for word in sentence:
            if DATA_dic.get(word)==None:
                DATA_dic[word] = 1
            else :
                DATA_dic[word] += 1


if __name__ == '__main__':
    url = u'https://en.wikipedia.org/wiki/Web_crawler'
    res = requests.get(url)

    # implement BeautifulSoup
    soup = BeautifulSoup(res.content,"html.parser")

    # DATA_dic as dictionary of { "word" : frequency }
    global DATA_dic
    DATA_dic = {}
    
    # check for each types
    title = soup.select('h1#firstHeading')
    sub_t = soup.select('div#siteSub')
    p_in_soup = soup.select('div.mw-parser-output > p')
    note_in_soup = soup.select('div.mw-parser-output > div.hatnote')
    h1_in_soup = soup.select('div.mw-parser-output h1')
    h2_in_soup = soup.select('div.mw-parser-output h2')
    h3_in_soup = soup.select('div.mw-parser-output h3')
    h4_in_soup = soup.select('div.mw-parser-output h4')
    h5_in_soup = soup.select('div.mw-parser-output h5')
    h6_in_soup = soup.select('div.mw-parser-output h6')
    list_in_soup = soup.select('div.mw-parser-output > ul > li')
    
    content = ( title, sub_t, p_in_soup, note_in_soup, h1_in_soup, h2_in_soup, h3_in_soup, h4_in_soup, h5_in_soup, h6_in_soup, list_in_soup )
    # get words and frequencies
    for lists in content:
        process(lists)
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