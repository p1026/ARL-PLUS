# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/6 7:19 PM
@Auth ： xinghe
@File ：findjs_api.py
@IDE ：PyCharm
@Motto:但行好事，莫问前程
"""

from app.plugins.FindJsInfo.lib.File_unauth import file_thread

def findJs(path):
    result = file_thread(path)
    return result
