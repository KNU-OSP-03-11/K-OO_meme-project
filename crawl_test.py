#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
import pymysql
from konlpy.tag import Okt
okt = Okt() # 한글 명사분석
import time # 시간분석
start = time.time()

# process for collecting only words
def process( soup_selction_list ):
    global DATA_dic
    flag = 0
    for content in soup_selction_list:
        title = content.get_text()
        sentence = re.findall(r"(?i)\b[a-zA-Z\-\u3131-\u3163\uac00-\ud7a3]+\b", title)
        #r"(?i)\b[a-z]+\b", content.get_text()
        # hangul = [^ \u3131-\u3163\uac00-\ud7a3]+
        # a-zA-Z^ \u3131-\u3163\uac00-\ud7a3
        # sentence = list(content.get_text().split())
        for word in sentence:
            if flag == 1:
                word = ' '.join(["K",word])
                if DATA_dic.get(word)==None:
                    DATA_dic[word] = 1
                else :
                    DATA_dic[word] += 1
                flag = 0
                break
            if word.find("K") == 0 :
                noun = okt.nouns(word)
                if noun!=[]:
                    if word.find("-") == 1:
                        noun.insert(0,"K-")
                        word = ''.join(elements for elements in noun)
                    else:
                        noun.insert(0,"K")
                        word = ''.join(elements for elements in noun)
                if len(word)==1 :
                    flag = 1
                    continue
                if DATA_dic.get(word)==None:
                    DATA_dic[word] = 1
                else :
                    DATA_dic[word] += 1
                break


url_list = []
url_list.append(u'https://search.naver.com/search.naver?where=news&query=K&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Aall&is_sug_officeid=0')
fp = open("output.txt",'w') # 확인용
for i in range(1,1000):
    url_list.append(u"https://search.naver.com/search.naver?where=news&sm=tab_pge&query=K&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=18&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={}1".format(i))
# DATA_dic as dictionary of { "word" : "url" }
global DATA_dic
DATA_dic = {}
for url in url_list:
    res = requests.get(url)

    # implement BeautifulSoup
    soup = BeautifulSoup(res.content,"html.parser")

    

    # check for each types
    title = soup.select('a.news_tit')

    process(title)
words = list(DATA_dic.keys())
frequencies = list(DATA_dic.values())
    
for i in range(len(words)):
    print("{} {}".format(words[i],frequencies[i]),file=fp) # 확인용
print("time : ",time.time() - start,file=fp)
fp.close()# 확인용

    
