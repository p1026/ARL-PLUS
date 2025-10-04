# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/5 00:48
@Auth ： xinghe 
@File ： PackerFuzzer_api.py 
@IDE ：  PyCharm
@Motto:  if live != end , love++
"""
import os


def api():
    list_url = ["https://kgrealtime.daojia.com", "https://scanaly.aeonlife.com.cn"]
    for i in list_url:
        os.system(f"/Users/xinghe/opt/anaconda3/envs/arl/bin/python PackerFuzzer.py -u {i}")

api()
