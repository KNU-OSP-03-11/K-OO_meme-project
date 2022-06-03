#!/usr/bin/python
#-*- coding: utf-8 -*-

import pymysql

if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='root', password='k-oo1234', db='KOO', charset='utf8')
    cur = conn.cursor()
    tableSTR = "CREATE TABLE KOOtable(word VARCHAR(30) UNIQUE KEY,title VARCHAR(50), useFreq INT,searchFreq INT)"
    cur.execute(tableSTR)
    conn.commit()
    conn.close()
    print("created table 'KOOtable'")
