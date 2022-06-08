#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from DB_Functions import * # mysql functions
okt = Okt() # 한글 명사분석
 
# process for collecting only words
def process( soup_selction_list ):
    global DATA_dic
    global DATA_T_dic
    flag = 0
    for content in soup_selction_list:
        link = content.attrs['href']
        title = content.get_text()
        sentence = re.findall(r"(?i)\b[a-zA-Z\-\u3131-\u3163\uac00-\ud7a3]+\b", title)
        #r"(?i)\b[a-z]+\b", content.get_text()
        # hangul = [^ \u3131-\u3163\uac00-\ud7a3]+
        # a-zA-Z^ \u3131-\u3163\uac00-\ud7a3
        # sentence = list(content.get_text().split())
        for word in sentence:
            if flag == 1: # if K + ' ' + word
                word = ' '.join(["K-",word])
                if DATA_dic.get(word)==None:
                    DATA_dic[word] = 1
                    DATA_T_dic[word] = " ".join(sentence)
                    DATA_U_dic[word] = link
                else :
                    DATA_dic[word] += 1
                flag = 0
                break
            if word.find("K") == 0 : # found K-word
                noun = okt.nouns(word)
                if noun!=[]:
                    if word.find("-") == 1:
                        noun.insert(0,"K-")
                        word = ''.join(elements for elements in noun)
                    else:
                        noun.insert(0,"K-")
                        word = ''.join(elements for elements in noun)
                if len(word)==1 : # if K + ' ' + word
                    flag = 1
                    continue
                if DATA_dic.get(word)==None:
                    DATA_dic[word] = 1
                    DATA_T_dic[word] = " ".join(sentence)
                    DATA_U_dic[word] = link
                else :
                    DATA_dic[word] += 1
                break

url_list = []
url_list.append(u'https://search.naver.com/search.naver?where=news&query=K&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Aall&is_sug_officeid=0')
for i in range(1,10):
    url_list.append(u"https://search.naver.com/search.naver?where=news&sm=tab_pge&query=K&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=18&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={}1".format(i))
global DATA_dic
DATA_dic = {}
global DATA_T_dic
DATA_T_dic = {}
global DATA_U_dic
DATA_U_dic = {}
for url in url_list:
    res = requests.get(url)
    # implement BeautifulSoup
    soup = BeautifulSoup(res.content,"html.parser")
    # check for each types
    title = soup.select('a.news_tit')
    process(title)
words = list(DATA_dic.keys())
frequencies = list(DATA_dic.values())
title_s = list(DATA_T_dic.values())
links = list(DATA_U_dic.values())
for i in range(len(words)):
    addMeme(initMeme(words[i],title_s[i],links[i],frequencies[i],0))