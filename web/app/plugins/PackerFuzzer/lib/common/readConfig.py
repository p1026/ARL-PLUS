# !/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
from configparser import ConfigParser

from app.arlconfig import Config


class ReadConfig(object):

    def __init__(self):
        self.path = Config.PFconfig_PATH  # 配置文件地址
        self.langPath = Config.PFini_PATH  # 配置文件地址
        self.config = ConfigParser()
        self.res = []

    def getValue(self, sections, key):
        self.config.read(self.path)
        options = self.config[sections][key]
        self.res.append(options)
        return self.res

    def getLang(self, sections, key):
        self.config.read(self.langPath)
        options = self.config[sections][key]
        self.res.append(options)
        return self.res
