#!/usr/bin/python
# It's for connecting with mySQL database
import pymysql
from dataclasses import dataclass

# -------------------------memeClass------------------------------
@dataclass
class memeClass:
    word: str = None
    title: str = None
    useFreq: int = None
    searchFreq: int = None


# -------------------------functions------------------------------
# initMeme, searchMeme, addMeme, updateUseFreq, updateSearchFreq, rankMeme, delMeme

# create new Meme // parameter: str, str, int, int
def initMeme(word, title, useFreq, searchFreq):
    meme = memeClass()
    meme.word = word
    meme.title = title
    meme.useFreq = useFreq
    meme.searchFreq = searchFreq
    #if (searchMeme(meme) == 1):
    #    return False
    return meme

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
    if (result == 1):
        return True
    elif (result == 0):
        return False

# add meme in DB. if it is arleady in DB, return False // parameter: memeClass
def addMeme(newMeme):
    if (searchMeme(newMeme) == 1):
        print("this meme is already in DB update it")
        return False

    conn = pymysql.connect(host='localhost', user='root', password='k-oo1234', db='KOO', charset='utf8')
    cur = conn.cursor()
    
    insertSTR = "INSERT IGNORE INTO KOOtable VALUES(%s, %s, %s, %s)"
    insertVAL = (newMeme.word, newMeme.title, newMeme.useFreq, newMeme.searchFreq)
    cur.execute(insertSTR, insertVAL)
    
    conn.commit()
    conn.close()

    print("new meme({}) is added".format(newMeme.word))
    return True

# update use_freq of meme. if it is not in DB, call addMeme // parameter: memeClass, int
def updateUseFreq(curMeme, addUseFreq):
    if (searchMeme(curMeme) == 0):
        curMeme.useFreq = addUseFreq
        addMeme(curMeme)
        print("This meme is not in DB. it's added instead of update")
        return True

    conn = pymysql.connect(host='localhost', user='root', password='k-oo1234', db='KOO', charset='utf8')
    cur = conn.cursor()

    updateSTR = "INSERT INTO KOOtable VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE use_freq = use_freq + %s"
    updateVAL = (newMeme.word, newMeme.title, newMeme.useFreq, newMeme.searchFreq, addUseFreq)
    cur.execute(updateSTR, updateVAL)

    conn.commit()
    conn.close()

   print("new meme is added ({0}, {1}, {2}, {3})".format(newMeme.word, newMeme.title, newMeme.useFreq, newMeme.searchFreq))
    return True

# update search_freq of meme. if it is not in DB, call addMeme // parameter: memeClass, int
def updateSearchFreq(curMeme, addSearchFreq):
    if (searchMeme(curMeme) == 0):
        curMeme.searchFreq = addSearchFreq
        addMeme(curMeme)
        print("This meme is not in DB. it's added instead of update")
        return True

    conn = pymysql.connect(host='localhost', user='root', password='k-oo1234', db='KOO', charset='utf8')
    cur = conn.cursor()

    updateSTR = "INSERT INTO KOOtable VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE search_freq = search_freq + %s"
    updateVAL = (newMeme.word, newMeme.title, newMeme.useFreq, newMeme.searchFreq, addSearchFreq)
    cur.execute(updateSTR, updateVAL)

    conn.commit()
    conn.close()

    print("search_freq of meme({0}) is updated +{1}".format(curMeme.word, addSearchFreq))

# Return ordered data by decrease //  parameter: int, int // return: tuple
# 0 : ORDER BY use_freq
# 1 : ORDER BY search_freq
def rankFreq(numOfRank, useOrSearch):    
    conn = pymysql.connect(host='localhost', user='root', password='k-oo1234', db='KOO', charset='utf8')
    cur = conn.cursor()

    rankSTR = "SELECT * FROM KOOtable ORDER BY %s DESC"    
    rankVAL = ('use_freq')
    
    if (useOrSearch ==1):
        rankVAL = ('search_freq')

    cur.execute(rankSTR, rankVAL)

    row = cur.fetchall()
    if (len(row)<numOfRank):
        numOfRank = len(row)

    for i in range(0, numOfRank):
        print(row[i])

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

    print("meme({}) is deleted". format(delMeme.word))
    return True


# -----------------------example of usage-------------------------------

# create new meme
newWord = 'K'
newWord = 'hello K2'
newFreq = 3
newMeme = initMeme('K', 'hello K1', 3, 1)
addMeme(newMeme)

# update use_freq
addUseFreq = 5
updateUseFreq(newMeme, addUseFreq) 

# update search_freq
addSearchFreq = 5
updateSearchFreq(newMeme, addSearchFreq) 

# meme rank
newMeme= initMeme('K2', 'hello K2', 4, 10)
addMeme(newMeme)
newMeme= initMeme('K3', 'hello K2', 5, 9)
addMeme(newMeme)
newMeme= initMeme('K4', 'hello K2', 6, 8)
addMeme(newMeme)
newMeme= initMeme('K5', 'hello K2', 7, 7)
addMeme(newMeme)
# use rank
rankFreq(10, 0)
# search rank
rankFreq(10, 1)

# delete meme
delMeme(newMeme)