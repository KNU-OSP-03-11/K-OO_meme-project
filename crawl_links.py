#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from DB_Functions import * # mysql functions
okt = Okt() # 한글 명사분석
global check
check = 0
rank_list = rankFreq(10,0)
# process for collecting only words
def process( soup_selction_list ):
    global check
    global top_url
    flag = 0
    temp = []
    for content in soup_selction_list:
        if flag == 5:
            break
        link = content.attrs['href']
        title = content.get_text()
        temp.append([title,link])
        flag+=1
    top_url.append([rank_list[check][1],temp])
    check+=1

        

url_list = []
for i in range(10):
    url_list.append(u'https://search.naver.com/search.naver?where=news&query={}&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Aall&is_sug_officeid=0'.format(rank_list[i][1]))
global top_url
top_url = []
for url in url_list:
    res = requests.get(url)
    # implement BeautifulSoup
    soup = BeautifulSoup(res.content,"html.parser")
    # check for each types
    title = soup.select('a.news_tit')
    process(title)
for element in top_url:
    addlink(initLink(element[0],element[1][0][0],element[1][0][1],element[1][1][0],element[1][1][1],element[1][2][0],element[1][2][1],element[1][3][0],element[1][3][1],element[1][4][0],element[1][4][1]))