
from flask import Flask
from flask import render_template
from flask import redirect, url_for, request
from DB_Functions import getMeme, rankFreq, updateSearchFreq, initMeme
import random
file = open('image_source.txt','r')
image_list=[]
while True:
    tp = file.readline()
    if tp =='':
        break
    image_list.append(tp)

    
app = Flask(__name__)


# get data from db
rank_list = rankFreq(20,0)
cloud_list = []
for element in rank_list:
    cloud_list.append(
    {
        "x":"{}".format(element[1]),
        "value":element[4],
        "category":"{}".format(str(random.randrange(1,10)))
    }
    )
search_list = []

@app.route('/')
def gohome():
    return redirect(url_for('home'))

@app.route('/home/')
def home():
    randnum=random.randrange(len(image_list))
    rank_list_s = rankFreq(5,1)
    search_list.clear()
    for element in rank_list_s:
        search_list.append([element[1],element[5]])
    return render_template(
        'home.html',
        cloud_list=cloud_list,
        image_url=image_list[randnum],
        search1 = search_list[0][0],
        search1_i = search_list[0][1],
        search2 = search_list[1][0],
        search2_i = search_list[1][1],
        search3 = search_list[2][0],
        search3_i = search_list[2][1],
        search4 = search_list[3][0],
        search4_i = search_list[3][1],
        search5 = search_list[4][0],
        search5_i = search_list[4][1],
        )

@app.route('/home_english/')
def home_english():
    randnum=random.randrange(len(image_list))
    rank_list_s = rankFreq(5,1)
    search_list.clear()
    for element in rank_list_s:
        search_list.append([element[1],element[5]])
    return render_template(
        'home_english.html',
        cloud_list=cloud_list,
        image_url=image_list[randnum],
        search1 = search_list[0][0],
        search1_i = search_list[0][1],
        search2 = search_list[1][0],
        search2_i = search_list[1][1],
        search3 = search_list[2][0],
        search3_i = search_list[2][1],
        search4 = search_list[3][0],
        search4_i = search_list[3][1],
        search5 = search_list[4][0],
        search5_i = search_list[4][1],
        )

@app.route('/home_japanese/')
def home_japanese():
    randnum=random.randrange(len(image_list))
    rank_list_s = rankFreq(5,1)
    search_list.clear()
    for element in rank_list_s:
        search_list.append([element[1],element[5]])
    return render_template(
        'home_japanese.html',
        cloud_list=cloud_list,
        image_url=image_list[randnum],
        search1 = search_list[0][0],
        search1_i = search_list[0][1],
        search2 = search_list[1][0],
        search2_i = search_list[1][1],
        search3 = search_list[2][0],
        search3_i = search_list[2][1],
        search4 = search_list[3][0],
        search4_i = search_list[3][1],
        search5 = search_list[4][0],
        search5_i = search_list[4][1],
        )

@app.route('/home_chinese/')
def home_chinese():
    randnum=random.randrange(len(image_list))
    rank_list_s = rankFreq(5,1)
    search_list.clear()
    for element in rank_list_s:
        search_list.append([element[1],element[5]])
    return render_template(
        'home_chinese.html',
        cloud_list=cloud_list,
        image_url=image_list[randnum],
        search1 = search_list[0][0],
        search1_i = search_list[0][1],
        search2 = search_list[1][0],
        search2_i = search_list[1][1],
        search3 = search_list[2][0],
        search3_i = search_list[2][1],
        search4 = search_list[3][0],
        search4_i = search_list[3][1],
        search5 = search_list[4][0],
        search5_i = search_list[4][1],
        )

@app.route('/home_french/')
def home_french():
    randnum=random.randrange(len(image_list))
    rank_list_s = rankFreq(5,1)
    search_list.clear()
    for element in rank_list_s:
        search_list.append([element[1],element[5]])
    return render_template(
        'home_french.html',
        cloud_list=cloud_list,
        image_url=image_list[randnum],
        search1 = search_list[0][0],
        search1_i = search_list[0][1],
        search2 = search_list[1][0],
        search2_i = search_list[1][1],
        search3 = search_list[2][0],
        search3_i = search_list[2][1],
        search4 = search_list[3][0],
        search4_i = search_list[3][1],
        search5 = search_list[4][0],
        search5_i = search_list[4][1],
        )

@app.route('/home_spanish/')
def home_spanish():
    randnum=random.randrange(len(image_list))
    rank_list_s = rankFreq(5,1)
    search_list.clear()
    for element in rank_list_s:
        search_list.append([element[1],element[5]])
    return render_template(
        'home_spanish.html',
        cloud_list=cloud_list,
        image_url=image_list[randnum],
        search1 = search_list[0][0],
        search1_i = search_list[0][1],
        search2 = search_list[1][0],
        search2_i = search_list[1][1],
        search3 = search_list[2][0],
        search3_i = search_list[2][1],
        search4 = search_list[3][0],
        search4_i = search_list[3][1],
        search5 = search_list[4][0],
        search5_i = search_list[4][1],
        )




@app.route('/search',methods=['POST'])
def search(input=None):
    if request.method == 'POST':
        temp = request.form['input']
    else:
        temp = None
    return redirect(url_for('searchview',input = temp))

@app.route('/<string:input>/')
def searchview(input):
    data, data2 = getMeme("K-{}".format(input))
    if data == None:
        data = getMeme("K{}".format(input))
        if data == None:
            data = getMeme("K {}".format(input))
    if data[0] == None:
        return render_template('result.html',input = input,flag = 0)
    else:
        updateSearchFreq(initMeme(data[1],data[2],data[3],data[4],data[5]),1)
        if data2 != None:
            return render_template(
                'result.html',
                input = input,
                flag = 2, 
                word = data[1],
                title = data[2],
                url = data[3],
                title1 = data2[2],
                title2 = data2[4],
                title3 = data2[6],
                title4 = data2[8],
                title5 = data2[10],
                url1 = data2[3],
                url2 = data2[5],
                url3 = data2[7],
                url4 = data2[9],
                url5 = data2[11],
                searchFreq = data[5]+1
                )
        else:
            return render_template(
                'result.html',
                input = input,
                flag = 1, 
                word = data[1],
                title = data[2],
                url = data[3],
                searchFreq = data[5]+1
                )
            


    

if __name__ == '__main__':
    app.run()
