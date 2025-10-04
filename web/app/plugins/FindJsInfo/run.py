# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/12 2:51 PM
@Auth ： xinghe
@File ：run.py
@IDE ：PyCharm
@Motto:但行好事，莫问前程
"""

import argparse
import time
from lib.url_unauth import Unauth_process
from lib.Findjslink import FindInfo
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class MyClass:
    parser = argparse.ArgumentParser(description='Demo program for argparse with -u and -l options')
    parser.add_argument('-u', '--url', type=str, help='URL to process')
    parser.add_argument('-l', '--file', type=str, help='File name')

    def __init__(self, input_string):
        self.input_string = input_string

    def url_input(self):
        if self.input_string.startswith('http'):
            user_input_url = self.input_string
            my_finder = FindInfo()
            try:
                # 调用 Request_Js 方法，并传入一个 URL 参数
                data1, data2 = my_finder.Request_Js(user_input_url)
                # 从Path_Screen函数返回的js列表中深入递归提取path
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
                unauth.geturl(user_input_url, path)
            except Exception as err:
                print("[+] 请校验输入参数 {}".format(err))
                pass
        else:
            print("[+] 不是一个有效域名")

    def file_input(self):
        if self.input_string.endswith('txt'):
            output = self.input_string
            from lib.File_unauth import file_thread
            try:
                file_thread(output)
            except Exception as err:
                print(f"[+] 文件未找到{err}")
                pass


def main():
    # 从终端输入 -u 和 -l 参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str)
    parser.add_argument('-l', '--file', type=str)
    args = parser.parse_args()

    # 实例化该类并处理输入字符串
    if args.url:
        MyClass(args.url).url_input()
    elif args.file:
        MyClass(args.file).file_input()
    else:
        parser.print_help()


if __name__ == '__main__':
    print("[{}]".format(time.strftime('%H:%M:%S', time.localtime(time.time()))),
          f"\033[1;36m 正在获取js文件并解析\033[0m\033[1;31m\033[0m")
    main()
    print("[+] 搜索结束")
