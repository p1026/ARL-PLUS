# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/12 4:54 PM
@Auth ： xinghe
@File ：url_unauth.py
@IDE ：PyCharm
@Motto:但行好事，莫问前程
"""
import re
import requests
from app.plugins.FindJsInfo.lib.Findjslink import FindInfo

from app.utils import get_logger

logger = get_logger()
class Unauth_process:

    def __int__(self):
        super().__init__()

    def is_not_matched(self, string):
        regex = re.compile(
            r"\.(pub|swf|avif|webp|txs|tx|xlsx|word|pdf|js.*|.*JSESSIONID|html|woff|ico|jpg|png|mp3|mp4|jsessionid.*|wasm)$|text\/(javascript|css)|static\/(css|js)|M/D/YYYY|img.*|.*img|.*node_modules|node_modules.*|!/|/\$|://|/?#|.woff?|/条/页|.ttf|.*jsessionid=",
            re.IGNORECASE)
        return not bool(regex.search(string))

    def geturl(self, url, path, data3):
        result_list = []
        for i in path:
            if self.is_not_matched(str(i)):
                try:
                    result = requests.get(url=url + i, timeout=3, verify=False)
                    if result.status_code == 200 or result.status_code == 302 or result.status_code == 405:
                        if len(result.text) != 0 and len(
                                result.text) < 2000 and 'html' not in result.text and "Apache" not in result.text and "Nginx" not in result.text and "PNG" not in result.text and "Forbidden" not in result.text and "HTML" not in result.text and "image" not in result.text and "401" not in result.text and "登录".encode("utf-8") not in result.text:
                            logger.info(
                                f'\033[1;32m[Success]\033[0m\033[1;31m\033[0m \033[0;33m{result.url}\033[0m \033[0;33m{result.status_code}\033[0m \033[0;33m{len(result.text)}\033[0m \033[1;32m{result.text}\033[0m')
                            for j in data3:
                                if i == j["api"]:
                                    result_list.append(self.biud_data(result, j["jslink"]))
                except Exception as e:
                    pass
        result_list = [i for n, i in enumerate(result_list) if i not in result_list[n + 1:]]
        return result_list

    def biud_data(self, result, jslink):
        data = dict()
        data['url'] = result.url
        data['jslink'] = jslink
        data['len'] = str(len(result.text))
        data['status_code'] = result.status_code
        if len(result.text) < 2000:
            data['content'] = result.text.replace('\n', '')
        else:
            data['content'] = result.url
        return data
