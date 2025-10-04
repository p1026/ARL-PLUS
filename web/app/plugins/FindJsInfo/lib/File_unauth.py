# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/12 5:19 PM
@Auth ： xinghe
@File ：File_unauth.py
@IDE ：PyCharm
@Motto:但行好事，莫问前程
"""

from urllib3.exceptions import InsecureRequestWarning
from queue import Queue
import threading
from app.plugins.FindJsInfo.lib.Findjslink import FindInfo
from app.plugins.FindJsInfo.lib.url_unauth import Unauth_process
import urllib3

from app import utils
from app.utils import conn_db
from app.arlconfig import Config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from queue import Queue
import threading


def ZooSpaider(queue, api_list):
    while not queue.empty():
        domain = queue.get()
        try:
            result = main(domain)
            api_list.extend(result)
        except Exception as e:
            pass

def main(user_input_url):
    my_finder = FindInfo()
    # 调用 Request_Js 方法，并传入一个 URL 参数
    data1, data2 = my_finder.Request_Js(user_input_url)
    # 从Path_Screen函数返回的js列表中深入递归提取path
    data3 = my_finder.api_list
    path_list_tmp = my_finder.While_Requests_Js(data2, user_input_url)
    # 保存最终提取的path，并去重，除去开头小数点
    path = []
    p_temp = []
    path.extend(data1)
    path.extend(path_list_tmp)
    path = list(set(path))
    for p_t in path:
        p_temp.append(p_t)
    for p in p_temp:
        if p.split("/")[0] == '.':
            p_re = p.replace(".", "")
            if p in path:
                path.remove(p)
            if p_re not in path:
                path.append(p_re)
    unauth = Unauth_process()
    api_list = unauth.geturl(user_input_url, path, data3)
    return api_list


def biuld_data(datas, link):
    data = dict()
    data['jslinks'] = link
    data['data'] = datas
    data['create_date'] = utils.curr_date()
    return data


def file_thread(file_url):
    queue = Queue(maxsize=150000)
    for i in open(file_url, 'r+'):
        queue.put(i.replace('\n', ''))

    api_list = []
    thread = []
    thread_count = 100

    for i in range(thread_count):
        t = threading.Thread(target=ZooSpaider, args=(queue, api_list))
        thread.append(t)
        t.start()

    for t in thread:
        t.join()

    return api_list
