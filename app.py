
from flask import Flask
from flask import render_template
from flask import redirect, url_for, request
from DB_Functions import getMeme, rankFreq
import random

app = Flask(__name__)


# get data from db
rank_list = rankFreq(20,0)
cloud_list = []

for element in rank_list:
    cloud_list.append(
    {
        "x":"{}".format(element[1]),
        "value":element[3],
        "category":"{}".format(str(random.randrange(1,10)))
    }
)

@app.route('/')
def gohome():
    return redirect(url_for('home'))

@app.route('/home/')
def home():
    return render_template('home.html',cloud_list=cloud_list)


@app.route('/search',methods=['POST'])
def search(input=None):
    if request.method == 'POST':
        temp = request.form['input']
    else:
        temp = None
    return redirect(url_for('searchview',input = temp))

@app.route('/<string:input>/')
def searchview(input):
    data = getMeme("K-{}".format(input))
    if data == None:
        data = getMeme("K{}".format(input))
        if data == None:
            data = getMeme("K {}".format(input))
    if data == None:
        return render_template('result.html',input = input,flag = 0)
    else:
        return render_template('result.html',input = input,flag = 1, word = data[1],title = data[2])

    

if __name__ == '__main__':
    app.run()
