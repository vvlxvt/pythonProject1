from flask import Flask, request, jsonify
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import requests
import json, re
from flask_sslify import SSLify



app = Flask(__name__)
sslify = SSLify(app)

URL = 'https://api.telegram.org/bot6006947703:AAFiIBqbYWhmZUl6l1crqb3ZbQI4CpiXkoU/'


def write_json(data, filename = 'answer.json'):
    # пишу json в файл
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_updates():
    # получаю ответ от сервера телеграм в ответ на запрос обновлений
    url = URL + 'getUpdates'
    r = requests.get(url) # отправляет GET запрос
    write_json(r.json())
    return r.json()



def find_value(json_obj, search_key):
    # поиск по json нужного значения
    if isinstance(json_obj, dict): # если объект словарь
        for key, value in json_obj.items():  # проверяем ключ для каждого ключа
            if value == search_key:            # если совпадает -
                res = json_obj
                return round(res['quote']['USD']['price'],2)         # возвращаем значение
            elif isinstance(value, (dict, list)): # если объект словарь или список
                result = find_value(value, search_key)  # ищем рекурсивно во вложенном словаре ключ
                if result is not None:       # если результат не словарь
                    return result            # возвращаем результат из списка

    elif isinstance(json_obj, list):         # если объект список
        for item in json_obj:                # ищем результат в списке
            # Рекурсивный вызов для элементов списка
            result = find_value(item, search_key)
            if result is not None:
                return result
    return None


def get_price(crypto: str):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {'start': '1','limit': '5000','convert': "USD"}
    headers = {'Accepts': 'application/json','X-CMC_PRO_API_KEY': '27668e1d-a3aa-4a74-9a74-7dcb4975c274',}
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text) # Преобразование JSON-строки в объект Python
        token = find_value(data,crypto)
        return token
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def parse_text(text):
    pattern = r"/\w+"
    cripto = re.search(pattern, text).group()
    return cripto[1:]

@app.route('/', methods = ['POST', "GET"])
def index():
    if request.method == 'POST':
        r = request.get_json()

        chat_id = r["message"]['chat']["id"]
        message = r["message"]['text']

        return jsonify(r)
    return '<h1>Hello bot!</h1>'

def send_message(chat_id, text = 'Rugby=15'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


if __name__ =='__main__':
    # main()
    app.run(debug=True)

# https://api.telegram.org/bot6006947703:AAFiIBqbYWhmZUl6l1crqb3ZbQI4CpiXkoU/setWebhook?url=https://ebb9-94-43-154-7.ngrok-free.app
# https://api.telegram.org/bot6006947703:AAFiIBqbYWhmZUl6l1crqb3ZbQI4CpiXkoU/deleteWebhook
# https://api.telegram.org/bot6006947703:AAFiIBqbYWhmZUl6l1crqb3ZbQI4CpiXkoU/setWebhook?url=vvlxvt.pythonanywhere.com