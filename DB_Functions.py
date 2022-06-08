#!/usr/bin/python
# It's for connecting with mySQL database
import string
import pymysql
from dataclasses import dataclass

# -------------------------memeClass------------------------------
@dataclass
class memeClass:
    word: str = None
    title: str = None
    link: str = None
    useFreq: int = None
    searchFreq: int = None

@dataclass
class linkClass:
    word: str = None
    title: str = None
    link1: str = None
    link2: str = None
    link3: str = None
    link4: str = None
    link5: str = None

# -------------------------functions------------------------------
# initMeme, searchMeme, addMeme, updateUseFreq, updateSearchFreq, rankMeme, delMeme

# create new Meme // parameter: str, str, int, int
def initMeme(word, title, link, useFreq, searchFreq):
    meme = memeClass()
    meme.word = word
    meme.title = title
    meme.link = link
    meme.useFreq = useFreq
    meme.searchFreq = searchFreq
    #if (searchMeme(meme) == 1):
    #    return False
    return meme

def initLink(word, title1, link1, title2, link2,title3, link3,title4, link4,title5, link5):
    link_s = linkClass()
    link_s.word = word
    link_s.title1 = title1
    link_s.link1 = link1
    link_s.title2 = title2
    link_s.link2 = link2
    link_s.title3 = title3
    link_s.link3 = link3
    link_s.title4 = title4
    link_s.link4 = link4
    link_s.title5 = title5
    link_s.link5 = link5
    return link_s

# search meme. parameter: memeClass // return: 0/1
def searchMeme(SearchMeme):
    conn = pymysql.connect(host='localhost', user='root', password='k-oo1234', db='KOO', charset='utf8')
    cur = conn.cursor()

    insertSTR = "SELECT EXISTS (SELECT word FROM KOOtable where word = %s) as result"
    insertVAL = (SearchMeme.word)
    cur.execute(insertSTR, insertVAL)
    conn.commit()
    conn.close()

    result = cur.fetchone()
    if (result[0] == 1):
        return True
    elif (result[0] == 0):
        return False

def searchlink(SearchLink):
    conn = pymysql.connect(host='localhost', user='root', password='k-oo1234', db='KOO', charset='utf8')
    cur = conn.cursor()

    insertSTR = "SELECT EXISTS (SELECT word FROM LINKtable where word = %s) as result"
    insertVAL = (SearchLink.word)
    cur.execute(insertSTR, insertVAL)
    conn.commit()
    conn.close()

    result = cur.fetchone()
    if (result[0] == 1):
        return True
    elif (result[0] == 0):
        return False

# getMeme(search_word) search_word as 'K word'
def getMeme(search_word : str ):
    conn = pymysql.connect(host='localhost', user='root', password='k-oo1234', db='KOO', charset='utf8')
    cur = conn.cursor()

    searchSTR = "SELECT * FROM KOOtable WHERE word = '{}'".format(search_word)
    cur.execute(searchSTR)
    
    result = cur.fetchone()

    searchSTR_2 = "SELECT * FROM LINKtable WHERE word = '{}'".format(search_word)
    cur.execute(searchSTR_2)

    result_2 = cur.fetchone()
    conn.commit()
    conn.close()
    return result , result_2

# add meme in DB. if it is arleady in DB, return False // parameter: memeClass
def addMeme(newMeme):
    if (searchMeme(newMeme) == 1):
       # print("this meme is already in DB update it")
        updateUseFreq(newMeme,newMeme.useFreq)
        return False

    conn = pymysql.connect(host='localhost', user='root', password='k-oo1234', db='KOO', charset='utf8')
    cur = conn.cursor()
    
    insertSTR = "INSERT INTO KOOtable (word, title, link, useFreq, searchFreq ) VALUES(%s, %s, %s, %s, %s)"
    insertVAL = (newMeme.word, newMeme.title, newMeme.link, newMeme.useFreq, newMeme.searchFreq)
    cur.execute(insertSTR, insertVAL)
    
    conn.commit()
    conn.close()

    # print("new meme({}) is added".format(newMeme.word))
    return True

def addlink(newLink):
    if (searchlink(newLink) == 1):
        # print("this meme is already in DB update it")
        return False

    conn = pymysql.connect(host='localhost', user='root', password='k-oo1234', db='KOO', charset='utf8')
    cur = conn.cursor()
    
    insertSTR = "INSERT INTO LINKtable (word, title1, link1, title2, link2, title3, link3, title4, link4, title5, link5 ) VALUES(%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"
    insertVAL = (newLink.word,newLink.title1, newLink.link1,newLink.title2, newLink.link2,newLink.title3, newLink.link3,newLink.title4, newLink.link4,newLink.title5, newLink.link5)
    cur.execute(insertSTR, insertVAL)
    
    conn.commit()
    conn.close()

    return True    

