
from flask import Flask
from flask import render_template
from flask import redirect, url_for, request
from DB_Functions import getMeme, rankFreq, updateSearchFreq, initMeme
import random

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

@app.route('/')
def gohome():
    return redirect(url_for('home'))

@app.route('/home/')
def home():
    return render_template('home.html',cloud_list=cloud_list)


@app.route('/home_english/')
def home_english():
    return render_template('home_english.html',cloud_list=cloud_list)


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
