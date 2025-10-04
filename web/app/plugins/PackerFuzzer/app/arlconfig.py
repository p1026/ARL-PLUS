# -*- coding: utf-8 -*-
"""
@Time ： 2024/5/14 4:23 PM
@Auth ： xinghe
@File ：arlconfig.py
@IDE ：PyCharm
@Motto: live != end, love ++
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    PackerFuzzer_PATH = os.path.join(basedir, '../PackerFuzzer.py')
    PFresult_PATH = os.path.join(basedir, '../result/')
    PFlog_PATH = os.path.join(basedir, '../')
    PFini_PATH = os.path.join(basedir, '../doc/lang.ini')
    PFconfig_PATH = os.path.join(basedir, '../config.ini')