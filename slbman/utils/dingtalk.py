import json
import requests
from slbman.settings import webhook


def send_message(message):
    headers = {"Content-Type": "application/json ;charset=utf-8 "}
    data = {
        "msgtype": "text",
        "text": {"content": message},
    }
    data = json.dumps(data)
    res = requests.post(webhook, data=data, headers=headers)
    print(res.text)


if __name__ == '__main__':
    msg = '''monitor test!'''
    send_message(msg)
