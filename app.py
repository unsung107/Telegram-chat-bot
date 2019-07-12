from flask import Flask, request
from decouple import config
import requests
import pprint

app = Flask(__name__)
API_TOKEN = config('API_TOKEN') #상수는 대문자
base_url = 'https://api.telegram.org'


@app.route('/')
def hello():
    return f'Hello, world!!!'


@app.route('/greeting/<name>')
def greeting(name):
    return f'hello, {name}'

@app.route(f'/{API_TOKEN}', methods=['POST'])
def telegram():
    from_telegram = request.get_json()
    #pprint.pprint(from_telegram)
    
    if from_telegram.get('message') is not None :
        # 우리가 원하는 로직
        chat_id = from_telegram.get('message').get('chat').get('id')
        text = from_telegram.get('message').get('text')

    if '주마' in text:
        talk = '도비는 이제 자유에요!'
    else :
        talk = '놓아줘라 이 악마야!!!'

    api_url = f'{base_url}/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={talk}'
    requests.get(api_url)

    return '', 200



if __name__ == '__main__' :
    app.run(debug=True)