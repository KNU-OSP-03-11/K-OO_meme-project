#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
import pymysql
from konlpy.tag import Okt
okt = Okt()

# process for collecting only words
def process( soup_selction_list ):
    global DATA_dic
    for content in soup_selction_list:
        title = content.get_text()
        sentence = re.findall(r"(?i)\b[a-zA-Z\-\u3131-\u3163\uac00-\ud7a3]+\b", title)
        #r"(?i)\b[a-z]+\b", content.get_text()
        # hangul = [^ \u3131-\u3163\uac00-\ud7a3]+
        # a-zA-Z^ \u3131-\u3163\uac00-\ud7a3
        # sentence = list(content.get_text().split())
        for word in sentence:
            if word.find("K") == 0 :
                noun = okt.nouns(word)
                if noun!=[]:
                    if word.find("-") == 1:
                        noun.insert(0,"K-")
                        word = ''.join(elements for elements in noun)
                    else:
                        noun.insert(0,"K")
                        word = ''.join(elements for elements in noun)
                if DATA_dic.get(word)==None:
                    DATA_dic[word] = 1
                else :
                    DATA_dic[word] += 1


url_list = []
url_list.append(u'https://search.naver.com/search.naver?where=news&query=K&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Aall&is_sug_officeid=0')
fp = open("output.txt",'w')
for i in range(1,20):
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
    
    print(words,file=fp)
fp.close()

    
