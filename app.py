

from flask import Flask
from flask import render_template
from flask import redirect, url_for


app = Flask(__name__)

#임시 DB 데이터 (형식 미정)
topics = [ 
    { 'topic' : '방역', 
    'mean' : '대한민국에 존재했었던 코로나바이러스감염증-19 관련 방역 시스템을 총체적으로 일컫는 신조어', 
    'ratio': 19.8
    },

    { 'topic' : 'pop', 
    'mean' : '한국 외의 나라에서 한국의 대중가요를 일컫는 말', 
    'ratio': 11.9
    },

    { 'topic' : '뷰티', 
    'mean' : 'kpop, k드라마 등의 한류 열풍으로 알려진 한국의 화장, 의상 등의 스타일을 뜻하는 말', 
    'ratio': 10.8
    },
    
]


def topictem(topic, mean):
    return f'''<html>
    <head>
	<title>{topic}</title>
    </head>
    <body>
	<h1>{topic}</h1>
	<br>
	
	<h3>{mean}<h3>
    </body>
    </html>'''
    

@app.route('/')
def home():
    return render_template('home.html')



@app.route('/<mytopic>/')
def topicview(mytopic):
    mean = ''
    for tp in topics:
        if(mytopic == tp['topic']) :
            print("해당되는 키워드 : :  --- ", mytopic)
            mean = tp['mean']

    return topictem(mytopic, mean)




