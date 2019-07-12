import requests  #요청을 하기위한 모듈
import pprint
from decouple import config #decouple 에서부터 config 호출


base_url = 'https://api.telegram.org'
token = config('API_TOKEN') #알아서들어감
chat_id = config('CHAT_ID')
text = '도비는 이제 자유에요'

api_url = f'{base_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}'

response = requests.get(api_url)
pprint.pprint(response.json())