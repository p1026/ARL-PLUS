import requests, json

headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Token": "87724e6a8b304b2cbcbd61ad7749c52a", #your token
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
        push("http://127.0.0.1:5013/api/src/", src[i])
