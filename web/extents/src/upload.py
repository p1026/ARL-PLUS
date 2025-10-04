# -*- coding: utf-8 -*-
"""
@Time ： 2023/10/8 6:10 PM
@Auth ： xinghe
@File ：upload.py
@IDE ：PyCharm
@Motto: live != end, love ++
"""
import requests, json

headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Token": "", #your token
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def push(url, data):
    try:
        result = requests.post(url=url, data=json.dumps(data), headers=headers, timeout=4)
        if result.status_code == 200:
            print("ok")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    src = open("src.json", 'r')
    src = json.load(src)
    for i in range(len(src)):
        push("http://127.0.0.1/api/src/", src[i])
