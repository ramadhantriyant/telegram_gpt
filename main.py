from os import getenv
from dotenv import load_dotenv
from requests import post
from flask import Flask, request

load_dotenv()
app = Flask(__name__)
TOKEN = getenv('TOKEN')
URL = f'https://api.telegram.org/bot{TOKEN}'


def openai(prompt):
    url = 'https://api.openai.com'
    apikey = getenv('APIKEY')
    headers = {'Authorization': f'Bearer {apikey}'}
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {
                'role': 'user',
                'content': f'{prompt}'
            }
        ],
        'temperature': 0.7
    }
    r = post(url + '/v1/chat/completions', headers=headers, json=data)
    return r.json()


def send_message(chat_id, text):
    body = {'chat_id': chat_id, 'text': text}
    r = post(URL + '/sendMessage', json=body)
    return r.json()


@app.route('/telegram', methods=['GET', 'PUT', 'DELETE'])
def telegram_get():
    return {'status': 'ok'}


@app.route('/telegram', methods=['POST'])
def telegram_post():
    body = request.get_json()
    chat_id = body['message']['chat']['id']
    message = body['message']['text']
    
    r = openai(message)
    for response in r['choices']:
        message = response['message']['content']
        sent = send_message(chat_id, message)
        return sent


if __name__ == '__main__':
    app.run(debug=True)