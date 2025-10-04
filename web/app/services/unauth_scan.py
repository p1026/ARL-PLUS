# -*- coding: utf-8 -*-
"""
@Time ： 2023/7/7 23:11
@Auth ： xinghe 
@File ： unauth_scan.py 
@IDE ：  PyCharm
@Motto:  if live != end , love++
"""
import json
import os.path
import subprocess
from app.plugins.FindJsInfo.findjs_api import findJs
from app.arlconfig import Config
from app import utils

logger = utils.get_logger()


class UnAuth(object):

    def __init__(self, targets: list):
        self.targets = targets

        tmp_path = Config.TMP_PATH
        rand_str = utils.random_choices()

        self.nuclei_target_path = os.path.join(tmp_path, "nuclei_target_{}.txt".format(rand_str))

    def _gen_target_file(self):
        with open(self.nuclei_target_path, "w") as f:
            for domain in self.targets:
                domain = domain.strip()
                if not domain:
                    continue
                f.write(domain + "\n")

    def unauth_exec(self):
        data = findJs(self.nuclei_target_path)
        return data

    def run(self):

        self._gen_target_file()
        results = self.unauth_exec()
        return results


def unauth_run(targets: list):
    if not targets:
        return []

    n = UnAuth(targets=targets)
    return n.run()