# update use_freq of meme. if it is not in DB, call addMeme // parameter: memeClass, int
def updateUseFreq(curMeme, addUseFreq):
    if (searchMeme(curMeme) == 0):
        curMeme.useFreq = addUseFreq
        addMeme(curMeme)
        # print("This meme is not in DB. it's added instead of update")
        return True

    conn = pymysql.connect(host='localhost', user='root', password='k-oo1234', db='KOO', charset='utf8')
    cur = conn.cursor()
    
    updateSTR = "INSERT INTO KOOtable (word, title, link, useFreq, searchFreq ) VALUES('{}','{}', '{}', {}, {}) ON DUPLICATE KEY UPDATE useFreq = useFreq + {}".format(curMeme.word, curMeme.title,curMeme.link, curMeme.useFreq, curMeme.searchFreq, str(addUseFreq))
    
    cur.execute(updateSTR)

    conn.commit()
    conn.close()

    # print("useFreq of meme({0}) is updated {2}+{1}".format(curMeme.word, addUseFreq,curMeme.useFreq))
    return True

# update search_freq of meme. if it is not in DB, call addMeme // parameter: memeClass, int
def updateSearchFreq(curMeme, addSearchFreq):
    if (searchMeme(curMeme) == 0):
        curMeme.searchFreq = addSearchFreq
        addMeme(curMeme)
        # print("This meme is not in DB. it's added instead of update")
        return True

    conn = pymysql.connect(host='localhost', user='root', password='k-oo1234', db='KOO', charset='utf8')
    cur = conn.cursor()

    updateSTR = "INSERT INTO KOOtable (word, title, link, useFreq, searchFreq ) VALUES('{}', '{}', '{}', {}, {}) ON DUPLICATE KEY UPDATE searchFreq = searchFreq + {}".format(curMeme.word, curMeme.title,curMeme.link, curMeme.useFreq, curMeme.searchFreq, addSearchFreq)
    
    cur.execute(updateSTR)

    conn.commit()
    conn.close()

    # print("searchFreq of meme({0}) is updated {2}+{1}".format(curMeme.word, addSearchFreq , curMeme.searchFreq))

# Return ordered data by decrease //  parameter: int, int // return: tuple
# 0 : ORDER BY use_freq
# 1 : ORDER BY search_freq
def rankFreq(numOfRank, useOrSearch):    
    conn = pymysql.connect(host='localhost', user='root', password='k-oo1234', db='KOO', charset='utf8')
    cur = conn.cursor()

    if (useOrSearch ==1):
        cur.execute("SELECT * FROM KOOtable ORDER BY searchFreq DESC")
    else:
        cur.execute("SELECT * FROM KOOtable ORDER BY useFreq DESC")
    row = cur.fetchmany(size = numOfRank)
    
    conn.commit()
    conn.close()

    return row


# Delete meme. parameter: memeClass, return: boolean
def delMeme(delMeme):
    if (searchMeme(delMeme) == 0):
        return False

    conn = pymysql.connect(host='localhost', user='root', password='k-oo1234', db='KOO', charset='utf8')
    cur = conn.cursor()

    delSTR = "DELETE FROM KOOtable WHERE word = %s"
    delVAL = delMeme.word
    cur.execute(delSTR, delVAL)

    conn.commit()
    conn.close()

    # print("meme({}) is deleted". format(delMeme.word))
    return True


# -----------------------example of usage-------------------------------
if __name__ == "__main__":
    # create new meme
    newWord = 'K'
    newWord = 'hello K2'
    newLink = 'link.com'
    newFreq = 3
    newMeme = initMeme('K', 'hello K1','link.com', 3, 1)
    addMeme(newMeme)

    # update use_freq
    addUseFreq = 5
    updateUseFreq(newMeme, addUseFreq) 

    # update search_freq
    addSearchFreq = 5
    updateSearchFreq(newMeme, addSearchFreq) 

    # meme rank
    newMeme= initMeme('K2', 'hello K2','link.com', 4, 10)
    addMeme(newMeme)
    newMeme= initMeme('K3', 'hello K2','link.com', 5, 9)
    addMeme(newMeme)
    newMeme= initMeme('K4', 'hello K2','link.com', 6, 8)
    addMeme(newMeme)
    newMeme= initMeme('K5', 'hello K2','link.com', 7, 7)
    addMeme(newMeme)
    # use rank
    rankFreq(10, 0)
    # search rank
    rankFreq(10, 1)

    # delete meme
    delMeme(newMeme)