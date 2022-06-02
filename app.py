
from flask import Flask
from flask import render_template
from flask import redirect, url_for, request
from DB_Functions import getMeme, rankFreq
import random

app = Flask(__name__)

# #임시 DB 데이터 (형식 미정)
# topics = [ 
#     { 'topic' : '방역', 
#     'mean' : '대한민국에 존재했었던 코로나바이러스감염증-19 관련 방역 시스템을 총체적으로 일컫는 신조어', 
#     'ratio': 19.8
#     },

#     { 'topic' : 'pop', 
#     'mean' : '한국 외의 나라에서 한국의 대중가요를 일컫는 말', 
#     'ratio': 11.9
#     },

#     { 'topic' : '뷰티', 
#     'mean' : 'kpop, k드라마 등의 한류 열풍으로 알려진 한국의 화장, 의상 등의 스타일을 뜻하는 말', 
#     'ratio': 10.8
#     },
    
# ]


# def topictem(topic, mean):
#     return f'''<html>
#     <head>
# 	<title>{topic}</title>
#     </head>
#     <body>
# 	<h1>{topic}</h1>
# 	<br>
	
# 	<h3>{mean}<h3>
#     </body>
#     </html>'''

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
def home():
    return render_template('home.html',cloud_list=cloud_list)



# @app.route('/<mytopic>/')
# def topicview(mytopic):
#     mean = ''
#     for tp in topics:
#         if(mytopic == tp['topic']) :
#             print("해당되는 키워드 : :  --- ", mytopic)
#             mean = tp['mean']

#     return topictem(mytopic, mean)


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
