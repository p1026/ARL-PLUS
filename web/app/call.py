# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/30 12:12 PM
@Auth ： xinghe
@File ：call.py
@IDE ：PyCharm
@Motto: live != end, love ++
"""

from app.services.unauth_scan import unauth_run
from app.services.packerFuzer_scan import Packerzuuer_scan
data = ["https://guguyuyin.com", "http://venus.guguyuyin.com", "https://www.guguyuyin.com"]


from app.plugins.FindJsInfo.findjs_api import findJs


print(Packerzuuer_scan(data, "sec"))
#print(unauth_run(data))

