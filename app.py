from flask import Flask, request
from decouple import config
import requests
import pprint

app = Flask(__name__)


API_TOKEN = config('API_TOKEN') #상수는 대문자
NAVER_CLIENT_ID = config('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = config('NAVER_CLIENT_SECRET')


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

    if text[0:4] == '/한영 ':
        headers = {
            'X-Naver-Client-Id': NAVER_CLIENT_ID,
            'X-Naver-Client-Secret': NAVER_CLIENT_SECRET, #딕셔너리에는 추가할수잇으니 마지막에도 ,넣는걸 추천~
        }
        data = {
            'source' : 'ko',
            'target' : 'en',
            'text' : text[4:] # '/번역'이후의 문자열만 대상으로 번역
        }
        papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
        papago_res = requests.post(papago_url, headers=headers, data=data)
        transltatedtext = papago_res.json().get('message').get('result').get('translatedText')

    if text[0:4] == '/영한 ':
        headers = {
            'X-Naver-Client-Id': NAVER_CLIENT_ID,
            'X-Naver-Client-Secret': NAVER_CLIENT_SECRET, #딕셔너리에는 추가할수잇으니 마지막에도 ,넣는걸 추천~
        }
        data = {
            'source' : 'en',
            'target' : 'ko',
            'text' : text[4:] # '/번역'이후의 문자열만 대상으로 번역
        }
        papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
        papago_res = requests.post(papago_url, headers=headers, data=data)
        transltatedtext = papago_res.json().get('message').get('result').get('translatedText')

    base_url = 'https://api.telegram.org'
    api_url = f'{base_url}/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={transltatedtext}'
    requests.get(api_url)

    return '', 200



if __name__ == '__main__' :
    app.run(debug=True)